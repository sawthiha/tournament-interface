import model.key as key
import model.audio as audio
import model.process as process

class ProcessDirector:
	def __init__(self, *args, **kwargs):
		self._process = None
		self._keymap = None
		self._judge_view = None
		self._board = None

	def pause(self, caller):
		''' Pause the process. No key input! '''
		if caller['text'] == 'Pause':
			self._keymap.disable()
			caller['text'] = 'Unpause'
		else:
			self._keymap.disable(enabled = True)
			caller['text'] = 'Pause'

	def onNext(self):
		candidate = self._process.next_candidate()
		if candidate == -1:
			self._process.save()
			steps, step, step_type, step_no, data, candidates, dropped, passed, highlights = self._process.overall_status()
			self._keymap.disable()

			if step_type != process.STEP:
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

	def key_on(self, key, value):
		self._process.cur_stage()[key] = value
		self._judge_view[int(key) - 1] = value
		audio.AUDIO.keypressed()
		is_complete, is_update = self._keymap.activate(key)
		if is_complete:
			update_total()
			if not is_update:
				root.after(int(config.controller['Delay']) * 1000, next_candidate)

	def key_off(self, key, value):
		pass

	def onDataComplete(self):


	@classmethod
	def director(cls, root, process):
		
		cls(process = process, judge_view = judge_view, keymap = , board = )