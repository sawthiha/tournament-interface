import config.config as config
import controller.control_history as history
import model.tools as tools
import model.manipulator as manipulator

STEP = 1
FINAL = 0
TB = -1
RESULT = -2

history.FORMAT = {STEP : history.history.format_step, FINAL : history.history.format_final, TB : history.history.format_tb, RESULT : history.history.format_result}

class Process:
	__slots__ = 'info', 'judges', 'stages', 'iterator', 'immutable', 'observers', 'groups', 'highlights', 'cur_group'

	def __init__(self, info, judges, stages, immutable = False):
		self.info = info
		self.judges = judges
		self.stages = stages
		self.iterator = self.stage_count() - 1
		self.immutable = immutable
		self.observers = []

	def next_candidate(self):
		candidate = self.cur_stage().next_candidate()
		return candidate
		
	def view_status(self):
		step = self.cur_stage()
		candidate = self.cur_candidate()
		candidates = step.candidates()
		progress = step.progress()
		dropped = step.dropped(is_overall = False)
		passed = step.passed(is_overall = False)
		return step, candidate, candidates, progress, dropped, passed

	def forward(self, to):
		cur_step = self.cur_stage()
		data = cur_step.data.copy(deep = True)
		cur_type = cur_step.type

		if cur_type == STEP:
			data = filter_by_total(data, self.threshold())
			next_step = final(data) if to == FINAL else step(to, data)
		elif cur_type == FINAL:
			bracket = cur_step.bracket
			group = bracket.group().get()
			if group:
				next_step = tiebreaker(bracket.iter + 1, data, bracket)
			else:
				next_step = result(data)
		elif cur_type == TB:
			bracket = cur_step.bracket
			tb = bracket.group().get()
			if tb:
				next_step = tiebreaker(cur_step.no + 0.1, data, bracket)
			else:
				group = bracket.next()
				if group:
					next_step = tiebreaker(bracket.iter + 1, data, bracket)
				else:
					next_step = result(data)
		else:
			return cur_step
		self.stages.append(next_step)
		self.iterator += 1
		self.update_ob(is_overall = True)

		return next_step

	def terminate(self):
		step = result(self.cur_stage().data)
		self.stages.append(step)
		self.iterator += 1

	def save(self):
		parent = self.info['META']['URI']
		self.cur_stage().sort()
		history.save_process(parent, self.cur_stage().type, self.cur_stage().dataframe(), self.cur_stage().no)

	def threshold(self):
		no = self.cur_stage_no()
		nJudges = len(self.judges)
		return tools.threshold(no, nJudges)

	def nJudges(self):
		return len(self.judges)

	def title(self):
		return self.info['META']['Title']

	def candidates(self):
		return int(self.info['META']['Candidates'])

	def steps(self):
		return [step.__repr__() for step in self.stages]

	def init_photos(self):
		return self.stages[0].candidates()

	def stage_count(self):
		return len(self.stages)

	def cur_stage(self):
		return self.stages[self.iterator]

	def cur_stage_no(self):
		return self.stages[self.iterator].no

	def cur_mode(self):
		return self.stages[self.iterator].cur_mode()

	def cur_candidate(self):
		return self.stages[self.iterator].cur_candidate()

	def cur_candidates(self):
		return self.stages[self.iterator].candidates()

	def cur_passed(self, is_overall = False):
		step = self.cur_stage()
		return step.passed(is_overall = is_overall)

	def cur_dropped(self, is_overall = False):
		step = self.cur_stage()
		return step.dropped(is_overall = is_overall)

	def cur_progress(self):
		return self.cur_stage().progress()

	def cur_validity(self, value):
		return False if self.cur_stage().type != STEP else value >= self.threshold()

	def cur_highlights(self):
		return self.cur_stage().highlights()

	def cur_reset(self):
		return self.cur_stage().reset()

	def cur_prev(self):
		return self.cur_stage().prev()

	def cur_next(self):
		return self.cur_stage().next()

	def cur_append(self, candidates):
		self.cur_stage().append(candidates)

	def cur_insert(self, candidates):
		self.cur_stage().insert(candidates)

	def cur_candidate_list(self):
		return self.cur_stage().candidate_list()

	def overall_status(self):
		step = self.cur_stage()
		data = step.dataframe()
		step_no = self.cur_stage_no()
		steps = self.steps()
		candidates = self.cur_candidates()
		dropped = self.cur_dropped(is_overall = True)
		passed = self.cur_passed(is_overall = True)
		highlights = self.cur_highlights()
		step_type = step.type
		return steps, step, step_type, step_no, data, candidates, dropped, passed, highlights

	def add_ob(self, observer):
		self.observers.append(observer)

	def update_ob(self, is_overall = False):
		total =	self.cur_candidates()
		progress = self.cur_progress()
		dropped = self.cur_dropped(is_overall = is_overall)
		passed = self.cur_passed(is_overall = is_overall)
		photo = self.cur_candidate()
		step = self.cur_stage()
		for ob in self.observers:
			ob.update(self.cur_stage(), self.cur_candidate(), progress, total, dropped, passed)

