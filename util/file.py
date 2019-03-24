import shutil
import errno
import os
import os.path as path

def copy(src, dest):
	''' 
		Copy file/folder as dest
		* Need for copy2()
	 '''
	try:
		shutil.copytree(src, dest)
	except OSError as e:
		# If src is a file
		if e.errno == errno.ENOTDIR:
			shutil.copy(src, dest)
		else:
			print('src was not copied! Error %s' % e)

def copy2(src, dest):
	''' 
		Copy file/folder into dest
		* Need for copyall2()
	 '''
	dest_path = path.join(dest, src)
	copy(src, dest_path)

def copyall2(srcs, dest):
	'''
		Copy all file/folder into dest
		* Need to copy namespace packages to pynsist_pkgs/
	 '''
	for src in srcs:
		copy2(src, dest)

def searchdir(dir, dest):
	'''
		Search for the folder dir in dest folder
		Return relative path to dir else ''
		* Need for replace folder
	 '''
	for root, dirs, files in os.walk(dest):
		return path.join(root, dir) if dir in dirs else ''

def rmdir(dir):
	try:
		shutil.rmtree(dir)
	except OSError as e:
		print('dir could not be removed! Error %s' % e)

def replace2(src, dest):
	dir = searchdir(src, dest)
	if dir:
		rmdir(dir)
	copy2(src, dest)

def replaceall2(srcs, dest):
	for src in srcs:
		replace2(src, dest)
