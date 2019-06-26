from lilylib import *
from lilylib import Chord as C
from lilylib import Note as N
from keys import *
from staves import *
from tempi import *

class vgs1(Manuscript):

	def __init__(self):
		super().__init__()
		self.title = "Venetianisches Gondellied"
		self.subtitle = "(Venetian Gondola Song)"
		self.composer = "Felix Mendelssohn"
		self.opus = "Op. 19, No. 6"
		self.key = GMinor()

		self.staves = [Treble("rh"), Bass("lh")]
		self.tempo = t68()
		self.create_sections(["intro", "octaves"])

		R = self.rest
		LH = self.LH

		self.sections["intro"].score["rh"] = [R("2.")]*2
		self.sections["intro"].score["lh"] = LH()*3 + LH(b=C([N('g'), N('a'), N("c'")]), c=N('ef'))

		self.sections["octaves"].score["rh"] = [N("d'", duration="4."), N("f'"), R(), N("ef'")]
		self.sections["octaves"].score["lh"] = []

		print(self)

	def LH(self, a=N('g,'), b=None, c=N('d')):
		if b is None:
			b = self.interval(N('g'), 2)
		return self.rhythm(8, [a, b, c])
		

vgs1()