class Stage:
	__slots__ = 'no', 'data', 'manpl', 'type'

	def __init__(self, no, data, manpl):
		global STEP
		self.no = no
		self.data = data
		self.manpl = manpl
		self.type = STEP

	def __setitem__(self, key, value):
		self.data.iloc[self.manpl.get(), int(key) - 1] = value

	def is_(self, stage_no):
		return self.no == stage_no

	def dataframe(self):
		return self.data

	def sort(self):
		data = self.data
		threshold = tools.threshold(self.no, self.judges())
		data = data.assign(Penaltized = data['Total'] + data['Penalty']).sort_values(['Penaltized', 'ID', 'Penalty'], ascending = [False, True, False])
		logic = data['Penaltized'] >= threshold
		self.data = tools.pd.concat([data.loc[logic].sort_index(), data.loc[~logic].sort_index()]).drop('Penaltized', axis = 1)

	def cur_mode(self):
		return 0 if self.no == 1 else 1

	def total(self):
		columns = self.data.columns.difference(['Total', 'Penalty', 'TB'])
		self.data['Total'] = self.data[columns].sum(axis = 1)
		return self.data.iloc[self.manpl.get()]['Total']

	def next_candidate(self):
		idx = next(self.manpl)
		if idx == -1:
			self.sort()
			return -1
		return self.data.iloc[idx].name

	def dropped(self, is_overall = False):
		threshold = tools.threshold(self.no, self.judges())
		sliced = self.data.iloc[:self.manpl.get()] if not is_overall else self.data
		logic = (sliced['Total'] + sliced['Penalty']) < threshold
		return logic.sum()

	def passed(self, is_overall = False):
		candidates = self.manpl.get() if not is_overall else len(self.data)
		dropped = self.dropped(is_overall = is_overall)
		return candidates - dropped

	def validity(self, idx):
		''' return valid, invalid counts '''
		threshold = tools.threshold(self.no, self.judges())
		invalid = self.data['Total'] + self.data['Penalty'] < threshold
		return (~invalid).loc[idx].sum(), invalid.loc[idx].sum()

	def judges(self):
		return len(self.data.columns.difference(['Total', 'Penalty']))

	def cur_candidate(self):
		try:
			return self.data.iloc[self.manpl.get()].name
		except IndexError:
			return -1

	def progress(self):
		cur = self.manpl.get()
		return self.candidates() - cur

	def candidates(self):
		return len(self.data)

	def highlights(self):
		no = self.no
		nJudges = self.judges()
		threshold = tools.threshold(no, nJudges)
		return [tools.invalid_candidates(self.data, threshold)]

	def ban(self, idx):
		limit = tools.threshold(self.no, self.judges())
		logic = (self.data.loc[idx, 'Total'] + self.data.loc[idx, 'Penalty']) < limit
		self.data.loc[idx, 'Penalty'] = self.data.loc[idx, 'Penalty'].where(logic, (self.data.loc[idx, 'Total'] - (limit - 1)) * -1).where(self.data.loc[idx, 'Total'] >= limit, 0)
		return self.data

	def pick(self, idx):
		limit = tools.threshold(self.no, self.judges())
		logic = (self.data.loc[idx, 'Total'] + self.data.loc[idx, 'Penalty']) >= limit
		self.data.loc[idx, 'Penalty'] = self.data.loc[idx, 'Penalty'].where(logic, limit - self.data.loc[idx, 'Total']).where(self.data.loc[idx, 'Total'] < limit, 0)
		return self.data

	def edit(self, idx):
		candidates = self.iloc(idx)
		self.manpl.insert(candidates)
		return self.manpl.next()

	def reset(self):
		idx = self.manpl.reindex(0)
		return self.data.iloc[idx].name

	def prev(self):
		idx = self.manpl.previous()
		return self.data.iloc[idx].name

	def next(self):
		idx = self.manpl.next()
		return self.data.iloc[idx].name

	def append(self, candidates):
		idx = self.iloc(candidates)
		self.manpl.append(idx)

	def insert(self, candidates):
		idx = self.iloc(candidates)
		self.manpl.insert(idx)

	def loc(self, candidates):
		return self.data.iloc[candidates].index.tolist()

	def iloc(self, candidates):
		return list(map(self.data.index.get_loc, candidates))

	def candidate_list(self):
		candidates = self.manpl.candidate_list()
		return self.data.index[candidates].tolist()

	def __repr__(self):
		return 'Step ' + str(self.no)

