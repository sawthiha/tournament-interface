import tkinter as tk
import tkinter.font as font

import config.config as config

default = config.config['DEFAULT']
main = config.config['MAIN']
judge = config.config['JUDGE']
score = config.config['SCORE']

logo_url = config.from_root(main['logo_image'])
background_url = config.from_root(main['background_image'])

def style(root):
	style = tk.ttk.Style(root)
	style.theme_use(default['Ttk_Theme'])
	style.configure('Main.TButton', width = int(main['Button_Width']))
	style.configure('Judge.TLabel', font = judge['Judge_Label_Font'], background = root.cget('bg'))
	style.configure('Status.TLabelframe', relief = tk.SOLID, borderwidth = 2)
	style.configure('Status.TLabel', font = judge['Status_Font'], background = root.cget('bg'))
	style.configure('Status.Banned.TLabel', font = judge['Status_Font'], background = default['Banned'])
	style.configure('Status.Valid.TLabel', font = judge['Status_Font'], background = default['Valid'])
	style.configure('Judge.TFrame',borderwidth = 3, relief = tk.SOLID, background = root.cget('bg'))
	style.configure('Banned.TFrame', background = default['Banned'])
	style.configure('Valid.TFrame', background = default['Valid'])
	style.configure('Banned.TLabel', font = judge['Judge_Label_Font'], background = default['Banned'])
	style.configure('Valid.TLabel', font = judge['Judge_Label_Font'], background = default['Valid'])
	style.configure('board.tag.TButton', font = 'Helvatic 18', highlightthickness = (0, 0, 300, 0))
	style.map('board.tag.TButton',
			background = [
				('active', '#aaaaaa'),
				('focus', '#aaaaaa')
			],
			relief = [
				('pressed', 'groove'),
				('!pressed', 'ridge'),
				('focus', 'groove')
			]
		)

	root.style = style
	
	root.grid_anchor(tk.CENTER)
	root.columnconfigure(0, weight = 1)
	root.rowconfigure(0, weight = 1)
	root.unbind_class('Button', '<space>')
	root.unbind_class('TButton', '<space>')
	root.bind_class('Button', '<Key-Return>', lambda event: event.widget.invoke())
	root.bind_class('TButton', '<Key-Return>', lambda event: event.widget.invoke())

def get_root():
	root = tk.Tk()
	root.attributes('-fullscreen', True)
	style(root)
	return root
