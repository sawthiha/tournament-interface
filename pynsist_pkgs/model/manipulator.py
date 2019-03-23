class CandidateManpl:
	def __init__(self, candidates):
		self.candidates = candidates
		self.iterator = 0

	def get(self):
		try:
			return self.candidates[self.iterator]
		except IndexError:
			return -1

	def __next__(self):
		try:
			candidate = self.candidates[self.iterator + 1]
			self.iterator += 1
			return candidate
		except IndexError:
			return -1

	def __len__(self):
		return self.candidates.__len__()

	def next(self):
		idx = self.__next__()
		return self.get() if idx < 0 else idx

	def previous(self):
		idx = self.iterator - 1
		if idx < 0:
			pass
		else:
			self.iterator -= 1
		return self.get()

	def relocate(self, candidate):
		try:
			self.iterator = self.candidates.index(candidate)
			return self.get()
		except ValueError:
			return -1

	def reindex(self, idx):
		try:
			candidate = self.candidates[idx]
			self.iterator = idx
			return candidate
		except IndexError:
			return -1

	def append(self, candidates):
		self.candidates.extend(candidates)

	def insert(self, candidates):
		offset = self.iterator + 1
		self.candidates = self.candidates[:offset] + candidates + self.candidates[offset:]

	def candidate_list(self):
		return self.candidates.copy()

	@classmethod
	def instance(cls, candidates):
		return cls(candidates)