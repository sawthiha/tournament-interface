import tkinter as tk
import tkinter.ttk as ttk

import sys
sys.path.append('../')

import ui.tools as tools
import config.ui_config as config

if __name__ == '__main__':
	root = tk.Tk()
	tagbar = tools.tag_bar(root)
	tagbar.panel.grid(row = 0, column = 0, sticky = tk.NSEW)
	tagbar.add('Hello')
	tagbar.add('Ha')
	tagbar.add('Foo')
	root.mainloop()
	#print(tagbar.tags[1].text())