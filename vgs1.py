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
		O = self.octave
		interval = self.interval
		second = self.second
		third = self.third
		third_b = self.third_b
		fourth = self.fourth
		sixth_b = self.sixth_b
		rhythm = self.rhythm
		scale = self.scale
		notes = self.notes
		descending_melody = self.descending_melody
		wandering_melody = self.wandering_melody

		self.sections["intro"].score["rh"] = R("2. 2.")
		self.sections["intro"].score["lh"] = LH()*3 + LH(b=C('g a c`'), c='ef')

		self.sections["octaves"].score["rh"] = [N('d`', dur='4.'), N('f`', art="~"), N('f`'), N('ef`')]
		self.sections["octaves"].score["lh"] = LH(a=O('g,,')) + LH(a=O('f,,'), b=third('a'), c='f') + LH(a=O('bf,,'), b=third('bf'), c='f') + LH(a=O('c,'), b=C('g c`'), c='ef')

		self.key = GMinorH()
		self.sections["in_d"].score["rh"] = [N('d`', art="~"), N('d`')] + R("2.")
		self.sections["in_d"].score["lh"] = LH('d,')*2 + LH('d,', third('a')) + LH('d,', third('fs'))

		self.sections["melody1"].score["rh"] = R("4. 4") + descending_melody()
		self.sections["melody1"].score["lh"] = LH_loop()

		self.sections["melody2"].score["rh"] = [N("d`", dur="4.")] + R("4") + descending_melody()[0:7]
		self.sections["melody2"].score["lh"] = LH_loop()[0:15]

		self.key = DMinorH()
		self.sections["melody2"].score["rh"] += wandering_melody()
		self.sections["melody2"].score["lh"] += LH_loop()[15:18] + LH('g,', third('bf'), 'g') + LH('g,', second('bf', key=DMinorH()), 'g') + LH('f,', fourth('a'), 'f')*2 + LH('g,', third('bf'), 'g') + LH('a,', N('cs`'), 'a') + LH('d', fourth('a'), 'f')*2

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
		melody = self.scale('d``', 'a`') + self.scale('c``', 'g`') + self.notes('d` ' + 'ef` '*4)
		melody = self.rhythm([8, 4], self.sixth_b(melody[0:5]) + self.third_b(melody[5:8]) + [melody[8]] + self.sixth_b(melody[9:]))
		
		self.key = GMinor()
		ornament = self.rhythm([16, 16, 8], self.sixth_b(self.notes('ef` f` g`')))
		melody[-2:-1] = ornament
		self.key = GMinorH()
		return melody

	def wandering_melody(self):
		def basic_scale():
			return self.rhythm([8], self.scale('g`', 'd``') + self.scale('f``', 'd``'))
		first_pass = [self.third_b('g`')] + basic_scale() + self.rhythm([4, 8], self.notes('a`` f`` d``'))
		first_pass[6] = self.fifth_b(first_pass[6])
		first_pass[9] = self.fourth_b(first_pass[9])

		second_pass = basic_scale()[1:] + self.rhythm(["4."], [self.third_b('d``')]) + self.rest("4")
		second_pass[2:7] = self.third_b(second_pass[2:7])
		return first_pass + second_pass
		

vgs1()