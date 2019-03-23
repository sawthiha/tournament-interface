import sys
sys.path.append('../')

import ui.main as main
import ui.board as board
import ui.judge as judge
import ui.tools as tools

class UIDirector:
	def __init__(self, *args, **kwargs):
		self._root = kwargs['root']
		self._main = kwargs['main']
		self._judge = None
		self._board = None

	def onKey(self, key, value):
		raise NotImplementedError()


	def onJudge(self):
		raise NotImplementedError()

	def onBoard(self):
		raise NotImplementedError()

	def onMain(self):
		raise NotImplementedError()

	@classmethod
	def director(cls, *args, **kwargs):
		''' 
		Get UI director.
		 '''

		entry = main.Main.main(kwargs['root'])

		cls(*args, **kwargs, main = entry)
