import os, sys

PLATFORM = sys.platform


if PLATFORM.startswith('win'):
	import win32print as printer
elif PLATFORM.startswith('linux'):
	import subprocess
elif PLATFORM.startswith('dar'):
	raise NotImplementedError()
else:
	raise NotImplementedError()

class DefaultPrinter:
	def __init__(self, impl):
		self._impl = impl

	def raw_print(raw_data, description = "Raw Data"):
		self._impl.raw_print(raw_data, description)

	@classmethod
	def instance(cls):
		if PLATFORM.startswith('win'):
			impl = DefaultWinPrinter()
		elif PLATFORM.startswith('lin'):
			impl = DefaultLinPrinter()
		elif PLATFORM.startswith('dar'):
			raise NotImplementedError("Not Implemented for %s" % PLATFORM)
		else:
			raise NotImplementedError("Not Implemented for %s" % PLATFORM)
		return cls(impl)

class DefaultWinPrinter:
	def raw_print(self, raw_data, description = "Raw Data"):
		prtinterName = win32print.GetDefaultPrinter()
		printer = win32print.OpenPrinter(prtinterName)
		try:
			job = win32print.StartDocPrinter(printer, 1, (description, None, "RAW"))
			try:
				win32print.StartPagePrinter(printer)
				win32print.WritePrinter(printer, raw_data)
				win32print.EndPagePrinter(printer)
			finally:
				win32print.EndDocPrinter(printer)
		finally:
			win32print.ClosePrinter(printer)

class DefaultLinPrinter:
	def raw_print(self, raw_data, description = "Raw Data")
		args = ['/usr/bin/lpr', '-#', '1', '-T', description]
		lpr = subprocess.Popen(args, stdin = subprocess.PIPE)
		lpr = subprocess.stdin.write(raw_data)

DEFAULT_PRINTER = DefaultPrinter.instance()
