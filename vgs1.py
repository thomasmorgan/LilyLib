exec(open("./lilylib.py").read())

title = "Venetianisches Gondellied"
subtitle = "(Venetian Gondola Song)"
composer = "Felix Mendelssohn"
opus = "Op. 19, No. 6"
key = GMinor()

staves = [Treble("rh"), Bass("lh")]
tempo = t68()
sections = create_sections(["intro", "octaves", "in_d", "melody1", "melody2", "bridge"])

def LH(a='g,', b=third('g'), c='d'):
	a = notify(a)
	c = notify(c)
	c[0].articulation = ")"
	b[0].articulation = "("
	return rhythm(8, a + b + c)

def LH_loop():
	return LH()*2 + LH(b=third('a'))*2 + LH()*2 + LH(b=fourth('g'), c='ef')*2

def descending_melody():
	melody = scale('d``', 'a`') + scale('c``', 'g`') + notes('d` ' + 'ef` '*4)
	melody = rhythm([8, 4], sixth_b(melody[0:5]) + third_b(melody[5:8]) + [melody[8]] + sixth_b(melody[9:]))
	
	global key
	key = GMinor()
	ornament = rhythm([16, 16, 8], sixth_b(notes('ef` f` g`')))
	melody[-2:-1] = ornament
	key = GMinorH()
	return melody

def wandering_melody():
	def basic_scale():
		return rhythm([8], scale('g`', 'd``') + scale('f``', 'd``'))
	first_pass = third_b('g`') + basic_scale() + rhythm([4, 8], notes('a`` f`` d``'))
	first_pass[6:7] = fifth_b(first_pass[6:7])
	first_pass[9:10] = fourth_b(first_pass[9:10])

	second_pass = basic_scale()[1:] + rhythm(["4."], third_b('d``')) + rest("4")
	second_pass[2:7] = third_b(second_pass[2:7])
	return first_pass + second_pass

sections["intro"].score["rh"] = R("2. 2.")
sections["intro"].score["lh"] = LH()*3 + LH(b=C('a', [-1, 0, 2]), c='ef')

sections["octaves"].score["rh"] = N('d`', dur='4.') + N('f`', art="~") + N('f` ef`')
sections["octaves"].score["lh"] = LH(a=O('g,,')) + LH(a=O('f,,'), b=third('a'), c='f') + LH(a=O('bf,,'), b=third('bf'), c='f') + LH(a=O('c,'), b=fourth('g'), c='ef')

key = GMinorH()
sections["in_d"].score["rh"] = N('d`', art="~") + N('d`') + R("2.")
sections["in_d"].score["lh"] = LH('d,')*2 + LH('d,', third('a')) + LH('d,', third('fs'))

sections["melody1"].score["rh"] = R("4. 4") + descending_melody()
sections["melody1"].score["lh"] = LH_loop()

sections["melody2"].score["rh"] = N("d`", dur="4.") + R("4") + descending_melody()[0:7]
sections["melody2"].score["lh"] = LH_loop()[0:15]
key = DMinorH()
sections["melody2"].score["rh"] += wandering_melody()
sections["melody2"].score["lh"] += LH_loop()[15:18] + LH('g,', third('bf'), 'g') + LH('g,', second('bf'), 'g') + LH('f,', fourth('a'), 'f')*2 + LH('g,', third('bf'), 'g') + LH('a,', N('cs`'), 'a') + LH('d', fourth('a'), 'f')*2

key = CMinorH()
sections["bridge"].score["rh"] = (rhythm([8], notes('d``')) +
								  V + rhythm([4, 8], notes('f`` d`` c`` b` c`` g` af` b` c`` g` af` b`')) +
								  CV + rhythm([8], notes('r f` g` r f` g` c`` c` g` af` d` b` c`` c` g` af` d` b`')) + EV)
sections["bridge"].score["lh"] = []

key = GMinor()
print_score()
