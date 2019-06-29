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
		self.create_sections(["intro", "octaves", "in_d", "melody1", "melody2"])

		R = self.rest
		LH = self.LH
		LH_loop = self.LH_loop
		octave = self.octave
		interval = self.interval
		second = self.second
		third = self.third
		fourth = self.fourth
		third_b = self.third_b
		sixth_b = self.sixth_b
		rhythm = self.rhythm
		scale = self.scale
		descending_melody = self.descending_melody

		self.sections["intro"].score["rh"] = [R("2.")]*2
		self.sections["intro"].score["lh"] = LH()*3 + LH(b=C(['g', 'a', 'c`']), c='ef')

		self.sections["octaves"].score["rh"] = [N('d`', duration='4.'), N('f`', art="~"), N('f`'), N('ef`')]
		self.sections["octaves"].score["lh"] = LH(a=octave('g,,')) + LH(a=octave('f,,'), b=third('a'), c='f') + LH(a=octave('bf,,'), b=third('bf'), c='f') + LH(a=octave('c,'), b=C(['g', 'c`']), c='ef')

		self.sections["in_d"].score["rh"] = [N('d`', art="~"), N('d`'), R("2.")]
		self.sections["in_d"].score["lh"] = LH(a='d,')*2 + LH(a='d,', b=third('a')) + LH(a='d,', b=C(['fs', 'a']))

		self.sections["melody1"].score["rh"] = [R("4."), R("4")] + descending_melody()
		self.sections["melody1"].score["lh"] = LH_loop()

		self.sections["melody2"].score["rh"] = [N("d`", duration="4."), R("4")] + descending_melody()[0:7]
		self.sections["melody2"].score["lh"] = LH_loop()[0:18] + LH(b=third('bf'), c='g') + LH(b=second('bf', key=DMinorH()), c='g') + LH(a='f,', b=fourth('a'), c='f')*2 + LH(b=third('bf'), c='g') + LH(a='a,', b=N('cs`'), c='a') + LH(a='d', b=fourth('a'), c='f')*2

		print(self)

	def LH(self, a=N('g,'), b=None, c=N('d')):
		if isinstance(a, str):
			a = N(a)
		if isinstance(c, str):
			c = N(c)
		if b is None:
			b = self.third('g')
		return self.rhythm(8, [a, b, c])

	def LH_loop(self):
		return(
			self.LH()*2 + 
			self.LH(b=self.third('a'))*2 +
			self.LH()*2 +
			self.LH(b=self.fourth('g'), c='ef')*2
		)

	def descending_melody(self):
		melody = self.scale('d``', 'a`') + self.scale('c``', 'g`') + self.notes(['d`'] + ['ef`']*4)
		melody = self.rhythm([8, 4], self.sixth_b(melody[0:5], key=GMinorH()) + self.third_b(melody[5:8]) + [melody[8]] + self.sixth_b(melody[9:]))
		ornament = self.rhythm([16, 16, 8], self.sixth_b(self.notes(['ef`', 'f`', 'g`'])))
		melody[-2:-1] = ornament
		return melody
		

vgs1()