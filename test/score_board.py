import tkinter as tk
import tkinter.ttk as ttk
import pandas as pd

import sys
sys.path.append('../')

import ui.board as board

if __name__ == '__main__':
	root = tk.Tk()
	data = pd.read_csv('../resource/history/T1F1.csv', sep = ',', index_col = 0, encoding = 'utf-8')
	ic = 3
	threshold = 2
	prev = None
	skip = None
	cont = None
	finalize = None
	result = board.result(root, data, ic, threshold, 3, skip, cont, finalize)
	result.statusbar.update('Step 1', 1, 1, 10, 0, 0)
	root.mainloop()