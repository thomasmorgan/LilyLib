exec(open("./lilylib.py").read())

title = "Venetianisches Gondellied"
subtitle = "(Venetian Gondola Song)"
composer = "Felix Mendelssohn"
opus = "Op. 19, No. 6"
key = GMinor()

staves = [Treble("rh"), Bass("lh")]
tempo = t68()
sections = create_sections(["intro", "octaves", "in_d", "melody1", "melody2", "bridge"])

def LH(a=N('g,'), b=third('g'), c=N('d')):
	lh = M(a, b, c)
	lh.rhythm(8)
	return lh

def LH_loop():
	return LH()*2 + LH(b=third('a'))*2 + LH()*2 + LH(b=fourth('g'), c='ef')*2

def descending_melody():
	melody = (S('d``', 'a`') + S('c``', 'g`')).rhythm(8, 4).harmony([-2]*5 + [-5]*3)
	return melody

def end_bit():
	melody = M('d` ' + 'ef` '*4).rhythm(8, 4).harmony([0] + [-2]*4)
	ornament = M('ef` f` g`').rhythm(16, 16, 8).harmony(-2)
	melody[-2:-1] = ornament
	return melody

def wandering_melody():
	def basic_scale():
		return (S('g`', 'd``') + S('f``', 'd``')).rhythm(8)
	first_pass = third_b('g`') + basic_scale() + M('a`` f`` d``').rhythm(4, 8)
	first_pass[6:7] = fifth_b(first_pass[6:7])
	first_pass[9:10] = fourth_b(first_pass[9:10])

	second_pass = M(basic_scale()[1:]) + third_b('d``').rhythm("4.") + M("r").rhythm(4)
	second_pass[2:7] = third_b(second_pass[2:7])
	return first_pass + second_pass

sections["intro"].score["rh"] = M("r r").rhythm('2.')
sections["intro"].score["lh"] = LH()*3 + LH(b=C('a', [-1, 0, 2]), c='ef')

sections["octaves"].score["rh"] = M('d` f` f` ef`').rhythm('4.')
sections["octaves"].score["lh"] = LH(a=O('g,,')) + LH(a=O('f,,'), b=third('a'), c='f') + LH(a=O('bf,,'), b=third('bf'), c='f') + LH(a=O('c,'), b=fourth('g'), c='ef')

key = GMinorH()
sections["in_d"].score["rh"] = M('d` r').rhythm('2.')
sections["in_d"].score["lh"] = LH('d,')*2 + LH('d,', third('a')) + LH('d,', third('fs'))

sections["melody1"].score["rh"] = M("r r").rhythm('4.', 4) + descending_melody()
key = GMinor()
sections["melody1"].score["rh"] += end_bit()

key = GMinorH()
sections["melody1"].score["lh"] = LH_loop()

sections["melody2"].score["rh"] = M("d` r").rhythm("4.", 4) + M(descending_melody()[0:7])
sections["melody2"].score["lh"] = M(LH_loop()[0:15])
key = DMinorH()
sections["melody2"].score["rh"] += wandering_melody()
sections["melody2"].score["lh"] += M(LH_loop()[15:18]) + LH('g,', third('bf'), 'g') + LH('g,', second('bf'), 'g') + LH('f,', fourth('a'), 'f')*2 + LH('g,', third('bf'), 'g') + LH('a,', N('cs`'), 'a') + LH('d', fourth('a'), 'f')*2

key = CMinorH()
bridge_v1 = M('f`` d`` c`` b` c`` g` af` b` c`` g` af` b`').rhythm(4, 8) + M('c``').rhythm(2)
bridge_v2 = M('r f` g`').rhythm(8)*2 + third('r c` r r d` r')*2 + M('r ef` g`')*2

key = GMinorH()
bridge_v1 +=  M('r').rhythm(8) + M('c`` ef`` a` ef`` a`').rhythm(8, 4) + M('ef``').rhythm(2)
bridge_v2 += M('r ef` fs`')*3

sections["bridge"].score["rh"] = M('d``').rhythm(8)# + V + bridge_v1 + CV + bridge_v2 + EV
sections["bridge"].score["lh"] = []

key = GMinor()
print_score()
