import tkinter as tk
import tkinter.ttk as ttk

import sys
sys.path.append('../')

import config.ui_config as config

POP_BAN = 1
POP_PICK = 2
POP_EDIT = 4
class TablePopup(tk.Menu):
	def __init__(self, cmd_dict, *args, **kwargs):
		tk.Menu.__init__(self, *args, **kwargs, tearoff = 0)
		self.cmd_dict = cmd_dict
		self.lbl_dict = {
			POP_BAN : 'Ban',
			POP_PICK : 'Pick',
			POP_EDIT : 'Edit'
		}
		self.__config()
		self.__load()

	def __config(self):
		self.bind('<FocusOut>', lambda event: self.unpost())

	def unpost(self):
		super().unpost()
		for lbl in self.lbl_dict.values():
			try:
				self.delete(lbl)
			except tk.TclError:
				continue

	def pop(self, event, commands):
		try:
			for value in mask(commands, POP_BAN, POP_PICK, POP_EDIT):
				try:
					self.add_command(label = self.lbl_dict[value], command = self.cmd_dict[value])
				except KeyError:
					continue
			self.tk_popup(event.x_root, event.y_root)
		finally:
			self.grab_release()

	def __load(self):
		pass

def mask(value, *mask):
	for m in mask:
		yield value & m
root = config.get_root()
for idx in range(0, 5):
	ttk.Button(text = str(idx)).pack(side = tk.LEFT)
cmd_dict = {
	POP_BAN : lambda :print('Ban'),
	POP_PICK : lambda :print('Pick'),
	POP_EDIT : lambda :print('Edit')
}

pop = TablePopup(cmd_dict)
root.bind('<Button-3>', lambda event : pop.pop(event, POP_BAN + POP_EDIT))
root.mainloop()
#

