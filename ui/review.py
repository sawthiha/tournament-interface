import tkinter as tk
import tkinter.ttk as ttk

import ui.tools as tools

class Review:
	def __init__(self, root, varPhoto, varPos, varName, lblPhoto, lblPhoto_, lblPos, lblPos_, lblName, txtName, table, layoutTable, btnConfirm, btnBan):
		self.root = root
		self.varPhoto = varPhoto
		self.varPos = varPos
		self.varName = varName
		self.lblPhoto = lblPhoto
		self.lblPhoto_ = lblPhoto_
		self.lblPos = lblPos
		self.lblPos_ = lblPos_
		self.lblName = lblName
		self.txtName = txtName
		self.table = table
		self.layoutTable = layoutTable
		self.btnConfirm = btnConfirm
		self.btnBan = btnBan
		self.__config()
		self.__load()
	
	def __config(self):
		tools.resizeTableByParent(self.root, self.table, weight_y = 0.7)
		tools.autoResizeTableCells(self.table)
		self.table.redraw()

	def __load(self):
		self.lblPhoto.grid(row = 1, column = 1, sticky = tk.E, padx = 10, pady = 5)
		self.lblPhoto_.grid(row = 1, column = 2, sticky = tk.W, padx = 10, pady = 5)
		self.lblPos.grid(row = 1, column = 3, sticky = tk.E, padx = 10, pady = 5)
		self.lblPos_.grid(row = 1, column = 4, sticky = tk.W, padx = 10, pady = 5)
		self.lblName.grid(row = 2, column = 1, columnspan = 2, sticky = tk.E, padx = 10, pady = 5)
		self.txtName.grid(row = 2, column = 3, columnspan = 2, sticky = tk.W, padx = 10, pady = 5)
		self.layoutTable.grid(row = 4, column = 1, columnspan = 4, rowspan = 2, pady = 5)
		self.table.grid(row = 1, column = 1)
		self.btnBan.grid(row = 7, column = 1, columnspan = 2, pady = 5)
		self.btnConfirm.grid(row = 7, column = 3, columnspan = 2, pady = 5)

	def destory(self):
		self.root.destroy()

def review(root, photo, pos, data):
	layout = ttk.Frame(root)
	varPhoto = tk.IntVar(layout, value = photo)
	varPos = tk.IntVar(layout, value = pos)
	varName = tk.StringVar(layout, value = 'Candidate Name')
	lblPhoto = ttk.Label(layout, text = 'Photo:')
	lblPhoto_ = tk.Label(layout, textvariable = varPhoto)
	lblPos = ttk.Label(layout, text = 'Position:')
	lblPos_ = tk.Label(layout, textvariable = varPos)
	lblName = ttk.Label(layout, text = 'Name')
	txtName = ttk.Entry(layout, textvariable = varName)
	layoutTable = ttk.Frame(layout)
	table = tools.table_cp(layoutTable, data)
	table.show()
	btnBan = ttk.Button(layout, text = 'Ban')
	btnConfirm = ttk.Button(layout, text = 'Confirm')
	review = Review(layout, varPhoto, varPos, varName, lblPhoto, lblPhoto_, lblPos, lblPos_, lblName, txtName, table, layoutTable, btnConfirm, btnBan)
	layout.grid(row = 1, column = 1, sticky = 'nsew')
	return review