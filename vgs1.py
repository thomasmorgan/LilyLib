# Load LilyLib
exec(open("./lilylib.py").read())

# basic info
title = "Venetianisches Gondellied"
subtitle = "(Venetian Gondola Song)"
composer = "Felix Mendelssohn"
opus = "Op. 19, No. 6"

# set starting key and metre
key = GMinor()
tempo = t68()

# create staves and sections
staves = [Treble("rh"), Bass("lh")]
sections = create_sections(["intro", "octaves", "in_d", "melody1", "melody2"])

# Define common motifs
def LH(a='g,', b=third('g'), c='d'):
	return M(a, b, c).r(8)

def LH_loop():
	return LH()*2 + LH(b=third('a'))*2 + LH()*2 + LH(b=fourth('g'), c='ef')*2

def descending_melody():
	return (S('d``', 'a`') + S('c``', 'g`')).r(8, 4).h([-2]*5 + [-5]*3)

def end_bit():
	melody = M('d` ' + 'ef` '*4).r(8, 4).h([0] + [-2]*4)
	ornament = M('ef` f` g`').r(16, 16, 8).h(-2)
	melody[-2:-1] = ornament
	return melody

def wandering_melody():
	def basic_scale():
		return (S('g`', 'd``') + S('f``', 'd``')).r(8)
	first_pass = third_b('g`') + basic_scale() + M('a`` f`` d``').r(4, 8)
	first_pass[6:7] = fifth_b(first_pass[6:7])
	first_pass[9:10] = fourth_b(first_pass[9:10])

	second_pass = M(basic_scale()[1:]) + third_b('d``').r("4.") + M("r").r(4)
	second_pass[2:7] = third_b(second_pass[2:7])
	return first_pass + second_pass

# write the various sections

W("intro", "rh",
	M("r r").r('2.'))
W("intro", "lh",
	LH()*3 + LH(b=C('a', [-1, 0, 2]), c='ef'))

W("octaves", "rh",
	M('d` f` f` ef`').r('4.'))
W("octaves", "lh",
	LH(a=O('g,,')) + LH(a=O('f,,'), b=third('a'), c='f') + LH(a=O('bf,,'), b=third('bf'), c='f') + LH(a=O('c,'), b=fourth('g'), c='ef'))

key = GMinorH()
W("in_d", "rh",
	M('d` r').r('2.'))
W("in_d", "lh",
	LH('d,')*2 + LH('d,', third('a')) + LH('d,', third('fs')))

W("melody1", "rh",
	M("r r").r('4.', 4) + descending_melody())
key = GMinor()
W("melody1", "rh",
	end_bit())

key = GMinorH()
W("melody1", "lh",
	LH_loop())

W("melody2", "rh",
	M("d` r").r("4.", 4) + M(descending_melody()[0:7]))
W("melody2", "lh",
	M(LH_loop()[0:15]))
key = DMinorH()
W("melody2", "rh", 
	wandering_melody())
W("melody2", "lh",
	M(LH_loop()[15:18]) + LH('g,', third('bf'), 'g') + LH('g,', second('bf'), 'g') + LH('f,', fourth('a'), 'f')*2 + LH('g,', third('bf'), 'g') + LH('a,', N('cs`'), 'a') + LH('d', fourth('a'), 'f')*2)

key = CMinorH()
bridge_v1 = M('f`` d`` c`` b` c`` g` af` b` c`` g` af` b`').r(4, 8) + M('c``').r(2)
bridge_v2 = M('r f` g`').r(8)*2 + third('r c` r r d` r')*2 + M('r ef` g`')*2

key = GMinorH()
bridge_v1 += M('r').r(8) + M('c`` ef`` a` ef`` a`').r(8, 4) + M('ef``').r(2)
bridge_v2 += M('r ef` fs`')*3

#W("bridge", "rh",
#	M('d``').r(8))# + V + bridge_v1 + CV + bridge_v2 + EV
#W("bridge", "lh", [])

# print the score
key = GMinor()
print_score()
