#!/usr/bin/env python3
import config.ui_config as config
import ui.main as main
import controller.control_main as control

root = config.get_root()
entry = main.Main.instance(root, create = control.create, history = control.history, settings = control.settings, about = control.about)

def main():
	root.mainloop()

if __name__ == '__main__':
	main()