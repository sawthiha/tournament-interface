import config.config as config
import controller.control_history as history
import model.tools as tools

STEP = 1
FINAL = 0
TB = -1
RESULT = -2

history.FORMAT = {STEP : history.history.format_step, FINAL : history.history.format_final, TB : history.history.format_tb}

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
		candidate = self.stages[self.iterator].next_candidate()
		return candidate

	def forward(self, to):
		cur_step = self.cur_stage()
		cur_step.sort()
		data = cur_step.data.copy(deep = True)
		cur_type = cur_step.type

		if cur_type == STEP:
			data = filter_by_total(data, self.threshold())
			next_step = final(data) if to == FINAL else step(to, data)
		elif cur_type == FINAL:
			bracket = cur_step.bracket.copy()
			groups = bracket.count()
			if groups:
				next_step = tiebreaker(bracket.group + 1, data, bracket)
			else:
				next_step = result(data)
		elif cur_type == TB:
			bracket = cur_step.bracket.copy()
			tb = bracket.get()
			if tb:
				next_step = tiebreaker(cur_step.no + 0.1, data, bracket)
			else:
				group = bracket.next_group()
				if group:
					next_step = tiebreaker(bracket.group + 1, data, bracket)
				else:
					next_step = result(data)

		else:
			return cur_step
		self.stages.append(next_step)
		self.iterator += 1
		self.update_ob(is_overall = True)

		return next_step

	def save(self):
		parent = self.info['META']['URI']
		history.save_process(parent, self.cur_stage().type, self.cur_stage().dataframe(), self.cur_stage().no)

	def threshold(self):
		no = self.cur_stage_no()
		nJudges = len(self.judges)
		return tools.threshold(no, nJudges)

	def nJudges(self):
		return len(self.judges)

	def check_recap(self, threshold):
		return tools.mode_recaps(self.cur_stage().dataframe(), threshold)

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
	__slots__ = 'no', 'data', 'iterator', 'type'

	def __init__(self, no, data):
		global STEP
		self.no = no
		self.data = data
		self.iterator = 0
		self.type = STEP

	def __setitem__(self, key, value):
		self.data.iloc[self.iterator, int(key) - 1] = value

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
		return self.data.iloc[self.iterator]['Total']

	def next_candidate(self):
		if self.iterator >= self.candidates() - 1:
			return -1
		else:
			self.iterator += 1
			return self.iterator

	def dropped(self, is_overall = False):
		threshold = tools.threshold(self.no, self.judges())
		sliced = self.data.iloc[:self.iterator] if not is_overall else self.data
		logic = (sliced['Total'] + sliced['Penalty']) < threshold
		return logic.sum()

	def passed(self, is_overall = False):
		candidates = self.iterator if not is_overall else len(self.data)
		dropped = self.dropped(is_overall = is_overall)
		return candidates - dropped

	def judges(self):
		return len(self.data.columns.difference(['Total', 'Penalty']))

	def cur_candidate(self):
		return self.data.iloc[self.iterator].name

	def progress(self):
		cur = self.iterator
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

	def __repr__(self):
		return 'Step ' + str(self.no)

class Final(Stage):
	def __init__(self, data, bracket):
		global FINAL
		Stage.__init__(self, FINAL, data)
		self.type = FINAL
		self.bracket = bracket

	def highlights(self):
		self.bracket.reset(self.data)
		return self.bracket.get_zip()

	def sort(self):
		data = self.data
		self.data = data.assign(Penaltized = data['Total'] + data['Penalty']).sort_values(['Penaltized', 'Total', 'Penalty'], ascending = [False, False, False]).drop('Penaltized', axis = 1)

	def dropped(self, is_overall):
		return 0

	def passed(self, is_overall):
		return self.candidates()

	def pick(self):
		logic = (self.data.loc[idx, 'Penalty'] == 0)
		self.data.loc[idx, 'Penalty'] = self.data.loc[idx, 'Penalty'].where(logic, 0)
		return self.data

	def ban(self):
		logic = (self.data.loc[idx, 'Penalty'] > 0)
		self.data.loc[idx, 'Penalty'] = self.data.loc[idx, 'Penalty'].where(logic, 1)
		return self.data		

	def cur_candidate(self):
		return self.data.iloc[self.iterator].name

	def __repr__(self):
		return 'Final'

class TieBreaker(Stage):
	def __init__(self, no, data, bracket):
		global TB
		Stage.__init__(self, no, data)
		self.bracket = bracket
		self.type = TB

	def __setitem__(self, key, value):
		self.data.iloc[self.bracket[self.iterator], int(key) - 1] = value

	def cur_mode(self):
		mode = 1 if len(self.bracket) > 2 else 0
		return mode

	def dataframe(self):
		#rows = self.data.index[self.bracket.get()]
		#return self.data.drop(self.data.index.difference(rows))
		return self.data

	def total(self):
		columns = self.data.columns.difference(['Total', 'Penalty', 'TB'])
		self.data['TB'] = self.data[columns].sum(axis = 1)
		if self.candidates() == 2:
			row = self.data.iloc[self.bracket[self.iterator]][columns]
			self.iterator += 1
			self.data.iloc[self.bracket[self.iterator]][columns] = row.replace({0 : 1, 1 : 0})
			self.data['TB'] = self.data[columns].sum(axis = 1)
		return self.data.iloc[self.bracket[self.iterator]]['TB']

	def sort(self):
		group = self.bracket.get()
		i_idx = list(map(self.data.index.get_loc, self.data.index))
		try:
			start, end = group[0], group[len(group) - 1]
			prepend = self.data.iloc[[idx for idx in i_idx if idx < start]]
			sortee = self.data.iloc[group].sort_values(['Penalty', 'Total', 'TB'], ascending = [True, False, False])
			append = self.data.iloc[[idx for idx in i_idx if idx > end]]
			self.data = tools.pd.concat([prepend, sortee, append])
		except IndexError:
			pass

	def highlights(self):
		self.bracket.update_all(self.data)
		return self.bracket.get_zip()

	def dropped(self, is_overall = False):
		return 0

	def passed(self, is_overall = False):
		return self.candidates()

	def cur_candidate(self):
		try:
			return self.data.iloc[self.bracket[self.iterator]].name
		except IndexError:
			return -1

	def candidates(self):
		return len(self.bracket)

	def __repr__(self):
		return 'TB ' + '{:.1f}'.format(self.no)

class Result(Stage):
	def __init__(self, data):
		global RESULT
		Stage.__init__(self, RESULT, data)
		self.type = RESULT

	def __setitem__(self, key, value):
		pass

	def sort(self):
		self.data.sort_values(['Penalty', 'Total', 'TB'], ascending = [True, False, False], inplace = True)

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
	wipe(data, STEP)
	step = Stage(no, data)
	return step

def final(data):
	wipe(data, FINAL)
	data = data.assign(TB = 0)
	bracket = tools.Bracket(data)
	step = Final(data, bracket)
	return step

def tiebreaker(no, data, bracket):
	wipe(data, TB)
	step = TieBreaker(no, data, bracket)
	return step

def result(data):
	data = data.drop(data.columns.difference(['Penalty']).tolist(), axis = 1)
	data['Name'] = 'N/A'
	step = Result(data)
	return step