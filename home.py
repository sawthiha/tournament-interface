#!/usr/bin/env python3
import config.ui_config as config
import ui.main as main

root = config.get_root()
entry = main.main(root)
### TODO
# Ringtones ***
# Pick/Ban/Edit ***
# Select and Continue
# Each TB must show only its group
# Larger Font in Judge Label
# 

def main():
	root.mainloop()

if __name__ == '__main__':
	main()