class CandidateManpl:
	def __init__(self, candidates):
		self.candidates = list(candidates)
		self.iterator = 0

	def get(self):
		return self.candidates[self.iterator]

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
		return self.__next__()

	def previous(self):
		raise NotImplementedError()

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


candidates = CandidateManpl([1, 2, 3])
candidates.append([4, 5])
if len(candidates) != 5:
	raise ValueError('append() failed!')
candidates.next()
if candidates.get() != 2:
	raise ValueError('next() failed!')
candidates.next()
candidates.next()
candidates.next()
if candidates.next() != -1:
	raise IndexError('next() failed!')

candidates.append([10])
if candidates.get() != 10:
	raise IndexError()

if candidates.reindex(0) == -1:
	raise IndexError('reindex() Failed!')

if candidates.relocate(2) == -1:
	raise IndexError('relocate() Failed!')