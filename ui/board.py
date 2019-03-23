import tkinter as tk
import tkinter.ttk as ttk

import ui.tools as tools
import config.ui_config as config

class ScoreBoard(ttk.Frame):
	instance = None

	def __init__(self, *args, **kwargs):
		ttk.Frame.__init__(self, *args, **kwargs)

	def destroy(self):
		super().destroy()
		ScoreBoard.instance = None

	def config(self):
		tools.resizeTableByParent(self, self.table, weight_y = 0.7)
		tools.autoResizeTableCells(self.table)
		tools.cellalign(self.table)
		tools.tableFont(self.table)
		tools.unbind(self.table, '<Double-Button-1>', '<Button-2>', '<Button-3>')
		tools.unbind(self.table.rowheader, '<Button-2>', '<Button-3>')
		self.table.redraw()

	def load(self):
		self.statusbar.grid(row = 1, column = 1, padx = 10, sticky = tk.NSEW)
		self.nav_pane.grid(row = 2, column = 1, padx = 10, sticky = tk.NSEW)
		self.panTable.grid(row = 3, column = 1, pady = (0, 10))
		self.table.grid()
		self.panel.grid(row = 4, column = 1)
		self.btnTo.pack(side = tk.LEFT)
		self.btnContinue.pack(side = tk.LEFT)

	def unhighlight(self):
		self.table.setRowColors(rows = range(0, len(self.table.model.df)), clr = '#ffffff', cols = 'all')

	def highlights(self, highlights):
		self.unhighlight()
		for group, color in highlights:
			self.table.setRowColors(rows = group, clr = color, cols = 'all')

	def update(self, step, data, candidates, passed, dropped, reset_statusbar, highlights = []):
		self.statusbar.update(step = step, total = candidates, drop = dropped, passed = passed)
		self.table.clearFormatting()
		self.table.redraw()
		self.table.model.df = data.drop('Penalty', axis = 1)
		self.table.copyIndex()
		self.table.moveColumns(names = ['ID'], pos = 'start')
		tools.resizeTableByParent(self, self.table, weight_y = 0.7)
		tools.autoResizeTableCells(self.table)
		tools.cellalign(self.table)
		tools.tableFont(self.table)
		self.table.redraw()
		self.highlights(highlights)
		reset_statusbar(self.statusbar)

	@classmethod
	def board(cls, *args, **kwargs):
		if ScoreBoard.instance:
			return None
		board = cls(kwargs['root'])
		board.rowconfigure(1, weight = 1)
		panel = ttk.Frame(board)

		varTo = tk.IntVar(panel, value = kwargs['step_no'] + 1)
		btnTo = ttk.Frame(panel)
		btns = [ttk.Radiobutton(btnTo, text = str(val), variable = varTo, value = val) for val in range(int(kwargs['step_no']) + 1, 5)]
		btns.append(ttk.Radiobutton(btnTo, text = 'Final', variable = varTo, value = 0))
		for btn in btns:
			btn.pack(padx = 5, side = tk.LEFT)
		btnContinue = tk.Button(panel, text = 'Continue >')

		panTable = ttk.Frame(board)
		table = tools.table_cp(panTable, kwargs['data'])
		table.show()
		table.copyIndex()
		table.moveColumns(names = ['ID'], pos = 'start')
		
		statusbar = tools.status_bar(board)
		statusbar.update(kwargs['step'], 0, 0, kwargs['candidates'], kwargs['dropped'], kwargs['passed'])
		statusbar.remove_all()
		
		board.statusbar = statusbar
		board.panTable = panTable
		board.table = table
		board.panel = panel
		board.btnTo = btnTo
		board.varTo = varTo
		board.btnContinue = btnContinue
		
		decor_step = kwargs['decor_step']

		@decor_step
		def onAction(step, data, candidates, passed, dropped, reset_statusbar, highlights = []):
			board.update(step, data, candidates, passed, dropped, reset_statusbar, highlights)
		
		nav_pane = NavigationPane(board)
		for step in kwargs['steps']:
			nav_pane.add(step, lambda event: onAction(nav_pane.index(event.widget)))
		board.nav_pane = nav_pane
		board.config()
		board.load()
		
		board.grid(row = 0, column = 0, sticky = 'nsew')

		commands = kwargs['commands']

		cmd_dict = {
			tools.POP_PICK : lambda : commands[0](board),
			tools.POP_BAN : lambda : commands[1](board),
			tools.POP_EDIT : lambda : commands[2](board)
		}

		def popup_logic():
			step_mask = kwargs['popup_mask'](board)
			flag = sum([mask * item for mask, item in zip(step_mask, cmd_dict.keys())])
			return flag

		menu = tools.popupmenu(board.table, popup_logic, cmd_dict)
		ScoreBoard.instance = board
		return board

	@classmethod
	def step(cls, *args, **kwargs):
		try:
			board = cls.board(*args, **kwargs)
			board.highlights(kwargs['highlights'])
			board.statusbar.mode_score()
			board.btnContinue.config(command = lambda: kwargs['cont'](board))
		finally:
			return board

	@classmethod
	def tiebreaker(cls, *args, **kwargs):
		try:
			board = cls.board(*args, **kwargs)
			board.highlights(kwargs['highlights'])
			board.statusbar.mode_final()
			board.btnTo.pack_forget()
			board.varTo.set(0)
			board.btnContinue.config(command = lambda: kwargs['cont'](board))
		finally:
			return board

	@classmethod
	def result(cls, *args, **kwargs):
		try:
			board = cls.board(*args, **kwargs)
			board.statusbar.mode_final()
			board.btnTo.pack_forget()
			board.btnContinue.config(command = lambda: kwargs['cont'](board))
			board.table.bind('<Double-Button-1>', lambda event : kwargs['dbl_click'](board))
		finally:
			return board

class Tag(ttk.Button):
	def __init__(self, *args, **kwargs):
		ttk.Button.__init__(self, *args, **kwargs, style = 'board.tag.TButton')

	def __config(self):
		pass

	def __load(self):
		pass		

class NavigationPane(ttk.Frame):
	def __init__(self, *args, **kwargs):
		ttk.Frame.__init__(self, *args, **kwargs)
		self.tags = []
		self.__config()
		self.__load()
		

	def __config(self):
		pass

	def __load(self):
		pass

	def add(self, name, onAction):
		tag = Tag(self, text = name)
		tag.bind('<FocusIn>', onAction)
		tag.pack(side = tk.LEFT)
		self.tags.append(tag)

	def index(self, tag):
		return self.tags.index(tag)