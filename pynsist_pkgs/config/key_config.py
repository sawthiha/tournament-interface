import config.config as config

keys = config.config['KEY']

SCHEME = [(0, 1, 3, 5, 7)]

key_dict = {
	';' : 'semicolon'
}

def special_char(keys):
	for char, sym in zip(key_dict.keys(), key_dict.values()):
		for idx, val in enumerate(keys):
			if val == char:
				keys[idx] = sym
	return keys

def get_keys(judges):
	key_map = {}
	for judge in judges:
		key_map[judge] = special_char(keys[judge].replace(' ', '').split(','))
	return key_map