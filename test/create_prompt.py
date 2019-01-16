import tkinter as tk
import tkinter.ttk as ttk

import sys
sys.path.append('../')

import ui.tools as tools

if __name__ == '__main__':
	root = tk.Tk()
	tags = tools.TagBar(root)
	tags.add('Apk')
	tags.pack()
	root.mainloop()