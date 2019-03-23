import controller.control_main as control
import config.ui_config as config
import tkinter as tk
import tkinter.ttk as ttk

class Main:
	def __init__(self, root, header, content, footer, background, lblTitle, panBtns, btnCreate, btnHistory, btnSetting, btnAbout, lblNote):
		self.root = root
		self.header = header
		self.content = content
		self.footer = footer
		self.background = background
		self.lblTitle = lblTitle
		self.panBtns = panBtns
		self.btnCreate = btnCreate
		self.btnHistory = btnHistory
		self.btnSetting = btnSetting
		self.btnAbout = btnAbout
		self.lblNote = lblNote

		self.__config()
		self.__load()

	def __config(self):
		self.header.config(borderwidth=1, relief='solid')
		self.content.config(borderwidth=1, relief='solid')
		self.footer.config(borderwidth=1, relief='solid')

		self.lblTitle.config(font=('Arial', 24,'bold'))

		self.panBtns.config(borderwidth=1, relief='solid')
		self.btnCreate['style'] = 'Main.TButton'
		self.btnHistory['style'] = 'Main.TButton'
		self.btnSetting['style'] = 'Main.TButton'
		self.btnAbout['style'] = 'Main.TButton'

	def __load(self):
		self.header.pack(fill=tk.BOTH)
		self.content.pack(fill=tk.BOTH, expand=True)
		self.footer.pack(fill=tk.X)
		self.lblTitle.pack(pady = 20, fill=tk.BOTH, expand=True)
		self.panBtns.pack(side=tk.LEFT, fill=tk.Y)
		self.btnCreate.pack(padx=40, pady=10, anchor='center')
		self.btnHistory.pack(padx=40, pady=10, anchor='center')
		self.btnSetting.pack(padx=40, pady=10, anchor='center')
		self.btnAbout.pack(padx=40, pady=10, anchor='center')
		self.lblNote.pack()

def main(root):
	background = tk.PhotoImage(file = config.logo_url)
	layout = ttk.Label(root, image = background)
	header = ttk.Frame(layout, bg = None)
	content = ttk.Frame(layout)
	footer = ttk.Frame(layout)
	
	lblTitle = ttk.Label(header, text = config.main['title'])
	panBtns = ttk.Frame(content)

	btnCreate = ttk.Button(panBtns, text='New Competition', command = lambda : control.create(root))
	btnHistory = ttk.Button(panBtns, text='History')
	btnSetting = ttk.Button(panBtns, text='Setting')
	btnAbout = ttk.Button(panBtns, text='About us', command = lambda : control.about(root))

	lblNote = ttk.Label(footer, text='Python Inside!')

	layout.grid(row = 0, column = 0, sticky = 'nsew')
	return Main(layout, header, content, footer, background, lblTitle, panBtns, btnCreate, btnHistory, btnSetting, btnAbout, lblNote)