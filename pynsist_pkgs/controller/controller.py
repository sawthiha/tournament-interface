import time
import datetime
import tkinter.messagebox as message

import model.process as mod_process
import model.key as mod_key
import model.audio as mod_audio
import ui.judge as mod_judge
import ui.board as mod_board
import config.controller_config as config
import controller.control_history as history
import controller.tools as tools
import ui.controlpanel as controlpanel

''' (Pick, Ban, Edit) '''
POPUP_MASK = {
	mod_process.STEP : (True, True, True),
	mod_process.FINAL : (False, False, True),
	mod_process.TB : (False, False, True),
	mod_process.RESULT: (False, False, False),
	'Invalid' : (False, False, False)
}

def decor_create_process(is_new):
	def wrapper(func):
		def new_wrapper(root, judge_list, title, judges, photos, candidates, step):
			judges = list(map(str, range(1, judges + 1)))
			data = tools.init_data(photos, judges)
			process = mod_process.process_new(title, candidates, photos, datetime.datetime.now(), judge_list, data, judges, step)
			return func(root, process)
			
		def old_wrapper():
			pass

		return new_wrapper if is_new else old_wrapper
	return wrapper

# Logic at controller 
# Inject Logic to board
# Board menu Button-3 on injected logic
	
@decor_create_process(is_new = True)
def init_tournament(root, process):
	def pause(caller):
		if caller['text'] == 'Pause':
			keymap.disable()
			caller['text'] = 'Unpause'
		else:
			keymap.disable(enabled = True)
			caller['text'] = 'Pause'

	def decor_selected(func):
		def wrapper(caller):
			idx = caller.table.getSelectedDataFrame().index
			step = process.cur_stage()
			data = func(caller, idx, step)
			return data
			
		return wrapper

	def decor_board_update(func):
		def wrapper(caller):
			func(caller)
			step = process.cur_stage()
			step.sort()
			data = step.dataframe()
			caller.table.model.df = data.drop('Penalty', axis = 1)
			caller.table.model.df.insert(0, 'ID', data.index.values.tolist())
			highlights = process.cur_highlights()
			caller.highlights(highlights)
			caller.table.redraw()
			dropped = process.cur_dropped(is_overall = True)
			passed = process.cur_passed(is_overall = True)
			caller.statusbar.update(drop = dropped, passed = passed)
		return wrapper

	@decor_board_update
	@decor_selected
	def pick(caller, idx, step):
		return step.pick(idx)

	@decor_board_update
	@decor_selected
	def ban(caller, idx, step):
		return step.ban(idx)

	@decor_selected
	def edit(caller, idx, step):
		candidate = step.edit(idx)
		call_judgeview(caller)
		return candidate

	commands = (pick, ban, edit)

	def prev(caller):
		candidate = process.cur_prev()
		caller.varCur.set(candidate)
		call_judgeview()
		return candidate

	def next_(caller):
		candidate = process.cur_next()
		call_judgeview()
		return candidate

	def reset(caller):
		candidate = process.cur_reset()
		call_judgeview(caller)

	def edit_end(caller, candidates):
		process.cur_append(candidates)
		call_judgeview(caller)

	def edit_after(caller, candidates):
		process.cur_insert(candidates)
		call_judgeview(caller)

	edit_strategies = {
		'After' : edit_after,
		'End' : edit_end
	}

	def name_edit(board):
		idx_name = board.table.model.df.columns.get_loc('Name')
		if board.table.currentcol == idx_name:
			board.table.drawCellEntry(board.table.currentrow, board.table.currentcol)

	def f1(caller):
		keymap.disable()
		candidate = process.cur_candidate()
		candidate_list = process.cur_candidate_list()
		controlpanel.editpanel(root, candidate = candidate, candidate_list = candidate_list, reset = reset, previous = prev, next = next_, edit_strategies = edit_strategies, on_close = lambda : keymap.disable(enabled = True))

	def f2(caller):
		result = message.askquestion("Terminate the competition", "Are You Sure?", icon='warning')
		if result == 'yes':
			process.terminate()
			board = mod_board.ScoreBoard.instance
			call_result(board)
			root.unbind('<F2>')

	def end(caller):
		parent = process.info['META']['URI']
		step = process.cur_stage()
		mod_process.history.save_process(parent, step.type, caller.table.model.df, step.no)
		caller.destroy()
		view.destroy()
		unbind()

	def popup_mask(caller):
		step = process.cur_stage()
		data = step.dataframe()
		step_mask = POPUP_MASK[step.type]
		idx = caller.table.getSelectedDataFrame().index
		valid , invalid = step.validity(idx)
		mask = (invalid.__bool__(), valid.__bool__(), True)
		return [m1 and m2 for m1, m2 in zip(step_mask, mask)]

	def decor_step(func):
		def wrapper(idx):
			step = process.stages[idx]
			def reset_statusbar(statusbar):
				step_type = step.type
				reset = statusbar.mode_score if step_type == mod_process.STEP else statusbar.mode_final
				reset()
			func(step, step.dataframe(), step.candidates(), step.passed(is_overall = True), step.dropped(is_overall = True), reset_statusbar, step.highlights())
		return wrapper

	def call_judgeview(caller = None):
		step, candidate, candidates, progress, dropped, passed = process.view_status()
		view.update(step, candidate, progress, candidates, dropped, passed)
		
		if step.type == mod_process.FINAL:
			view.statusbar.mode_judge_final()
		else:
			view.statusbar.mode_judge()
		
		try:
			caller.destroy()
		except AttributeError:
			pass
		
		root.update()
		mod_audio.AUDIO.candidatechanged(process.cur_candidate())
		keymap.disable(enabled = True)
		keymap.reset(process.cur_mode())

	def call_result(caller = None):
		try:
			caller.destroy()
		except AttributeError:
			pass

		steps, step, step_type, step_no, data, candidates, dropped, passed, highlights = process.overall_status()
		result = mod_board.ScoreBoard.result(
									root = root, steps = steps, decor_step = decor_step, 
									data = data, step = step, step_no = step_no, candidates = candidates, 
									passed = passed, dropped = dropped, cont = end, popup_mask = popup_mask, commands = commands,
									highlights = highlights, dbl_click = name_edit
								)

	def cont(caller):
		to = caller.varTo.get()
		step = process.forward(to)
		steps = process.steps()
		view.default()

		if step.type == mod_process.RESULT:
			call_result(caller)
			return
		call_judgeview(caller)

	def update_total():
		total = process.cur_stage().total()
		is_highlight = process.cur_stage().type == mod_process.STEP
		is_valid = process.cur_validity(total)
		view.status(process.cur_candidate(), total, is_highlight, is_valid)
		view.sum(total, is_highlight, is_valid)
		root.update()

	def next_candidate():
		candidate = process.next_candidate()
		if candidate == -1:
			process.save()
			steps, step, step_type, step_no, data, candidates, dropped, passed, highlights = process.overall_status()
			keymap.disable()

			if step_type != mod_process.STEP:
				root.bind('<>')
				tiebreaker = mod_board.ScoreBoard.tiebreaker(
						root = root, steps = steps, 
						decor_step = decor_step, data = data, step = step, step_no = step_no, 
						candidates = candidates, passed = passed, dropped = dropped, 
						cont = cont, popup_mask = popup_mask, commands = commands, highlights = highlights
					)
				root.unbind('<F2>')
				root.bind('<F2>', lambda event: f2(tiebreaker))
			else:
				score = mod_board.ScoreBoard.step(
						root = root, steps = steps, 
						decor_step = decor_step, data = data, step = step, step_no = step_no, 
						candidates = candidates, passed = passed, dropped = dropped, 
						cont = cont, popup_mask = popup_mask, commands = commands, highlights = highlights
					)
			root.update()
			mod_audio.AUDIO.stepchanged()
			return
		call_judgeview()

	def on(keymap, key, value):
		process.cur_stage()[key] = value
		view[int(key) - 1] = value
		mod_audio.AUDIO.keypressed()
		is_complete, is_update = keymap.activate(key)
		if is_complete:
			update_total()
			if not is_update:
				root.after(int(config.controller['Delay']) * 1000, next_candidate)
	
	def off(keymap, key, value):
		pass

	bind_dict = {
		'<Key>' : lambda event: keymap(event.keysym),
		'<space>' : lambda event: pause(view.btnPause),
		'<F1>' : lambda event: f1(view),
		'<F2>' : lambda event: print('Not Implemented!')
	}

	def bind():
		for event, strategy in zip(bind_dict.keys(), bind_dict.values()):
			root.bind(event, strategy)

	def unbind():
		for event in bind_dict.keys():
			root.unbind(event)

	view = mod_judge.judge(root, process.title(), process.cur_stage_no(), process.cur_candidate(), process.judges, pause, process.cur_candidates() - 1, process.cur_stage().type != mod_process.STEP)
	process.add_ob(view)
	process.update_ob()

	keymap = mod_key.keymap(process.judges, on, off)
	keymap.switch_mode(process.cur_mode())

	bind()
	mod_audio.AUDIO.candidatechanged(process.cur_candidate())
	
	return view