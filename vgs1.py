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
score = create_sections(["intro", "octaves", "in_d", "melody1", "melody2", "bridge"])

# Define common motifs
def LH(a='g,', b=_3rd('g'), c='d'):
	return M(a, b, c).r(8)

def LH_loop():
	return LH()*2 + LH(b=_3rd('a'))*2 + LH()*2 + LH(b=_4th('g'), c='ef')*2

def descending_melody():
	return (S('d``', 'a`') + S('c``', 'g`')).r(8, 4).h(["6th_"]*5 + ["3rd_"]*3)

def wandering_melody():
	def basic_scale():
		return (S('g`', 'd``') + S('f``', 'd``')).r(8)
	first_pass = basic_scale().hn('f``', '5th_') + M('a`` f`` d``').r(4, 8).hn('a``', '4th_')

	second_pass = basic_scale()[2:] + M('d``').r("4.") + R(4)
	second_pass[2:] = _3rd_(second_pass[2:])
	return first_pass + second_pass

# write the various sections

score["intro"]["rh"] = R("2.")*2
score["intro"]["lh"] = LH()*3 + LH(b=C('a', [-1, 0, 2]), c='ef')

score["octaves"]["rh"] = M('d` f` f` ef`').r('4.') + M('d` r').r('2.')
score["octaves"]["lh"] = LH(a=O('g,,')) + LH(a=O('f,,'), b=_3rd('a'), c='f') + LH(a=O('bf,,'), b=_3rd('bf'), c='f') + LH(a=O('c,'), b=_4th('g'), c='ef')

key = GMinorH()
score["in_d"]["rh"] = M()
score["in_d"]["lh"] = LH('d,')*2 + LH('d,', _3rd('a')) + LH('d,', _3rd('fs'))

score["melody1"]["rh"] = R('4.', 4) + descending_melody()
key = GMinor()
ending = M('d` ' + 'ef` '*4).r(8, 4).h(["1st"] + ["6th_"]*4)
ornament = M('ef` f` g`').r(16, 16, 8).h("6th_")
ending[-2:-1] = ornament
score["melody1"]["rh"] += ending

key = GMinorH()
score["melody1"]["lh"] = LH_loop()

score["melody2"]["rh"] = M("d` r").r("4.", 4) + descending_melody()[1:8] + _3rd_('g`').r(8)
score["melody2"]["lh"] = M(LH_loop()[1:16])
key = DMinorH()
score["melody2"]["rh"] += wandering_melody()
score["melody2"]["lh"] += M(LH_loop()[16:19]) + LH('g,', _3rd('bf'), 'g') + LH('g,', _2nd('bf'), 'g') + LH('f,', _4th('a'), 'f')*2 + LH('g,', _3rd('bf'), 'g') + LH('a,', 'cs`', 'a') + LH('d', _4th('a'), 'f')*2

key = CMinorH()
bridge_v1 = M('f`` d`` c`` b` c`` g` af` b` c`` g` af` b`').r(4, 8) + M('c``').r(2)
bridge_v2 = M('r f` g`').r(8)*2 + _3rd('r c` r r d` r')*2 + M('r ef` g`')*2

key = GMinorH()
bridge_v1 += M('r').r(8) + M('c`` ef`` a` ef`` a`').r(8, 4) + M('ef``').r(2)
bridge_v2 += M('r ef` fs`')*3

score["bridge"]["rh"] = M('d``').r(8) + V + bridge_v1 + CV + bridge_v2 + EV
score["bridge"]["lh"] = M()

# print the score
key = GMinor()
print_score()
