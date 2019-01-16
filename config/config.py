import configparser as cp

config = cp.ConfigParser()
# Package
#config.read('../config.ini')
# Home
config.read('config.ini')

default = config['DEFAULT']