import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk

import sys
sys.path.append('../')

import config.ui_config as config
#import controller.control_main as control

class Main(tk.Canvas):
	def __init__(self, dependencies, *args, **kwargs):
		tk.Canvas.__init__(self, *args, **kwargs)
		dependencies(self)
		self.__config()
		self.__load()

	def __config(self):
		pass

	def __load(self):
		self.create_image(0, 0, image = self.bg_img, anchor = tk.NW)
		self.btns.pack(side = tk.BOTTOM, fill = tk.X)
		self.btnCreate.pack(side = tk.LEFT, fill = tk.X, expand = True)
		self.btnHistory.pack(side = tk.LEFT, fill = tk.X, expand = True)
		self.btnSettings.pack(side = tk.LEFT, fill = tk.X, expand = True)
		self.btnAbout.pack(side = tk.LEFT, fill = tk.X, expand = True)

	@classmethod
	def main(cls, root, *args, **kwargs):
		def dependencies(caller):
			screen_size = (root.winfo_screenwidth(), root.winfo_screenheight())
			caller.bg_img = ImageTk.PhotoImage(image = Image.open(config.background_url).resize(screen_size, Image.BICUBIC))
			caller.btns = ttk.Frame(caller)
			caller.btnCreate = ttk.Button(caller.btns, text = 'New Competition', style = 'Main.TButton', command = lambda : kwargs['create'](caller))
			caller.btnHistory = ttk.Button(caller.btns, text = 'History', style = 'Main.TButton', command = lambda : kwargs['history'](caller))
			caller.btnSettings = ttk.Button(caller.btns, text = 'Settings', style = 'Main.TButton', command = lambda : kwargs['settings'](caller))
			caller.btnAbout = ttk.Button(caller.btns, text = 'About', style = 'Main.TButton', command = lambda : kwargs['about'](caller))
		view = cls(dependencies, root)
		view.grid(row = 0, column = 0, sticky = tk.NSEW)
		return view

if __name__ == '__main__':
	root = config.get_root()
	view = Main.main(root)
	root.mainloop()
