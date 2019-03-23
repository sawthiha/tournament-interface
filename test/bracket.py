import pandas as pd

import sys
sys.path.append('../')

import model.color as color

data = pd.read_csv('../resource/history/T042/Final.csv', index_col = 0)

class Bracket:
	def __init__(self, groups):
		self.groups = groups
		self.iter = 0

	def group(self):
		return self.groups[self.iter]

	def reload(self, data):
		self.groups = Group.TIE_fighter(data)

	def update(self, data):
		list(map(lambda group: group.update(data) , self.groups))

	def __len__(self):
		return self.groups[self.iter].__len__()

	def __next__(self):
		try:
			group = self.groups[self.iter + 1]
			self.iter += 1
			return group
		except IndexError:
			return None

	def next(self):
		return self.__next__()

	def highlights(self):
		return [group.highlight() for group in self.groups]

	def copy(self):
		return self.groups[self.iter].copy()

	@classmethod
	def bracket(cls, data):
		groups = Group.TIE_fighter(data)
		return cls(groups)

class Group:
	def __init__(self, sub, colour):
		self.subs = [sub]
		self.colour = colour

	def __len__(self):
		try:
			return len(self.subs[0])
		except IndexError:
			return 0

	def get(self):
		try:
			return self.subs[0]
		except IndexError:
			return []

	def update(self, data):
		group = self.get()
		subs = self.analyze_tie(data, idx = group)
		if group:
			self.subs.remove(group)
		list(map(lambda sub : self.subs.insert(0, sub), subs))	

	def all(self):
		return [itm for sub in self.subs for itm in sub]

	def highlight(self):
		return self.all(), self.colour

	def copy(self):
		return copy.deepcopy(self)

	@classmethod
	def TIE_fighter(cls, data):
		groups = cls.analyze_tie(data)
		color_map = color.highlightmap()
		colours = [color_map.get() for idx in range(0, len(groups))]
		return [cls(group, colour) for group, colour in zip(groups, colours)]

	@staticmethod
	def analyze_tie(data, idx = None):
		try:
			df = data.iloc[idx]
			counts = df.groupby(['Total', 'TB']).size()
		except TypeError:
			df = data
			counts = df.groupby(['Total', 'TB']).size()
		counts = counts[counts > 1]
		groups = []
		for entry in counts.index:
			logic = (df['Total'] == entry[0]) & (df['TB'] == entry[1])
			groups.append(list(map(data.index.get_loc, df.index[logic])))
		groups.reverse()
		return groups

bracket = Bracket.bracket(data)
print(bracket.group().get())
idx33 = [0, 1]
idx35 = [2, 3]
data.iloc[idx33, -1] = 33
data.iloc[idx35, -1] = 35
bracket.update(data)
print(bracket.group().get())
idx3 = [0, 2]
idx2 = [1, 3]
data.iloc[idx3, -1] = 3
data.iloc[idx2, -1] = 2
bracket.update(data)
bracket.update(data)
print(bracket.group().get())
''' Next '''
bracket.next()
print(bracket.group().get())
idx3 = [4]
idx2 = [5]
data.iloc[idx3, -1] = 3
data.iloc[idx2, -1] = 2
bracket.update(data)
print(bracket.group().get())
print(bracket.next())