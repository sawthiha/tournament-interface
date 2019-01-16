import sys
import pandas as pd
import pandastable as pt
import configparser as config
import parse

if __name__ == '__main__':
	print(sys.version)
	print('pandas', pd.__version__)
	print('pandastable', pt.__version__)
	print('parse', parse.__version__)