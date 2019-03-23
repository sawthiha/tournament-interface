import pynsist
import controller.file as file

PYNIST_PKGS = 'pynsist_pkgs'

LOCAL_PKGS = ('config', 'controller', 'model', 'ui')

def fetch_pkgs():
	'''
		Copy local namespaces to pynsist_pkgs
		* The build process wasn't bothered of copying the top local namespace pkgs
		so have to copy them yourself to pynsist_pkgs
	'''
	file.replaceall2(LOCAL_PKGS, PYNIST_PKGS)

if __name__ == '__main__':
	fetch_pkgs()
	pynsist.main(config_file = 'installer.cfg')