class Final(Stage):
	def __init__(self, data, manpl, bracket):
		global FINAL
		Stage.__init__(self, FINAL, data, manpl)
		self.type = FINAL
		self.bracket = bracket

	def next_candidate(self):
		candidate = super().next_candidate()
		if candidate == -1:
			self.bracket.reload(self.data)
		return candidate

	def highlights(self):
		return self.bracket.highlights()

	def sort(self):
		data = self.data
		self.data = data.assign(Penaltized = data['Total'] + data['Penalty']).sort_values(['Penaltized', 'Total', 'Penalty'], ascending = [False, False, False]).drop('Penaltized', axis = 1)

	def dropped(self, is_overall):
		return 0

	def passed(self, is_overall):
		return self.candidates()

	def pick(self, idx):
		logic = (self.data.loc[idx, 'Penalty'] == 0)
		self.data.loc[idx, 'Penalty'] = self.data.loc[idx, 'Penalty'].where(logic, 0)
		return self.data

	def ban(self, idx):
		logic = (self.data.loc[idx, 'Penalty'] > 0)
		self.data.loc[idx, 'Penalty'] = self.data.loc[idx, 'Penalty'].where(logic, 1)
		return self.data		

	def cur_candidate(self):
		return self.data.iloc[self.manpl.get()].name

	def validity(self, idx):
		''' return valid, invalid counts '''
		invalid = self.data['Penalty'] == 0
		return (~invalid).loc[idx].sum(), invalid.loc[idx].sum()

	def __repr__(self):
		return 'Final'

class TieBreaker(Stage):
	def __init__(self, no, data, manpl, bracket, group):
		global TB
		Stage.__init__(self, no, data, manpl)
		self.bracket = bracket
		self.group = group
		self.type = TB

	def __setitem__(self, key, value):
		self.data.iloc[self.manpl.get(), int(key) - 1] = value

	def next_candidate(self):
		candidate = super().next_candidate()
		if candidate == -1:
			self.bracket.update(self.data)
		return candidate

	def cur_mode(self):
		mode = 1 if len(self.group) > 2 else 0
		return mode

	def dataframe(self):
		rows = self.data.index[self.group.get()]
		return self.data.drop(self.data.index.difference(rows))
		#return self.data

	def total(self):
		columns = self.data.columns.difference(['Total', 'Penalty', 'TB'])
		self.data['TB'] = self.data[columns].sum(axis = 1)
		bin_mode = self.candidates() == 2
		if bin_mode:
			row = self.data.iloc[self.manpl.get()][columns]
			self.manpl.next()
			self.data.iloc[self.manpl.get()][columns] = row.replace({0 : 1, 1 : 0})
			self.data['TB'] = self.data[columns].sum(axis = 1)
		return self.data.iloc[self.manpl.get() - 1]['TB'] if bin_mode else self.data.iloc[self.manpl.get()]['TB']

	def sort(self):
		group = self.group.get()
		try:
			start, end = min(group), max(group)
			prepend = self.data.iloc[list(range(0, start))]
			sortee = self.data.iloc[group].sort_values(['Penalty', 'Total', 'TB'], ascending = [True, False, False])
			append = self.data.iloc[list(range(end + 1, len(self.data)))]
			self.data = tools.pd.concat([prepend, sortee, append])
		except IndexError:
			pass

	def highlights(self):
		groups = tools.Group.analyze_tie(self.data, idx = self.group.get())
		colour = self.group.colour
		try:
			relative_groups = [list(map(lambda x : x - group[0], group)) for group in groups]
		except IndexError:
			pass
		return [(group, colour) for group in relative_groups]

	def dropped(self, is_overall = False):
		return 0

	def passed(self, is_overall = False):
		return self.candidates()

	def cur_candidate(self):
		try:
			return self.data.iloc[self.manpl.get()].name
		except IndexError:
			return -1

	def candidates(self):
		return len(self.bracket)

	def validity(self, idx):
		''' return valid, invalid counts '''
		invalid = self.data['Penalty'] == 0
		return (~invalid).loc[idx].sum(), invalid.loc[idx].sum()

	def __repr__(self):
		return 'TB ' + '{:.1f}'.format(self.no)

