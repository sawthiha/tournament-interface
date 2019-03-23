import model.color as color
import copy
import pandas as pd
import copy

COLORS = color.highlightmap()
THRESHOLD_REF = {3:13, 5:23, 7:33}

def invalid_candidates(df, threshold):
	global COLORS
	invalids = df.index[(df['Total'] + df['Penalty']) < threshold]
	candidates = [df.index.get_loc(candidate) for candidate in invalids], COLORS.get_banned()
	return candidates

def threshold(no, nJudges):
	if no == 1:
			t = int(nJudges / 2) + 1
	else:
		t = THRESHOLD_REF[nJudges]
		idx = 2
		while idx < no:
			t += 2
			idx += 1
	return t

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
		subs.reverse()
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