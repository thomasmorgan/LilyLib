from lilylib import Key

class CMajor(Key):
	def __init__(self):
		super().__init__()
		self.letters = ['c', 'd', 'e', 'f', 'g', 'a', 'b']
		self.name = "c major"
		self.filter_notes()

class DMajor(Key):
	def __init__(self):
		super().__init__()
		self.letters = ['cs', 'd', 'e', 'fs', 'g', 'a', 'b']
		self.name = "d major"
		self.filter_notes()

class EMajor(Key):
	def __init__(self):
		super().__init__()
		self.letters = ['cs', 'ds', 'e', 'fs', 'gs', 'a', 'b']
		self.name = "e major"
		self.filter_notes()

class FMajor(Key):
	def __init__(self):
		super().__init__()
		self.letters = ['c', 'd', 'e', 'f', 'g', 'a', 'bf']
		self.name = "f major"
		self.filter_notes()

class GMajor(Key):
	def __init__(self):
		super().__init__()
		self.letters = ['c', 'd', 'e', 'fs', 'g', 'a', 'b']
		self.name = "g major"
		self.filter_notes()

class AMajor(Key):
	def __init__(self):
		super().__init__()
		self.letters = ['cs', 'd', 'e', 'fs', 'gs', 'a', 'b']
		self.name = "a major"
		self.filter_notes()

class BMajor(Key):
	def __init__(self):
		super().__init__()
		self.letters = ['cs', 'ds', 'e', 'fs', 'gs', 'as', 'b']
		self.name = "b major"
		self.filter_notes()

class CMinor(Key):
	def __init__(self):
		super().__init__()
		self.letters = ['c', 'd', 'ef', 'f', 'g', 'af', 'b']
		self.name = "c minor"
		self.filter_notes()

class DMinor(Key):
	def __init__(self):
		super().__init__()
		self.letters = ['c', 'd', 'e', 'f', 'g', 'a', 'bf']
		self.name = "g minor"
		self.filter_notes()

class DMinorH(Key):
	def __init__(self):
		super().__init__()
		self.letters = ['cs', 'd', 'e', 'f', 'g', 'a', 'bf']
		self.name = "g minor"
		self.filter_notes()

class GMinor(Key):
	def __init__(self):
		super().__init__()
		self.letters = ['c', 'd', 'ef', 'f', 'g', 'a', 'bf']
		self.name = "g minor"
		self.filter_notes()

class GMinorH(Key):
	def __init__(self):
		super().__init__()
		self.letters = ['c', 'd', 'ef', 'fs', 'g', 'a', 'bf']
		self.name = "g minor"
		self.filter_notes()