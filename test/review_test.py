import pandas as pd
import tkinter as tk

import sys
sys.path.append('../')

import ui.review as review
import config.ui_config as config

if __name__ == '__main__':
	root = config.get_root()
	data = pd.read_csv('T1F1.csv')
	data = data.join(pd.Series('N/A', name = 'Step', index = data.index))
	review = review.review(root, 1, 1, data)
	#foo(1, 2, 3, key = 1, lol = True)
	root.mainloop()