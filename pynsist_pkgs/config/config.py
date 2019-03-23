import configparser as cp
import sys
import os
import os.path as path

root_dir = path.dirname(sys.modules['__main__'].__file__)

def from_root(url):
	return path.join(root_dir, url)

config = cp.ConfigParser()
# Package
#config.read('../config.ini')
# Home
config.read(from_root('config.ini'))

default = config['DEFAULT']