class Result(Stage):
	def __init__(self, data):
		global RESULT
		Stage.__init__(self, RESULT, data, None)
		self.type = RESULT

	def __setitem__(self, key, value):
		pass

	def sort(self):
		valid = self.data['Penalty'] == 0
		valid_slice = self.data.loc[valid]
		invalid_slice = self.data.loc[~valid]
		self.data = tools.pd.concat([valid_slice, invalid_slice])

	def pick(self, idx):
		logic = (self.data.loc[idx, 'Penalty'] == 0)
		self.data.loc[idx, 'Penalty'] = self.data.loc[idx, 'Penalty'].where(logic, 0)
		return self.data

	def ban(self, idx):
		logic = (self.data.loc[idx, 'Penalty'] > 0)
		self.data.loc[idx, 'Penalty'] = self.data.loc[idx, 'Penalty'].where(logic, 1)
		return self.data

	def validity(self, idx):
		''' return valid, invalid counts '''
		invalid = self.data['Penalty'] != 0
		return (~invalid).loc[idx].sum(), invalid.loc[idx].sum()

	def candidates(self):
		return len(self.data)

	def cur_mode(self):
		return -1

	def cur_candidate(self):
		return -1

	def next_candidate(self):
		return -1

	def dropped(self, is_overall):
		return 0

	def passed(self, is_overall):
		return len(self.data)

	def progress(self):
		return -1

	def highlights(self):
		return []

	def __repr__(self):
		return 'Result'

class ProcessBuilder:
	__slots__ = 'info', 'stk', 'cur', 'judges'

	def __init__(self, info, data, judges, t_step):
		self.info = info
		self.stk = [None for i in range(0, 15)]
		self.cur = 1
		
		self.stk[0] = step(t_step, data) if t_step != FINAL else final(data)
		self.judges = judges

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		self.stk = None
		self.cur = 0

	def add_stage(self, no, data):
		self.stk[self.cur] = Stage(no, data)
		self.cur += 1

	def build(self):
		return Process(self.info, self.judges, self.stk[0: self.cur])

	def build_immutable(self):
		return Process(self.id, self.judges, self.stk[0: self.cur], self.stk_final, immutable = True)

@history.decor_save
def process_new(info, data, judges, t_step):
	with ProcessBuilder(info, data, judges, t_step) as builder:
		process = builder.build()
	return process

# TODO: support dataframes and no from history
@history.decor_read_process
def process_old(info, judges, stages, finals):
	pass

def filter_by_total(data, threshold):
	logic = (data['Total'] + data['Penalty']) > (threshold - 1)
	return data.loc[logic]

def wipe(data, step_type):
	cols = data.columns
	cols = data.columns.difference(['Total', 'Penalty']) if step_type == TB else cols
	data[cols] = 0

def step(no, data):
	candidates = list(range(0, len(data)))
	wipe(data, STEP)
	iterator = manipulator.CandidateManpl.instance(candidates)
	step = Stage(no, data, iterator)
	return step

def final(data):
	candidates = list(range(0, len(data)))
	wipe(data, FINAL)
	data = data.assign(TB = 0)
	bracket = tools.Bracket.bracket(data)
	manpl = manipulator.CandidateManpl.instance(candidates)
	step = Final(data, manpl, bracket)
	return step

def tiebreaker(no, data, bracket):
	group = bracket.copy()
	candidates = group.get()
	wipe(data, TB)
	manpl = manipulator.CandidateManpl.instance(candidates)
	step = TieBreaker(no, data, manpl, bracket, group)
	return step

def result(data):
	data = data.drop(data.columns.difference(['Penalty']).tolist(), axis = 1)
	data['Name'] = 'N/A'
	step = Result(data)
	return step