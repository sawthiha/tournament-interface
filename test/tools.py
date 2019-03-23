import pandas as pd
import tkinter as tk

import sys
sys.path.append('../')

import ui.tools as tools

if __name__ == '__main__':
	data = pd.read_csv('../resource/judges.csv', sep = ',', index_col = 0)
	def logic(partial):
		return data[data['name'].str.contains(partial)]['name'].tolist()
	root = tk.Tk()
	var = tk.StringVar(root)
	entry = tools.AutoEntry(root, logic = logic, textvariable = var)
	entry.pack()
	root.mainloop()