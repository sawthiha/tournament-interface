import tkinter as tk
import tkinter.ttk as ttk
import pandastable as pt

class Spinbox(ttk.Entry):
	def __init__(self, master = None, **kw):
		ttk.Entry.__init__(self, master, 'ttk::spinbox', **kw)

	def set(self, value):
		self.tk.call(self._w, 'set', value)

class PromptCreate:
	def __init__(self, root, lblTitle, txtTitle, varTitle, lblPhotos, txtPhotos, varPhotos, warnPhotos, lblJudges, btnJudges, varJudges, btnCreate, varCandidates, lblCandidates, txtCandidates, varStep, lblStep, btnStep, tags, txtJudges, btnAdd):
		self.root = root
		self.lblTitle = lblTitle
		self.txtTitle = txtTitle
		self.varTitle = varTitle
		self.lblPhotos = lblPhotos
		self.txtPhotos = txtPhotos
		self.varPhotos = varPhotos
		self.lblCandidates = lblCandidates
		self.txtCandidates = txtCandidates
		self.varCandidates = varCandidates
		self.warnPhotos = warnPhotos
		self.lblJudges = lblJudges
		self.btnJudges = btnJudges
		self.varJudges = varJudges
		self.varStep = varStep
		self.lblStep = lblStep
		self.btnStep = btnStep
		self.btnCreate = btnCreate
		self.tags = tags
		self.txtJudges = txtJudges
		self.btnAdd = btnAdd
		self.btnCreate = btnCreate

		self.__config()
		self.__load()

	def __config(self):
		self.txtTitle.config(width = 20)
		self.txtPhotos.config(width = 20)

	def __load(self):
		self.lblTitle.grid(row = 0, column = 0, padx = 5, pady = 5)
		self.txtTitle.grid(row = 0, column = 1, padx = 5, pady = 5)
		self.warnPhotos.grid(row = 1, column = 0, columnspan = 2, sticky = 'e')
		self.lblCandidates.grid(row = 2, column = 0, padx = 5, pady= 10)
		self.txtCandidates.grid(row = 2, column = 1, padx = 5, pady= 10)
		self.lblPhotos.grid(row = 3, column = 0, padx = 5, pady= 10)
		self.txtPhotos.grid(row = 3, column = 1, padx = 5, pady= 10)
		self.lblJudges.grid(row = 4, column = 0, padx = 5, pady= 10)
		self.btnJudges.grid(row = 4, column = 1, padx = 5, pady= 10)
		self.tags.grid(row = 5, column =0, columnspan = 2)
		self.txtJudges.grid(row = 6, column = 0)
		self.btnAdd.grid(row = 6, column = 1)
		self.btnStep.grid(row = 7, column = 0, padx = 5, pady= 10)
		self.btnCreate.grid(row = 7, column = 1, padx = 5, pady= 10)
		self.warnPhotos.grid_remove()

	def destory(self):
		self.root.destroy()

	def warn(self, show = True):
		if show:
			self.warnPhotos.grid()
		else:
			self.warnPhotos.grid_remove()

