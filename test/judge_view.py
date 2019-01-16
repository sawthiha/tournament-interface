import pandas as pd
import time
import tkinter as tk
import tkinter.ttk as ttk

import sys
sys.path.append('../')

import ui.judge as judge
import config.ui_config as config

root = config.get_root()

def main(root):
	data = pd.read_csv('T1F1.csv')
	title = 'Foo'
	stage = 'Step 1'
	cur_candidate = 1
	judges = list(map(str, range(1, 3 + 1)))
	pause = lambda caller: print('pause')
	remain = 99
	judge_view = judge.judge(root, title, stage, cur_candidate, judges, pause, remain)
	judge_view[0] = 10
	judge_view[1] = 10
	judge_view[2] = 10
	judge_view.sum(30, True, is_valid = False)
	judge_view.reset_score()
	judge_view.update(stage, 2, 2, 5, 1, 1)
	judge_view.status(1, 5, True, True)

if __name__ == '__main__':
	main(root)
	root.mainloop()
