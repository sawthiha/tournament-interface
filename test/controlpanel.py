import tkinter as tk
import tkinter.ttk as ttk

import sys
sys.path.append('../')

import ui.tools as tools

class Edit(tk.Toplevel):
	"""docstring for Edit"""
	def __init__(self, dependencies, *args, **kwargs):
		tk.Toplevel.__init__(self, *args, **kwargs)
		dependencies(self)
		self.__config()
		self.__load()
	
	def __config(self):
		self.grid_anchor(tk.CENTER)
		self.resizable(False, False)

	def __load(self):
		self.lblCandidate.grid(row = 0, column = 0, columnspan = 3, pady = 10)
		self.lblCur.grid(row = 0, column = 3, columnspan = 2, pady = 10)
		self.tagbar.grid(row = 1, column = 0, columnspan = 5)
		self.txtEdit.grid(row = 2, column = 0, columnspan = 3, pady = 10)
		self.btnSubmit.grid(row = 2, column = 3, columnspan = 2, pady = 10)
		self.btnPrevious.grid(row = 3, column = 0, padx = 5, pady = 5)
		self.btnReset.grid(row = 3, column = 1, padx = 5, pady = 5)
		self.frmEdit.grid(row = 3, column = 2, padx = 5, pady = 5)
		self.btnEdit.grid(row = 3, column = 3, padx = 5, pady = 5)
		self.btnNext.grid(row = 3, column = 4, padx = 5, pady = 5)

	def destroy(self):
		self.on_close()
		super().destroy()

def editpanel(root, *args, **kwargs):
	''' candidate, candidate_list, reset, previous, next, edit_strategies, on_close '''
	def dependencies(caller):
		caller.lblCandidate = ttk.Label(caller, text = 'Candidate')
		caller.varCur = tk.IntVar(caller, value = kwargs['candidate'])
		caller.lblCur = ttk.Label(caller, textvariable = caller.varCur)

		caller.tagbar = tools.TagBar(caller)
		caller.varEdit = tk.IntVar(caller, value = kwargs['candidate'])
		caller.txtEdit = ttk.Combobox(caller, textvariable = caller.varEdit, values = kwargs['candidate_list'])
		caller.btnSubmit = ttk.Button(caller, text = 'Submit', command = lambda : caller.tagbar.add(caller.varEdit.get()))

		caller.btnReset = ttk.Button(caller, text = 'Reset', command = lambda : kwargs['reset'](caller))
		caller.btnPrevious = ttk.Button(caller, text = '<', command = lambda : caller.varCur.set(kwargs['previous'](caller)))
		caller.btnNext = ttk.Button(caller, text = '>', command = lambda : caller.varCur.set(kwargs['next'](caller)))
		
		edit_strategies = kwargs['edit_strategies']
		caller.varEditKey = tk.StringVar(caller, value = list(edit_strategies.keys())[0])
		caller.frmEdit = ttk.Frame(caller)
		caller.optsEdit = [ttk.Radiobutton(caller.frmEdit ,variable = caller.varEditKey, value = key, text = key) for key, strg in zip(edit_strategies.keys(), edit_strategies.values())]
		for opt in caller.optsEdit:
			opt.pack(side = tk.LEFT)
		caller.btnEdit = ttk.Button(caller, text = 'Edit', command = lambda : edit_strategies[caller.varEditKey.get()](caller, [int(tag) for tag in caller.tagbar.all()]))
		caller.on_close = kwargs['on_close']

		caller.bind('<Escape>', lambda event: caller.destroy())
		caller.bind('<Control-greater>', lambda event: caller.btnNext.invoke())
		caller.bind('<Control-less>', lambda event: caller.btnPrevious.invoke())

	panel = Edit(dependencies)
	return panel

candidate = 1
candidate_list = [1, 2, 3]
def reset(caller):
	print('reset')

def previous(caller):
	print('previous')
	return 1

def next_(caller):
	print('next')
	return 1

def edit1(caller, candidates):
	print(candidates)

edit_strategies = {
	'1' : edit1
}

root = tk.Tk()
root.bind('<F1>', lambda event : editpanel(root, candidate = candidate, candidate_list = candidate_list, reset = reset, previous = previous, next = next_, edit_strategies = edit_strategies, on_close = lambda : print('closed')))
root.mainloop()