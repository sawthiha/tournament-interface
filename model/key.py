import sys
sys.path.append('../')

import config.key_config as config

SWITCH_ON = 1
SWITCH_OFF = 0

MODE = [[0, 1], [2, 3, 4]]
MODE_1 = 0
MODE_2 = 1

class Key:
	__slots__ = 'parent', 'key', 'value', 'states', 'state'

	def __init__(self, key, value, on, off):
		self.parent = None
		self.key = key
		self.states = [off, on]
		self.state = SWITCH_OFF
		self.value = value

	def switch(self, state = SWITCH_OFF):
		self.state = state

	def check(self, key):
		return key.lower() == self.key

	def map(self, map):
		self.parent = map

	def __call__(self, value):
		self.states[self.state](self.parent, self.value, value)

class KeyMap:
	__slots__ = 'keys', 'activated', 'scheme', 'enabled'

	def __init__(self, keys, scheme = 0, enabled = True):
		self.keys = keys
		for group in keys.values():
			for key in group:
				key.map(self)
		self.scheme = scheme
		self.enabled = enabled
		self.activated = []

	def switch_mode(self, mode, state = SWITCH_ON):
		for group in self.keys.keys():
			for idx in MODE[mode]:
				self.keys[group][idx].switch(state)

	def reset(self, mode):
		self.switch_all(state = SWITCH_OFF)
		self.switch_mode(mode, state = SWITCH_ON)
		self.reset_activated()

	def reset_activated(self):
		self.activated = []

	def count(self):
		return len(self.keys) / 3

	def set_scheme(self, scheme = 0):
		self.scheme = scheme

	def disable(self, enabled = False):
		self.enabled = enabled

	def switch_group_offset(self, group, start,  stop, state = SWITCH_OFF):
		for key in self.keys[group][start:stop]:
			key.switch(state)

	def switch_group(self, group, state = SWITCH_OFF):
		for key in self.keys[group]:
			key.switch(state)

	def switch_all(self, state = SWITCH_ON):
		for group in self.keys.keys():
			self.switch_group(group, state = state)

	def switch_all_offset(self, start, stop, state = SWITCH_OFF):
		for group in self.key.keys():
			self.switch_group_offset(start, stop, group, state)

	def is_all_activated(self):
		status = True
		for group in self.keys.keys():
			status &= group in self.activated
		return status

	def __call__(self, key):
		if not self.enabled:
			return 

		for group in self.keys.keys():
			idx = 0
			n = len(self.keys[group])
			while idx < n:
				k = self.keys[group][idx]
				if k.check(key):
					k(config.SCHEME[self.scheme][idx])
					return
				idx += 1

def keymap(judges, on, off):
	k_map = {}
	keys = config.get_keys(judges)
	for judge, k_list in zip(keys.keys(), keys.values()):
		k_map[judge] = []
		idx = 0
		while idx < 5:
			k_map[judge].append(Key(k_list[idx], judge, on, off))
			idx += 1
	return KeyMap(k_map)

if __name__ == '__main__':
	keymap = keymap([str(i) for i in range(1, 3 + 1)], list(), dict())
	keymap.switch_mode(1)
	for group in keymap.keys:
		for key in keymap.keys[group]:
			print(key.state)