def promptcreate(root, create, logic, decor_save_judge):
	window = tk.Toplevel(root)
	window.wm_title('Create a tournament')
	window.geometry('%dx%d+%d+%d' % (500, 400, 250, 125))
	window.grid_anchor(tk.CENTER)
	
	varTitle = tk.StringVar(window, value = 'Tournament Title')
	varCandidates = tk.IntVar(window)
	varPhotos = tk.IntVar(window)
	varJudges = tk.IntVar(window, value = 5)
	varStep = tk.IntVar(window, value = 1)
	lblTitle = ttk.Label(window, text = 'Title')
	txtTitle = ttk.Entry(window, textvariable = varTitle)
	lblCandidates = ttk.Label(window, text = 'Candidates')
	txtCandidates = ttk.Entry(window, textvariable = varCandidates)
	lblPhotos = ttk.Label(window, text = 'No of Photos')
	txtPhotos = ttk.Entry(window, textvariable = varPhotos)
	warnPhotos = ttk.Label(window, text = 'Invalid Input!')
	
	lblJudges = ttk.Label(window, text = 'No of Judges')
	btnJudges = ttk.Frame(window)
	j3 = ttk.Radiobutton(btnJudges, text = '3', variable = varJudges, value = 3)
	j5 = ttk.Radiobutton(btnJudges, text = '5', variable = varJudges, value = 5)
	j7 = ttk.Radiobutton(btnJudges, text = '7', variable = varJudges, value = 7)
	for btn in (j3, j5, j7):
		btn.pack(padx = 10, side = tk.LEFT)
	
	btnStep = ttk.Frame(window)
	lblStep = ttk.Label(btnStep, text = 'Start Step')
	s1 = ttk.Radiobutton(btnStep, text = '1', variable = varStep, value = 1)
	s2 = ttk.Radiobutton(btnStep, text = '2', variable = varStep, value = 2)
	s3 = ttk.Radiobutton(btnStep, text = 'Final', variable = varStep, value = 0)
	for btn in (lblStep, s1, s2, s3):
		btn.pack(padx = 10, side = tk.LEFT)
	
	btnCreate = ttk.Button(window, text = 'Start')
	
	tags = TagBar(window)
	varName = tk.StringVar(window)
	txtJudges = AutoEntry(logic, window, textvariable = varName)
	
	@decor_save_judge
	def onClick(text):
		tags.add(text, limit = varJudges.get())

	btnAdd = ttk.Button(window, text = 'Choose', command = lambda:onClick(varName.get()))
	
	prompt = PromptCreate(window, lblTitle, txtTitle, varTitle, lblPhotos, txtPhotos, varPhotos, warnPhotos, lblJudges, btnJudges, varJudges, btnCreate, varCandidates, lblCandidates, txtCandidates, varStep, lblStep, btnStep, tags, txtJudges, btnAdd)
	btnCreate.configure(command = lambda : create(prompt))

class PromptAbout:
	def __init__(self, root, lblAbout):
		self.root = root
		self.lblAbout = lblAbout
		self.__config()
		self.__load()

	def __config(self):
		pass

	def __load(self):
		self.lblAbout.grid(row = 0, column = 0)

def promptabout(root):
	window = tk.Toplevel(root)
	window.wm_title('About')
	window.geometry('%dx%d+%d+%d' % (300, 200, 250, 125))
	window.grid_anchor(tk.CENTER)
	lblAbout = ttk.Label(window , text = 'Not Supported yet!')
	prompt = PromptAbout(window, lblAbout)

def table_cp(parent, data):
	return pt.Table(parent, dataframe = data.drop('Penalty', axis = 1))

def cellalign(table, align = 'center'):
	table.align = align

def unbind(table, *args):
	for arg in args:
		table.unbind(arg)

def rowSelectedColor(table, color = None):
	table.rowselectedcolor = color

def tableFont(table, font = 'Aerial', size = 14, weight = 'bold'):
	table.thefont = (font, size, weight)

def expandTableCols(table, width):
	table.cellwidth = width
	widths = table.model.columnwidths
	for c in widths:
		widths[c] = width

def expandTableColsByTable(table):
	n_cols = len(table.model.df.columns)
	relative_width =  int(table['width']) / n_cols
	expandTableCols(table, relative_width)

def autoResizeTableCells(table, height = 40):
	expandTableColsByTable(table)
	table.setRowHeight(height)

def resizeTableByParent(root, table, weight_x = 0.95, weight_y = 0.8):
	table.config(width = root.winfo_screenwidth() * weight_x, height = root.winfo_screenheight() * weight_y)

