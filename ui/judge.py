import tkinter as tk
import tkinter.ttk as ttk
import random

import config.ui_config as config
import ui.tools as tools

class Judge(ttk.Frame):
	def __init__(self, dependencies, *args, **kwargs):
		ttk.Frame.__init__(self, *args, **kwargs)
		dependencies(self)
		self.__config()
		self.__load()

	def __config(self):
		self.info.grid_anchor(tk.W)
		self.grid_anchor(tk.CENTER)
		self.rowconfigure(0, weight = 1)
		self.rowconfigure(1, weight = 1)
	
	def __load(self):
		self.statusbar.grid(columnspan = 3, sticky = tk.NSEW, padx = 20)
		self.lblJudges.grid(columnspan = 3, sticky = tk.NSEW)
		self.info.grid(row = 2, column = 0)
		self.statusbox.grid(row = 2, column = 1)
		self.lblSum.grid(row = 2, column = 2, sticky = tk.E, padx = 20)
		self.btnPause.grid(row = 3, column = 1)
		self.grid(row = 0, column = 0, sticky = 'nsew')

	def __setitem__(self, key, item):
		self.varJudges[key].set(str(item))

	def status(self, candidate, total, is_highlight, is_valid = False):
		self.statusbox.update(candidate, total, is_highlight, is_valid)

	def reset_score(self):
		for var in self.varJudges:
			var.set('')
		self.lblSum.default()
		random.shuffle(self.varJudges)

	def sum(self, total, is_highlight, is_valid = False):
		self.lblSum.set(total, is_highlight, is_valid)

	def update(self, step, photo, progress, total, drop, passed):
		self.statusbar.update(step, photo, progress, total, drop, passed)
		self.reset_score()

	def default(self):
		self.lblSum.default()
		self.statusbox.default()

class ScorePanel(ttk.Frame):
	def __init__(self, vars, *args, **kwargs):
		ttk.Frame.__init__(self, *args, **kwargs)
		n = len(vars)
		width = self.winfo_screenwidth() / n - 40
		height = config.judge['Judge_Label_Height']
		self.labels = [ScoreLabel(var, self, width = width, height = height) for var in vars]
		self.__config()
		self.__load()

	def __config(self):
		pass

	def __load(self):
		self.grid_anchor(tk.CENTER)
		col = 0
		for lbl in self.labels:
			lbl.grid(row = 0, column = col, padx = 20, sticky = tk.NSEW)
			col += 1

class ScoreLabel(ttk.Frame):
	def __init__(self, var, *args, **kwargs):
		ttk.Frame.__init__(self, *args, **kwargs, style = 'Judge.TFrame')
		self.label = ttk.Label(self, textvariable = var, style = 'Judge.TLabel')
		self.var = var
		self.__config()
		self.__load()

	def __config(self):
		self.grid_propagate(0)
		self.grid_anchor(tk.CENTER)

	def __load(self):
		self.label.grid()

class TotalLabel(ScoreLabel):
	def __init__(self, var, *args, **kwargs):
		ScoreLabel.__init__(self, var, *args, **kwargs)
		self.__config()

	def __config(self):
		self.configure(width = config.judge['Total_Label_Width'], height = config.judge['Total_Label_Height'])

	def set(self, value, is_highlight, is_valid = False):
		self.var.set(value)
		if is_highlight:
			self.label['style'] = 'Valid.TLabel' if is_valid else 'Banned.TLabel'
			self['style'] = 'Valid.TFrame' if is_valid else 'Banned.TFrame'

	def default(self):
		self.var.set('')
		self.label['style'] = 'Judge.TLabel'
		self['style'] = 'Judge.TFrame'

class StatusBox(ttk.LabelFrame):
	def __init__(self, *args, **kwargs):
		ttk.LabelFrame.__init__(self, *args, **kwargs, style = 'Status.TLabelframe', text = 'Previously,')
		self.varCandidate = tk.StringVar(self)
		self.varStatus = tk.StringVar(self)
		self.lblCandidate = ttk.Label(self, text = 'Candidate: ', style = 'Status.TLabel')
		self.lblCandidate_ = ttk.Label(self, textvariable = self.varCandidate, style = 'Status.TLabel')
		self.lblStatus = ttk.Label(self, text = 'Status: ', style = 'Status.TLabel')
		self.lblStatus_ = ttk.Label(self, textvariable = self.varStatus, style = 'Status.TLabel')
		self.__config()
		self.__load()

	def __config(self):
		pass

	def __load(self):
		self.lblCandidate.grid(row = 0, column = 0)
		self.lblCandidate_.grid(row = 0, column = 1)
		self.lblStatus.grid(row = 1, column = 0)
		self.lblStatus_.grid(row = 1, column = 1)

	def update(self, candidate, status, is_highlight, is_valid = False):
		self.varCandidate.set(candidate)
		self.varStatus.set(status)
		if is_highlight:
			self.lblStatus_['style'] = 'Status.Valid.TLabel' if is_valid else 'Status.Banned.TLabel'

	def default(self):
		self.varCandidate.set('')
		self.varStatus.set('')
		self.lblStatus_['style'] = 'Status.TLabel'

class InfoBox(ttk.Frame):
	def __init__(self, title,*args, **kwargs):
		ttk.Frame.__init__(self, *args, **kwargs)
		self.lblTitle = ttk.Label(self, text = title, style = 'Status.TLabel')
		self.__config()
		self.__load()

	def __config(self):
		pass

	def __load(self):
		self.lblTitle.pack()

def judge(root, title, stage, cur_candidate, judges, pause, remain, drop = 0):
	def dependencies(judge_view):
		judge_view.statusbar = tools.status_bar(judge_view)

		judge_view.varJudges = [tk.StringVar(judge_view) for judge in judges]
		judge_view.varSum = tk.StringVar(judge_view)

		judge_view.lblJudges = ScorePanel(judge_view.varJudges, judge_view)
		judge_view.lblSum = TotalLabel(judge_view.varSum, judge_view)
	
		judge_view.info = InfoBox(title, judge_view)
		judge_view.statusbox = StatusBox(judge_view)

		judge_view.btnPause = ttk.Button(judge_view, text = 'Pause', command = lambda: pause(btnPause))

	return Judge(dependencies, root)