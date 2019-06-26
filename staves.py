from lilylib import Stave

class Treble(Stave):

	def __init__(self, name=None):
		self.type = "treble"
		super().__init__(name)


class Bass(Stave):

	def __init__(self, name=None):
		self.type = "bass"
		super().__init__(name)
		