class StatusBar(ttk.Frame):
	def __init__(self, varStep, varTotal, varProgress, varDrop, varPass, varPhoto, font_, highlights,*args, **kwargs):
		ttk.Frame.__init__(self, *args, **kwargs)

		self.varStep = varStep
		self.varTotal = varTotal
		self.varProgress = varProgress
		self.varDrop = varDrop
		self.varPass = varPass
		self.varPhoto = varPhoto
		
		self.lblStep = ttk.Label(self, textvariable = varStep, style = 'Status.TLabel')

		self.lblPhoto = ttk.Label(self, text = 'Photo No.', style = 'Status.TLabel')
		self.lblPhoto_ = ttk.Label(self, textvariable = varPhoto, style = 'Status.TLabel')

		self.lblTotal = ttk.Label(self, textvariable = varTotal, style = 'Status.TLabel')
		self.lblPer = ttk.Label(self, text = '/', style = 'Status.TLabel')
		
		self.lblProgress = ttk.Label(self, textvariable = varProgress, style = 'Status.TLabel')

		
		self.lblDrop = ttk.Label(self, textvariable = varDrop, style = 'Status.Banned.TLabel')
		self.lblPass = ttk.Label(self, textvariable = varPass, style = 'Status.Valid.TLabel')
		self.__config()
		self.__load()

	def __config(self):
		self.lblStep['anchor'] = tk.CENTER
		self.lblPhoto['anchor'] = tk.E
		self.lblDrop['anchor'] = tk.CENTER
		self.lblPass['anchor'] = tk.CENTER

	def __load(self):
		self.lblStep.pack(fill = tk.X, side = tk.LEFT, expand = True)
		self.lblDrop.pack(fill = tk.X, side = tk.LEFT, expand = True)
		self.lblPass.pack(fill = tk.X, side = tk.LEFT, expand = True)
		self.lblPhoto.pack(fill = tk.X, side = tk.LEFT, expand = True)
		self.lblPhoto_.pack(fill = tk.X, side = tk.LEFT, expand = True)
		self.lblProgress.pack(fill = tk.X, side = tk.LEFT)
		self.lblPer.pack(fill = tk.X, side = tk.LEFT)
		self.lblTotal.pack(fill = tk.X, side = tk.LEFT, expand = True)

	def remove_all(self):
		self.lblStep.pack_forget()
		self.lblDrop.pack_forget()
		self.lblPass.pack_forget()
		self.lblPhoto.pack_forget()
		self.lblPhoto_.pack_forget()
		self.lblProgress.pack_forget()
		self.lblPer.pack_forget()
		self.lblTotal.pack_forget()

	def mode_score(self):
		self.remove_all()
		self.lblStep.pack(fill = tk.X, side = tk.LEFT, expand = True)
		self.lblDrop.pack(fill = tk.X, side = tk.LEFT, expand = True)
		self.lblPass.pack(fill = tk.X, side = tk.LEFT, expand = True)
		self.lblTotal['anchor'] = tk.CENTER
		self.lblTotal.pack(fill = tk.X, side = tk.LEFT, expand = True)

	def mode_final(self):
		self.remove_all()
		self.lblStep.pack(fill = tk.X, side = tk.LEFT, expand = True)
		self.lblTotal['anchor'] = tk.CENTER
		self.lblTotal.pack(fill = tk.X, side = tk.LEFT, expand = True)

	def mode_judge(self):
		self.remove_all()
		self.__load()

	def mode_judge_final(self):
		self.remove_all()
		self.lblStep.pack(fill = tk.X, side = tk.LEFT, expand = True)
		self.lblPhoto.pack(fill = tk.X, side = tk.LEFT, expand = True)
		self.lblPhoto_.pack(fill = tk.X, side = tk.LEFT, expand = True)
		self.lblProgress.pack(fill = tk.X, side = tk.LEFT, expand = True)
		self.lblProgress['anchor'] = tk.E
		self.lblPer.pack(side = tk.LEFT)
		self.lblTotal['anchor'] = tk.W
		self.lblTotal.pack(fill = tk.X, side = tk.LEFT, expand = True)

	def update(self, step = None, photo = None, progress = None, total = None, drop = None, passed = None):
		if step != None:
			self.varStep.set(step)
		if total != None:
			self.varTotal.set(total)
		if progress != None:
			self.varProgress.set(progress)
		if drop != None:
			self.varDrop.set(drop)
		if passed != None:
			self.varPass.set(passed)
		if photo != None:
			self.varPhoto.set(photo)

def status_bar(root):
	invalid = '#ff1111'
	valid = '#11ff11'
	font_ = ('Aerial', 24, 'bold')
	varStep = tk.StringVar(value = 'N/A')
	varPhoto = tk.IntVar()
	varTotal = tk.IntVar()
	varProgress = tk.IntVar()
	varDrop = tk.IntVar()
	varPass = tk.IntVar()

	return StatusBar(varStep, varTotal, varProgress, varDrop, varPass, varPhoto, font_, (invalid, valid), root)

