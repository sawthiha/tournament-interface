import model.color as color
import copy
import pandas as pd
COLORS = color.highlightmap()

THRESHOLD_REF = {3:13, 5:23, 7:33}

def decor_occurances(is_iloc):
	def decor_wrapper(func):
		def wrapper(df, threshold):
			candidates = []
			logic = df['Penalty'] == 0
			counts = df.loc[logic].groupby(['Total', 'TB']).size()
			counts = counts[counts > 1]
			counts.sort_index(ascending=False, inplace=True)
			for entry in counts.index:
				logic = (df['Total'] == entry[0]) & (df['TB'] == entry[1])
				group = df.index[logic]
				if df.index.get_loc(group[0]) >= threshold:
					break
				candidates.append(list(map(df.index.get_loc, group.tolist())) if is_iloc else group.tolist())
			return func(candidates)
		return wrapper
	return decor_wrapper

@decor_occurances(is_iloc = True)
def highlight_recaps(candidates):
	global COLORS
	for group in candidates:
		yield group, COLORS.get()

@decor_occurances(is_iloc = False)
def mode_recaps(candidates):
	bucket = []
	for group in candidates:
		mode = 1 if len(group) > 2 else 0
		bucket.extend([(candidate, mode) for candidate in group])
	return bucket

@decor_occurances(is_iloc = True)
def bracket(candidates):
	return candidates

@decor_occurances(is_iloc = False)
def all_recaps(candidates):
	return extract_recaps(candidates)

def extract_recaps(candidates):
	bucket = []
	for group in candidates:
		bucket.extend(group)
	return bucket

def bracket_check(data, bracket):
	counts = data.iloc[bracket].groupby(['Total', 'TB']).size()
	counts = counts[counts > 1]
	group = []
	for entry in counts.index:
		logic = (data['Total'] == entry[0]) & (data['TB'] == entry[1])
		group.extend(data.index[logic].tolist())
	return list(map(data.index.get_loc, group))

def validate(status):
	global COLORS
	return COLORS.get_banned() if status else COLORS.get_valid()

def invalid_candidates(df, threshold):
	global COLORS
	invalids = df.index[(df['Total'] + df['Penalty']) < threshold]
	candidates = [df.index.get_loc(candidate) for candidate in invalids], COLORS.get_banned()
	return candidates

def highlights(no):
	colors = color.highlightmap()
	return [colors.get() for idx in range(0, no)]

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
	def __init__(self, data):
		self.groups = bracket(data, len(data))
		self.colours = highlights(len(self.groups))
		self.group = 0 if self.groups else -1

	def __getitem__(self, key):
		return self.groups[self.group][key]

	def __len__(self):
		return len(self.groups[self.group])

	def reset(self, data):
		self.groups = bracket(data, len(data))
		self.colours = highlights(len(self.groups))
		self.group = 0 if self.groups else -1

	def update(self, data):
		self.groups[self.group] = bracket_check(data, self.groups[self.group])
		return self.get()

	def update_all(self, data):
		def replace(group):
			return bracket_check(data, group)
		self.groups = list(map(replace, self.groups))
		return self.get_zip()

	def count(self):
		return len(self.groups)

	def copy(self):
		return copy.deepcopy(self)

	def get(self):
		return self.groups[self.group]

	def get_zip(self):
		return list(zip(self.groups, self.colours))

	def next_group(self):
		try:
			group = self.groups[self.group + 1]
			self.group += 1
			return group
		except IndexError:
			return []