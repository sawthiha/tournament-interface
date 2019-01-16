import tkinter as tk
import tkinter.ttk as ttk
import pandas as pd

import sys
sys.path.append('../')

import config.ui_config as config
import ui.board as board

if __name__ == '__main__':
	root = config.get_root()
	data = pd.read_csv('../resource/history/T1F1.csv', sep = ',', index_col = 0, encoding = 'utf-8')
	data['Penalty'] = 0
	steps = ['Step 1', 'Step 2', 'Step 3', 'Final 1']
	step = 'Final 1'
	step_no = 1
	initial = 100
	candidates = 90
	drop = initial - candidates
	passed = candidates
	def decor_step(func):
		def wrapper(idx):
			print('Hee Hee')
		return wrapper
	
	def cont(caller):
		pass
	
	def pick(caller):
		pass

	def ban(caller):
		pass

	def reset_statusbar(statusbar):
		reset = statusbar.mode_judge
		reset()

	final = board.result(root, steps, decor_step, data, step, step_no, candidates, passed, drop, cont, pick, ban, highlights = [])

	root.mainloop()