class TagBar(ttk.Frame):
	def __init__(self, *args, **kwargs):
		ttk.Frame.__init__(self, *args, **kwargs)
		self.tags = []
		self.__config()
		self.__load()

	def empty(self):
		if self.tags:
			return True
		else:
			return False

	def all(self):
		return [tag.text() for tag in self.tags]

	def add(self, text, limit = None):
		if limit and len(self.tags) >= limit:
			return
		obj = tag(self, text)
		self.tags.append(obj)
		obj.pack(padx = 10, side = tk.LEFT)

	def remove(self, obj):
		self.tags.remove(obj)

	def __config(self):
		pass

	def __load(self):
		pass

class Tag(ttk.Frame):
	def __init__(self, text, *args, **kwargs):
		ttk.Frame.__init__(self, *args, **kwargs)

		self.parent = args[0]

		self.lblText = ttk.Label(self, text = text)
		self.lblCancel = tk.Label(self, text = 'x', fg  = 'red')
		
		
		self.__config()
		self.__load()

	def __config(self):
		self.lblCancel.default_fg = 'red'
		self.lblCancel.bind('<Button-1>', lambda event : self.destroy())
		self.lblCancel.bind('<Enter>', self.onEnter)
		self.lblCancel.bind('<Leave>', self.onLeave)

	def __load(self):
		self.lblText.pack(side = tk.LEFT)
		self.lblCancel.pack(side = tk.LEFT)

	def onEnter(self, event):
		widget = event.widget
		widget['fg'] = 'blue'

	def onLeave(self, event):
		widget = event.widget
		widget['fg'] = widget.default_fg

	def text(self):
		return self.lblText['text']

	def destroy(self):
		self.parent.remove(self)
		super().destroy()
		self.parent = None

def tag(bar, text):
	tag_ = Tag(text, bar)
	return tag_

class AutoEntry(ttk.Entry):
	def __init__(self, logic, *args, **kwargs):
		ttk.Entry.__init__(self, *args, **kwargs)
		
		self.logic = logic
		self.likehood = self.logic('')
		self.iterator = 0
		self.var = kwargs['textvariable']
		
		self.__config()
		self.__load()
		self.__bind()

	def __config(self):
		pass

	def __load(self):
		pass

	def onUp(self, event):
		txt = self.var.get()
		if self.selection_present():
			txt = txt.replace(self.selection_get(), '')
		idx = len(txt)
		
		self.iterator = self.iterator - 1 if self.iterator > 0 else len(self.likehood) - 1
		self.var.set(self.likehood[self.iterator])
		self.select_range(idx, tk.END)

	def onDown(self, event):
		txt = self.var.get()
		if self.selection_present():
			txt = txt.replace(self.selection_get(), '')
		idx = len(txt)
		self.iterator = self.iterator + 1 if self.iterator < (len(self.likehood) - 1) else 0
		self.var.set(self.likehood[self.iterator])
		self.select_range(idx, tk.END)

	def onTab(self, event):
		self.onDown(event)
		return 'break'

	def onReturn(self, event):
		self.selection_clear()
		self.icursor(tk.END)

	def onChanged(self, event):
		if event.char == event.keysym or event.keysym == 'BackSpace':
			txt = self.var.get()
			likehood = self.logic(txt)
			idx = len(txt)
			self.likehood = [txt]
			self.likehood.extend(likehood)
			self.iterator = 0
			self.var.set(self.likehood[self.iterator])
			self.select_range(idx, tk.END)

	def __bind(self):
		self.bind('<Up>', self.onUp)
		self.bind('<Down>', self.onDown)
		self.bind('<Tab>', self.onTab)
		self.bind('<Return>', self.onReturn)
		self.bind('<KeyRelease>', self.onChanged)

def popupmenu(parent, logic, commands):
	menu = TablePopup(commands, parent)
	parent.bind('<Button-3>', lambda event: menu.pop(event, logic()))
	return menu

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