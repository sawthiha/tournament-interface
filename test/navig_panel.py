import tkinter as tk
import tkinter.ttk as ttk

import sys
sys.path.append('../')

import config.ui_config as config

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

root = config.get_root()
pane = NavigationPane(root)
def onAction(event):
	print(pane.index(event.widget))
pane.add('Step 1', onAction)
pane.add('Step 2', onAction)
pane.add('Step 3', onAction)
pane.add('Step 5', onAction)
pane.add('TB 1', onAction)
pane.add('Step 2', onAction)
pane.add('Step 3', onAction)
pane.add('Step 5', onAction)
pane.add('TB 1', onAction)
pane.add('Step 2', onAction)
pane.add('Step 3', onAction)
pane.add('Step 5', onAction)
pane.add('TB 1', onAction)
pane.pack(side = tk.TOP, fill = tk.X, expand = True, padx = 10)
root.mainloop()
