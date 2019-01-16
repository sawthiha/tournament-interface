import tkinter as tk
import pandastable as pt

class History:
	def __init__(self, optProcess, optStep, opt):
		pass

def history(root, processes, ):
	frame = tk.Frame(root)
	varProcess = tk.StringVar()
	optProcess = tk.OptionMenu(frame, varProcess, *['f001', 'foo2', 'foo3'])
	optStep = tk.OptionMenu(frame, varStep, *[1, 3, 4, 5])
	table = pt.Table(frame)

if __name__ == '__main__':
	pass