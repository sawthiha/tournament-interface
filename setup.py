from distutils.core import setup
import py2exe, sys, os

sys.argv.append('py2exe')

setup(windows=[{'script': 'home.py'}], \
			options={"py2exe": {"includes": ["decimal", "Tkinter", \
			"tkFileDialog", "csv", "xml.dom.minidom", "os"], \
			'bundle_files': 1, 'compressed': False}}, \
			zipfile = None)