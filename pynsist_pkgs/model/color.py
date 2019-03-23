import config.config as config

class ColorMap:
	__slots__ = 'colors', 'valid', 'banned', 'iterator'
	def __init__(self, colors, valid = '#00ff00', banned = '#ff0000',):
		self.colors = colors
		self.banned = banned
		self.valid = valid
		self.colors.reverse()
		self.iterator = len(self.colors) - 1

	def get(self):
		try:
			if self.iterator < 0:
				self.iterator = len(self.colors) - 1
			color =  self.colors[self.iterator]
			self.iterator -= 1
			return color
		except IndexError:
			return '#ffffff'

	def get_banned(self):
		return self.banned

	def get_valid(self):
		return self.valid

def colormap(colors):
	clrs = ColorMap(colors)
	return clrs

def highlightmap():
	clrs = ColorMap(config.default['Highlights'].split(','), config.default['Valid'], config.default['Banned'])
	return clrs