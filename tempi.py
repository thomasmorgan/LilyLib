from models import Tempo

class t68(Tempo):

	def __init__(self):
		self.name = "6/8"

	def __repr__(self):
		return "\\time {}\n".format(self.name)