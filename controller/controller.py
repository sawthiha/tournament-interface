import time
import datetime

import model.process as mod_process
import model.key as mod_key
import ui.judge as mod_judge
import ui.board as mod_board
import config.controller_config as config
import controller.control_history as history
import controller.tools as tools

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

	view = mod_judge.judge(root, process.title(), process.cur_stage_no(), process.cur_candidate(), process.judges, pause, process.cur_candidates() - 1)
	process.add_ob(view)
	process.update_ob()

	def decor_selected(func):
		def wrapper(caller):
			idx = caller.table.getSelectedDataFrame().index
			step = process.cur_stage()
			
			data = func(idx, step)

			step.sort()
			caller.table.model.df = data.drop('Penalty', axis = 1)
			caller.table.model.df.insert(0, 'ID', data.index.values.tolist())
			highlights = process.cur_highlights()
			caller.highlights(highlights)
			caller.table.redraw()
			dropped = process.cur_dropped(is_overall = True)
			passed = process.cur_passed(is_overall = True)
			caller.statusbar.update(drop = dropped, passed = passed)
		return wrapper

	def decor_step(func):
		def wrapper(idx):
			step = process.stages[idx]
			def reset_statusbar(statusbar):
				step_type = step.type
				reset = statusbar.mode_score if step_type == mod_process.STEP else statusbar.mode_final
				reset()
			func(step, step.dataframe(), step.candidates(), step.passed(is_overall = True), step.dropped(is_overall = True), reset_statusbar, step.highlights())
		return wrapper

	@decor_selected
	def pick(idx, step):
		return step.pick(idx)

	@decor_selected
	def ban(idx, step):
		return step.ban(idx)

	def reset(caller):
		keymap.disable(enabled = True)
		keymap.reset(process.cur_mode())
		caller.destory()

	def cont(caller):
		to = caller.varTo.get()
		step = process.forward(to)
		steps = process.steps()
		view.default()

		if step.type == mod_process.RESULT:
			data = step.dataframe()
			step_no = 0
			candidate_list = tools.get_candidates()
			
			def decor_save_candidate(func):
				def wrapper(caller):
					candidate = caller.varName.get()
					if not candidate:
						return
					if candidate not in candidate_list['name'].values:
						candidate_list.loc[len(candidate_list) + 1] = candidate
						tools.save_candidates(candidate_list)
					func(candidate)
				return wrapper

			def logic(partial):
				return candidate_list[candidate_list['name'].str.contains(partial)]['name'].tolist()

			candidates = step.candidates()
			passed = process.cur_passed()
			drop = process.cur_dropped()

			result = mod_board.result(root, steps, decor_step, data, step, step_no, candidates, passed, drop, None, pick, ban, decor_save_candidate)
			caller.destory()
			return
		reset(caller)

	# TODO: Ringtones *
	def on(keymap, key, value):
		process.cur_stage()[key] = value
		view[int(key) - 1] = value
		keymap.activated.append(key)
		if keymap.is_all_activated():
			total = process.cur_stage().total()
			is_highlight = process.cur_stage().type == mod_process.STEP
			is_valid = process.cur_validity(total)
			view.status(process.cur_candidate(), total, is_highlight, is_valid)
			view.sum(total, is_highlight, is_valid)
			root.update()
			keymap.disable()
			root.after(int(config.controller['Delay']) * 1000, lambda : process.update_ob())
			if process.next_candidate() == -1:
				step = process.cur_stage()
				step.sort()
				process.save()
				data = process.cur_stage().dataframe()
				step_no = process.cur_stage_no()
				steps = process.steps()
				candidates = process.cur_candidates()
				drop = process.cur_dropped(is_overall = True)
				passed = process.cur_passed(is_overall = True)
				highlights = process.cur_highlights()
				step_type = process.cur_stage().type
				if step_type != mod_process.STEP:
					tiebreaker = mod_board.tiebreaker(root, steps, decor_step, data, step, step_no, candidates, passed, drop, cont, pick, ban, highlights)
				else:
					score = mod_board.score(root, steps, decor_step, data, step, step_no, candidates, passed, drop, cont, pick, ban, highlights)
				return
			keymap.reset(process.cur_mode())
			keymap.disable(enabled = True)
		else:
			pass #keymap.switch_group(key)
		root.update()
	
	def off(keymap, key, value):
		pass

	keymap = mod_key.keymap(process.judges, on, off)
	keymap.switch_mode(process.cur_mode())

	root.bind('<Key>', lambda event: keymap(event.keysym))
	root.bind('<space>', lambda event: pause(view.btnPause))
	return view