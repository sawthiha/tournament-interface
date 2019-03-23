import ui.main as main
import ui.board as board
import ui.judge as judge
import ui.tools as tools

class UIDirector:
	def __init__(self, *args, **kwargs):
		self._root = kwargs['root']
		self._main = kwargs['main']
		self._create = None
		self._judge = None
		self._score = None
		self._print = None

	def onKey(self, key, value):
		raise NotImplementedError()

	def callCreate(self):
		tools.promptcreate(self._root)

	def callJudge(self):
		raise NotImplementedError()

	def callBoard(self):
		raise NotImplementedError()

	def callMain(self):
		raise NotImplementedError()

	def destroyCreate(self):
		try:
			self._create.destroy()
			self._create = None
		except AttributeError:
			pass

	def destroyJudge(self):
		try:
			self._judge.destroy()
			self._judge = None
		except AttributeError:
			pass

	def destroyBoard(self):
		try:
			self._score.destroy()
			self._score = None
		except AttributeError:
			pass

	@classmethod
	def getDirector(cls, *args, **kwargs):
		''' 
		Get UI director.
		 '''
		main_ = main.Main.getMain(kwargs['root'])
		return cls(root = kwargs['root'], main = main_)
