import tkinter as tk
import tkinter.ttk as ttk

import ui.tools as tools
import config.ui_config as config

class ScoreBoard(ttk.Frame):
	def __init__(self, *args, **kwargs):
		ttk.Frame.__init__(self, *args, **kwargs)

	def destory(self):
		self.destroy()

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

def decor_score(func):
	def wrapper(root, steps, decor_step, data, step, step_no, candidates, passed, drop, cont, pick, ban, highlights = []):
		step_no = int(step_no)
		board = ScoreBoard(root)
		board.rowconfigure(1, weight = 1)
		panel = ttk.Frame(board)

		varTo = tk.IntVar(panel, value = step_no + 1)
		btnTo = ttk.Frame(panel)
		btns = [ttk.Radiobutton(btnTo, text = str(val), variable = varTo, value = val) for val in range(step_no + 1, 5)]
		btns.append(ttk.Radiobutton(btnTo, text = 'Final', variable = varTo, value = 0))
		for btn in btns:
			btn.pack(padx = 5, side = tk.LEFT)
		btnContinue = tk.Button(panel, text = 'Continue >')

		panTable = ttk.Frame(board)
		table = tools.table_cp(panTable, data)
		table.show()
		table.copyIndex()
		table.moveColumns(names = ['ID'], pos = 'start')
		
		statusbar = tools.status_bar(board)
		statusbar.update(step, 0, 0, candidates, drop, passed)
		statusbar.remove_all()
		
		board.statusbar = statusbar
		board.panTable = panTable
		board.table = table
		board.panel = panel
		board.btnTo = btnTo
		board.varTo = varTo
		board.btnContinue = btnContinue
		
		@decor_step
		def onAction(step, data, candidates, passed, dropped, reset_statusbar, highlights = []):
			board.update(step, data, candidates, passed, dropped, reset_statusbar, highlights)
		
		nav_pane = NavigationPane(board)
		for step in steps:
			nav_pane.add(step, lambda event: onAction(nav_pane.index(event.widget)))
		board.nav_pane = nav_pane
		board.config()
		board.load()
		
		func(board, cont, highlights)
		board.grid(row = 0, column = 0, sticky = 'nsew')

		cmd_dict = {
			tools.POP_BAN : lambda : ban(board),
			tools.POP_PICK : lambda : pick(board),
			tools.POP_EDIT : lambda : print('Edit')
		}

		menu = tools.popupmenu(board.table, )
		menu.add_command(label = 'Pick', command = lambda: pick(board))
		menu.add_command(label = 'Ban', command = lambda : ban(board))
		
		return board
	return wrapper

@decor_score
def score(board, cont, highlights):
	board.highlights(highlights)
	board.statusbar.mode_score()
	board.btnContinue.config(command = lambda: cont(board))
	return board

@decor_score
def tiebreaker(board, cont, highlights):
	board.highlights(highlights)
	board.statusbar.mode_final()
	board.btnTo.pack_forget()
	board.varTo.set(0)
	board.btnContinue.config(command = lambda: cont(board))
	return board

def decor_entry(func):
	def wrapper(root, steps, decor_step, data, step, step_no, candidates, passed, drop, cont, pick, ban, decor_save, logic, highlights = []):
		caller = func(root, steps, decor_step, data, step, step_no, candidates, passed, drop, cont, pick, ban, highlights)
		tagbar = tools.TagBar(caller.root)
		varName = tk.StringVar(caller.root)
		panName = ttk.Frame(caller.root)
		txtName = tools.AutoEntry(logic, panName, textvariable = varName)

		@decor_save
		def submit(candidate):
			tagbar.add(candidate, limit = len(data))

		btnSubmit = ttk.Button(panName, text = 'Submit', command = lambda: submit(caller))
		caller.tagbar = tagbar
		caller.panName = panName
		caller.txtName = txtName
		caller.varName = varName
		caller.btnSubmit = btnSubmit

		tagbar.grid(row = 4, column = 1)
		panName.grid(row = 5, column = 1)
		txtName.pack(side = tk.LEFT)
		btnSubmit.pack(side = tk.LEFT)
		return caller
	return wrapper

@decor_score
def result(board, cont, highlights):
	board.statusbar.mode_final()
	board.btnTo.pack_forget()
	board.btnContinue.pack_forget()
	return board