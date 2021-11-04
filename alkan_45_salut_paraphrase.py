from piece import Piece
from points import rest, rests, note, notes, tied_note, chords, chord, arpeggio, diminished7, scale, transpose, add, merge, tied_chord
from staves import Bass, Super
from markup import voices, ottava, clef, key_signature, triplets, linebreak, nolinebreak, grace, pagebreak, slur, phrase, after_grace
from util import join, rep, pattern, omit, select, rep, flatten, subset
from tones import tonify

class Salut(Piece):

	def details(self):
		self.title = "Salut, cendre du pauvre!"
		self.subtitle = "Paraphrase"
		self.composer = "C. V. Alkan"
		self.date = "1856"
		self.mutopiacomposer = "AlkanCV"
		self.mutopiainstrument = "piano"
		self.source = "Simon Richault, 1856"
		self.style = "Romantic"
		self.license = "Creative Commons Attribution-ShareAlike 4.0"
		self.maintainer = "Thomas Morgan"
		self.mantainer_email = "thomas.j.h.morgan@gmail.com"
		self.opus = "Op. 45"
		self.key = "Bf major"
		self.auto_add_bars = True
		self.improvements = False
		if self.improvements:
			self.staves=[Super('treble', extra_text='\\set Score.connectArpeggios = ##t', _with='\\consists "Span_arpeggio_engraver"'), Bass(_with='\\consists "Span_arpeggio_engraver"')]
			self.piano_staff = False
		else:
			self.staves=[Bass('treble', extra_text='\\set Score.connectArpeggios = ##t', _with='\\consists "Span_arpeggio_engraver"'), Bass(_with='\\consists "Span_arpeggio_engraver"')]
		

	def subtext(self):
		return '''
\\layout {
  \\context {
	\\Staff
	\\RemoveEmptyStaves
  }
}
\\layout {
  \\context {
	\\Score
	\\consists "Span_arpeggio_engraver"
  }
}
		'''

	def write_score(self):

		##################
		# Opening Chords #
		##################

		def rolled_chords(chord1, chord2):
			return [
				chords([select(chord1, 4, 5), select(chord2, 4, 5), select(chord1, 5, 6), select(chord2, 4, 5)], [2, 2, 2, '4.'], ornamentation='arpeggio'),
				chords([subset(chord1, 1, 3), subset(chord2, 1, 3), select(chord1, 1, 3, 4), subset(chord2, 1, 3)], [2, 2, 2, '4.'], ornamentation='arpeggio')
			]

		dim7 = diminished7('bf,,', 6, key='e major')
		fmaj = omit(arpeggio('f,,', 6, key='f major'), 2)

		opening_chords = rolled_chords(dim7, fmaj)

		if self.improvements:
			opening_chords = {
				'treble': rests(1, 2, 4, 8),
				'bass': ottava(voices(select(opening_chords, 1), select(opening_chords, 2)), -1)
			}
			select(opening_chords['treble'], 1).prefix += ' \\override Rest.transparent = ##t '
		else:
			opening_chords = {
				'treble': select(opening_chords, 1),
				'bass': select(opening_chords, 2)
			}
		
		select(opening_chords['treble'], 1).prefix = '\\tempo "Adagio sostenuto" 4 = 69'
		select(opening_chords['treble'], 1).dynamics = "mf"

		############
		# Melody 1 #
		############

		def melody(tone, durs, key, alt=False):
			tones = scale(self.transpose(tone, -1, 'octave'), 9, key=key)
			if not alt:
				melody = notes(pattern(tones, 1, 8, 8, 9, 7, 5, 4, 3), [8, 2, 8, 8, 8, 8]+durs)
			else:
				melody = notes(pattern(tones, 1, 8, 8, 8, 9, 7, 5, 4, 4, 3, 6, 5), [8, '4.', 8, 8, 8, 8, 8, 2, 8, 8, 8, 8])

			select(melody, 1).articulation += '('
			select(melody, 2).dynamics = '<'
			if not alt:
				select(melody, 6).articulation += ')'
				select(melody, 7).articulation += '('
				select(melody, 2).phrasing += '~'
				select(melody, 4).dynamics = '!'
			else:
				select(melody, 8).phrasing += "~"
				select(melody, 5).dynamics = '!'
			select(melody, len(melody)).articulation += ')'
			return(melody)

		upper_treble_voice = melody('f`', [2, '4.'], self.key) + melody('c`', ['2.', 4], self.key)
		select(upper_treble_voice, len(upper_treble_voice)).replace('ef', 'e')
		lower_treble_voice = rests(8, prefix='\\omit ') + rests(4) + notes('c` bf g', 4) + slur(notes('f e f ds', 4)) + rests(4) + notes('e f d', 4) + slur(notes('c b, bf,', [4, 4, 2]))
		if self.improvements:
			select(lower_treble_voice, 9).replace('ds', 'ef')

		select(lower_treble_voice, 4).add('d`')
		select(lower_treble_voice, 12).add('a')

		select(upper_treble_voice, 1).dynamics = 'p'
		select(upper_treble_voice, 1).markup = '\\italic{dolce cantabile}'
		select(upper_treble_voice, 15).markdown = '\\italic{dim.}'
		select(lower_treble_voice, 3).markdown = '\\dynamic{pp} \\italic{e legatissimo}'

		treble = voices(upper_treble_voice, lower_treble_voice)

		bass = (
			rests(8, 4) + notes('a, bf,', 4) + [chord('ef, ef', 4)] +
			voices(slur(self.chromatic('d', -3, dur=[4, 4, '4.'])) + rests(8), slur(notes('f, fs,', ['2.', 4]))) +
			rests(4) + notes('g, a,', 4) + [chord('bf,, bf,', 4)] +
			voices(slur(self.chromatic('a,', -3, dur=[4, 4, 2])), notes('c, c,', ['2.', 4]))
		)

		select(bass, len(bass)).suffix += linebreak

		if self.improvements:
			melody1 = {'treble': treble, 'bass': bass}
		else:
			melody1 = {'treble': clef('treble', treble), 'bass': bass}

		####################
		# Opening Chords 2 #
		####################

		dim7 = diminished7('f,,', 6, key='b minor')
		cmaj = omit(arpeggio('c,,', 6, key='c major'), 2)
		opening_chords2 = rolled_chords(dim7, cmaj)

		if self.improvements:
			opening_chords2 = {
				'treble': rests(1, 2, 4, 8),
				'bass': ottava(voices(select(opening_chords2, 1), select(opening_chords2, 2)), -1)
			}
			select(opening_chords2['treble'], 1).prefix += ' \\override Rest.transparent = ##t '
		else:
			opening_chords2 = {
				'treble': clef('bass', select(opening_chords2, 1)),
				'bass': select(opening_chords2, 2)
			}

		select(opening_chords2['treble'], 1).dynamics = "mf"
		#select(opening_chords2['bass'], 2).suffix = nolinebreak

		# ############
		# # Melody 2 #
		# ############

		upper_treble_voice = melody('af`', [2, '4.'], 'bf minor') + melody('e`', ['2.', 4], 'a major', True)
		lower_treble_voice = rests(8, prefix='\\omit ') + rests(4) + chords(['ef`', 'df` f`', 'bf'], 4) + phrase(notes('af g', 4) + slur(notes('af gs', 4))) + rests(4) + chords(['e c`', 'e cs`'], 4) + notes('fs e fs d', [4, 4, 4, 2])

		select(upper_treble_voice, 1).dynamics = 'p'
		select(upper_treble_voice, 1).markup = '\\italic{dolce}'
		select(lower_treble_voice, 3).dynamics = 'pp'
		select(upper_treble_voice, len(upper_treble_voice)-2).markdown = '\\italic{ten.}'

		treble = voices(upper_treble_voice, lower_treble_voice)
		
		bass = rests(8, 4) + voices(
			notes('af gf, gf', [2, 8, 8]) + slur(notes('f e ef', [4, 4, '4.'])) + rests(8, 4) + chords(['gs, d', 'a, cs'], 4) + notes('d, d', 8) + slur(notes('cs d b, e,', [4, 4, 4, 4])),
			notes('c df gf,', 4) + notes('af, gs,', ['2.', 4]) + rests(2, 4, prefix='\\omit ') + notes('d, e, e,', [4, '2.', 4])
		)

		if self.improvements:
			melody2 = {'treble': treble, 'bass': bass}
		else:
			melody2 = {'treble': clef('treble', treble), 'bass': bass}

		select(melody2['bass'], len(melody2['bass'])).suffix = linebreak + select(melody2['bass'], len(melody2['bass'])).suffix


		############
		# Chords 1 #
		############

		self.set_key('a major')

		def octave(tone):
			return chord([tone, transpose(tone, -1, 'a major', 'octave')], 8)

		def triple(points):
			return flatten([triplets(rep(point, 3), omit_number=True) for point in flatten([points])])

		def triple_octaves(tones):
			return flatten([triple(octave(t)) for t in flatten([tonify(tones)])])

		upper_treble4 = notes('a cs` d` e` fs` gs`', ['2.', 8, 8]) + notes('a` b` fs`', [2, '4.', 8]) + slur(notes('a` gs` g`', [2, 4, 4]))
		lower_treble4 = triple(chords(['cs e', 'cs e', 'cs e', 'e a', 'e b', 'e gs b', 'e gs b', 'b e`', 'a cs`', 'a cs`', 'b d` fs`', 'b d`', 'cs` e`', 'a cs` e`', 'gs b e`', 'g b e`'], 8))
		bass4 = triple_octaves('a, e cs a, gs, b, gs, e fs, a, d, fs, e, ds e') + triple(chord('e, d', 8))

		if self.improvements:
			select(upper_treble4, 1).prefix += self.key_signature
			select(bass4, 1).prefix += self.key_signature

		select(lower_treble4, 1).markdown = '\\italic{poco cresc.}'
		select(lower_treble4, 1).markup = '\\italic{sempre sostenuto}'
		select(bass4, 1).ornamentation = 'sustainOn'
		select(bass4, 2).markdown = '\\italic{sostenuto}'
		select(lower_treble4, 25).dynamics = '<'
		select(lower_treble4, 31).dynamics = '!\\>'
		select(lower_treble4, 36).dynamics = '!'
		
		if not self.improvements:
			select(upper_treble4, 1).prefix = '\\clef "bass" ' + select(upper_treble4, 1).prefix

		upper_treble8 = notes('fs` b` d``', ['2.', 8, 8]) + notes('d`` e` a` cs`` cs`` d` cs` e`', [4, 2, 8, 8]) + notes('cs` b c`', [2, 4, 4])
		for i in [1, 4, 8, 12]:
			select(upper_treble8, i).phrasing = '('
		for i in [5, 9]:
			select(upper_treble8, i).phrasing = ')-('
		for i in [3, 7, 11, 14]:
			select(upper_treble8, i).phrasing = ')'
		if not self.improvements:
			select(upper_treble8, 2).prefix = '\\clef "treble" ' + select(upper_treble8, 2).prefix
		lower_treble8 = triple(chords(['fs as cs`', 'fs as cs`', 'fs b d`', 'd` fs`', 'd` e`', 'e gs b', 'e a cs`', 'cs` e`', 'd` a`', 'e b', 'e b', 'e a', 'e a', 'fs a', 'gs', 'fs gs'], 8))
		bass8 = add(triple(notes('cs e d b, gs, d cs a, fs,', 8)) + triple_octaves('gs, a, cs') + triple(notes('e, ds e', 8)), 'e,') + triple_octaves('d')

		select(upper_treble8, 4).dynamics = '>'
		select(upper_treble8, 5).dynamics = '!\\<'
		select(upper_treble8, 7).dynamics = '!'
		select(upper_treble8, 8).dynamics = '>'
		select(upper_treble8, 9).dynamics = '!'
		select(lower_treble8, 1).dynamics = '<'
		select(lower_treble8, 11).dynamics = '!'
		if not self.improvements:
			select(lower_treble8, 28).prefix = '\\clef "bass" ' + select(lower_treble8, 28).prefix
		select(lower_treble8, 29).markdown = '\\italic{dim.}'
		select(lower_treble8, 37).dynamics = '>'
		select(lower_treble8, 43).dynamics = '!'
		select(lower_treble8, 46).dynamics = 'p'

		upper_treble12 = notes('df` f` gf` af` bf` c``', ['2.', 8, 8]) + notes('df`` f`` ef``', [2, '4.', 8]) + notes('df`` c`` b`', [2, 4, 4])
		lower_treble12 = triple(chords(['f af', 'f af', 'f af', 'f af df`', 'af ef`', 'af c` ef`', 'af c` ef`', 'c` ef` af`', 'ef` bf`', 'ef` g` bf`', 'g` bf` df``', 'ef` bf` df``', 'ef` g` bf`', 'ef` g` bf`', 'ef` af`', 'ef` af`'], 8))
		bass12 = add(triple_octaves('df af f df c ef c af,'), 'af,') + add(triple_octaves('g, bf, ef, g,'), 'ef,') + add(triple_octaves('af,'), 'ef,') + triple_octaves('ef') + add(triple_octaves('af'), 'ef') + add(triple(notes('b', 8)), 'af')

		if not self.improvements:
			select(upper_treble12, 4).prefix = '\\clef "treble" ' + select(upper_treble12, 4).prefix
			for p in upper_treble12:
				p.replace('df` f` gf` af` bf` c`` df`` f`` ef``', 'cs` es` fs` gs` as` bs` cs`` es`` ds``')
			for p in lower_treble12:
				p.replace('f af c` df` ef` f` gf` af` bf` c`` df`` f`` ef`` g`', 'es gs bs cs` ds` es` fs` gs` as` bs` cs`` es`` ds`` fss`')
			for p in bass12:
				p.replace('ef,, g,, af,, bf,, c, df, ef, f, g, af, bf, c df ef f af', 'ds,, fss,, gs,, as,, bs,, cs, ds, es, fss, gs, as, bs, cs ds es gs')

		for i in [1, 4, 10]:
			select(upper_treble12, i).phrasing = '('
		for i in [3, 6, 12]:
			select(upper_treble12, i).phrasing = ')'

		select(upper_treble12, 1).markdown = "\\italic{cresc. poco a poco}"
		if self.improvements:
			select(upper_treble12, 1).prefix += "\\key af \\major "
			select(bass12, 1).prefix += "\\key af \\major "
		select(upper_treble12, 7).dynamics = "<"
		select(upper_treble12, 8).dynamics = "rfz"
		select(upper_treble12, 10).dynamics = ">"
		select(upper_treble12, 12).dynamics = "p"

		upper_treble16 = notes('b` e`` g``', ['2.', 8, 8]) + notes('g`` g` c`` e`` e`` e` a` c``', [4, 2, 8, 8]) + notes('c`', [2, '4.', 8])
		lower_treble16 = triple(chords(['ds` fs`', 'ds` a`', 'e` g`', 'g` b`', 'g` b` d``', 'b f`', 'c` e`', 'e` g`', 'e` gs`', 'gs d`', 'a c`', 'c` e`', 'f a', 'f a', 'e g', 'g bf'], 8))
		bass16 = add(triple(notes('a fs g e', 8)), 'b') + add(triple(chords(['f b', 'ds g', 'e', 'c'], 8)), 'g') + add(triple(notes('d b, c a,', 8)), 'e') + triple(chords(['f, c']*4, 8))

		for i in [1, 4]:
			select(upper_treble16, i).phrasing = '('
		for i in [3, 6]:
			select(upper_treble16, i).phrasing = ')'

		select(lower_treble16, 9).dynamics = '<'
		select(lower_treble16, 12).dynamics = '!'
		select(lower_treble16, 13).dynamics = '>'
		select(lower_treble16, 15).dynamics = '!'
		select(lower_treble16, 25).dynamics = '>'
		select(lower_treble16, 27).dynamics = '!'
		select(lower_treble16, 28).dynamics = '<'
		select(lower_treble16, 36).dynamics = '!'
		select(lower_treble16, 37).dynamics = 'p'
		select(lower_treble16, 37).markup = '\\italic{dolce}'
		select(bass16, 37).markdown = '\\italic{sostenutissimo}'

		if self.improvements:
			select(upper_treble16, 1).prefix += '\\key e \\minor '
			select(bass16, 1).prefix += '\\key e \\minor '

		upper_treble19 = notes('c` f` ef` df` g a bf', 4) + chords(['bf d`', 'a c`'], 8) + notes('bf a', [2, 4])
		lower_treble19 = triple(chords(['f a', 'f c`', 'f c`', 'f bf', 'f', 'f g', 'e g', 'e', 'e g', 'e g', 'f'], 8))
		bass19 = triple(chords(['f, c'], 8)) + triple_octaves('a, bf, df c c c c') + triple(chords(['f, c', 'c, f, c', 'f, c'], 8))

		if self.improvements:
			select(upper_treble19, 1).prefix += '\\key bf \\major '
			select(bass19, 1).prefix += '\\key bf \\major '

		if not self.improvements:
			select(upper_treble19, 1).prefix += '\\clef "bass" '

		for i in [5, 10]:
			select(upper_treble19, i).phrasing = '('
		for i in [9, 11]:
			select(upper_treble19, i).phrasing = ')'

		select(lower_treble19, 4).dynamics = '>'
		select(lower_treble19, 12).dynamics = '!'
		select(lower_treble19, 13).dynamics = '<'
		select(lower_treble19, 22).dynamics = '!\\>'
		select(lower_treble19, 24).dynamics = '!'

		chords1 = {
			'treble': voices(
				upper_treble4 + upper_treble8 + upper_treble12 + upper_treble16 + upper_treble19,
				lower_treble4 + lower_treble8 + lower_treble12 + lower_treble16 + lower_treble19
			),
			'bass': bass4 + bass8 + bass12 + bass16 + bass19
		}

		# ############
		# # Chords 2 #
		# ############

		# self.set_key('bf major')

		# def f_octave(dur):
		# 	return [note('f', 8, articulation="("), note('f`', dur, articulation=')')]

		# upper_bass = chords(['c ef', 'bf, d', 'gs, b,', 'a, c', 'd f', 'c ef', 'a, cs', 'bf, d', 'ef g', 'c ef', 'a, f', 'bf, d', 'g, ef', 'a, c'], 4)
		# select(upper_bass, 1).articulation = '('
		# select(upper_bass, 4).articulation = ')'
		# select(upper_bass, 5).articulation = '('
		# select(upper_bass, 8).articulation = ')'
		# select(upper_bass, 8).markup = '\\italic{poco cresc.}'
		# select(upper_bass, 9).articulation = '('
		# select(upper_bass, 14).articulation = ')'

		# chords2 = {
		# 	'treble': rep(rests(8) + f_octave('2.'), 2) + rests(8) + rep(f_octave('4.'), 2),
		# 	'bass': voices(upper_bass, rep(triple(notes('f,', 8)), 14))
		# }

		# select(chords2['treble'], 1).prefix += ' \\override Rest.transparent = ##f '
		# select(chords2['treble'], 1).dynamics = 'p'

		# ############
		# # Chords 3 #
		# ############

		# upper_treble = subset(melody('f`', [2, 8], self.key), 1, 6) + tied_note('bf', [2, 8]) + notes('a g a', 8)
		# select(upper_treble, 7).articulation = ')-('
		# select(upper_treble, 11).articulation = ')'

		# lower_treble = rests(8, 4) + triple(notes('af g g f e ef c', 8))
		# select(lower_treble, 1).prefix += ' \\override Rest.transparent = ##t '
		# select(lower_treble, 14).markdown = '\\italic{smorz.}'

		# bass = merge(triple(notes('d, ef, ef,', 8)), notes('bf, bf, bf, bf, bf, b, c c ef,', 8)) + add(triple(notes('d cs c ef', 8)), 'f,')

		# chords3 = {
		# 	'treble': voices(upper_treble, lower_treble),
		# 	'bass': bass
		# }

		# #########
		# # Plods #
		# #########

		# self.set_key('b minor')

		# def plod(tones):
		# 	tones = tonify(tones)
		# 	return grace(notes(tones, 16)) + notes(select(tonify(tones), 1), 8, articulation="!") + rests(8)

		# def octoplod(tones):
		# 	plink = plod(tones)
		# 	select(plink, 3).add(self.transpose(select(tonify(tones), 1), 1, 'octave'))
		# 	return plink

		# def superoctoplod(tones):
		# 	plink = octoplod(tones)
		# 	select(plink, 1).add(self.transpose(select(tonify(tones), 1), 1, 'octave'))
		# 	return plink

		# def harmoplod(tones):
		# 	tones = tonify(tones)
		# 	plink = plod(subset(tones, 1, 2))
		# 	select(plink, 3).add(select(tones, 3))
		# 	return plink

		# def harmoctoplod(tones):
		# 	tones = tonify(tones)
		# 	plink = superoctoplod(subset(tones, 1, 2))
		# 	select(plink, 1).add(select(tones, 3))
		# 	select(plink, 3).add(select(tones, 3))
		# 	return plink


		# def treble_plod(one, two, three, held_note=2):
		# 	if len(one) == 3:
		# 		melody = chords(one, 8)
		# 	elif len(one) == 2:
		# 		tones = tonify(select(one, 1))
		# 		melody = chords([subset(tones, 1, 3), subset(tones, 2, 4), select(one, 2)], 8)
		# 	elif len(one) == 1:
		# 		tones = tonify(select(one, 1))
		# 		melody = chords([subset(tones, 1, 3), subset(tones, 2, 4), subset(tones, 3, 5)], 8)
		# 	melody = triplets(melody)
		# 	vs = voices(chords([omit(select(melody, 3).tones, held_note), two, three], ['4.', 8, 4]), notes(select(select(melody, 3).tones, held_note), 2) + [rest(4, prefix='\\omit ')])
		# 	select(vs, 1).articulation = '('
		# 	select(vs, 2).articulation = ')'
		# 	melody += vs
		# 	return melody

		# def extended_treble_plod(one, two, three, four, five, six, seven, eight):
		# 	melody = treble_plod(one, two, three)
		# 	melody = (
		# 		subset(melody, 1, 3) + chords([select(melody, 3).tones, two, three, three], [4, '8.', 16, 4]) +
		# 		chords([four, five, six, seven, eight], [8, 8, '8.', 16, 4]) + rests(4)
		# 	)
		# 	select(melody, 4).articulation = '('
		# 	select(melody, 5).articulation = ')'
		# 	select(melody, 7).articulation = '('
		# 	select(melody, 8).articulation = ')'
		# 	select(melody, 10).articulation = '('
		# 	select(melody, 12).articulation = ')'
		# 	return melody

		# def mini_treble_plod(one, two, three, alt=False):
		# 	tones = tonify(select(one, 1))
		# 	melody = (
		# 		triplets(chords([subset(tones, 1, 3), subset(tones, 2, 4), subset(tones, 3, 5)], 8)) +
		# 		chords([two], '8.', articulation='(') + chords([three], 16, articulation=')')
		# 	)
		# 	if not alt:
		# 		return melody + chords([two], 2)
		# 	else:
		# 		tones = tonify(two)
		# 		return (
		# 			melody + 
		# 			voices(chords([select(tones, 1, 3), three], ['4.', 8]), chords([select(tones, 2)], 2)) +
		# 			tied_chord(two, [4, 8]) + chords([three], 8) + rep(chords([two], 8, articulation="(") + chords([three], 8, articulation=")"), 3)
		# 		)

		# treble = (
		# 	rests(2, 4) + treble_plod(['as, cs fs as', 'e fs cs`'], 'd fs b', 'cs fs as') +
		# 	treble_plod(['cs fs as', 'e fs cs`', 'g as e`'], 'fs d`', 'e as cs`') +
		# 	extended_treble_plod(['e as cs`', 'g as e`', 'as e` g`'], 'as d` fs`', 'g as e`', 'fs as d`', 'e as cs`', 'd fs b', 'cs`', 'cs fs as') +
		# 	treble_plod(['b, d fs b d`'], 'e cs`', 'd fs b', held_note=1) + treble_plod(['d d fs b d`'], 'e cs`', 'd fs b', held_note=1) +
		# 	extended_treble_plod(['fs b d` fs` b`'], 'b d` g`', 'b d` fs`', 'g b e`', 'fs b d`', 'e as cs`', 'd`', 'd fs b') +
		# 	treble_plod(['d es gs b d`'], 'as cs`', 'es gs b') + treble_plod(['es gs b d` es`'], 'cs` e`', 'gs b d`') +
		# 	extended_treble_plod(['gs b d` es`', 'b d` es` gs`', 'd` es` gs` b`'], 'a d` fs` a`', 'fs a d` fs`', 'e a e`', 'd a d', 'ds a bs', 'e cs`', 'ds a bs') +
		# 	mini_treble_plod(['ds a bs ds` a`'], 'ds` a` bs`', 'e` cs``') + mini_treble_plod(['ds` a` bs` ds`` a``'], 'ds`` a`` bs``', 'e`` cs```', alt=True) +
		# 	merge(self.chromatic('ds``', -8, 8), self.chromatic('a``', -8, 8), self.chromatic('c```', -8, 8)) + 
		# 	merge(self.chromatic('fs``', -8, 8), self.chromatic('c```', -8, 8), self.chromatic('ds```', -8, 8)) + 
		# 	chords([subset(tonify('bs ds` fs` a` bs` ds`` fs`` a`` bs`` ds``` fs```'), i, i+3) for i in [8, 7, 6, 5, 4, 3, 2, 1]], 8) +
		# 	chords(['as cs` e` g`', 'gs b d` f`', 'fs a c` ef`', 'es gs b d`'], 4, articulation='^') +
		# 	chords(['ef fs a c`', 'd es gs b', 'as, cs fs', 'as, cs fs', 'as, cs fs', 'as, cs f'], [2, 2, 1]) + 
		# 	voices(notes('e', 1), notes('cs', 2, articulation='(') + notes('c', 4) + notes('bf,', 4, articulation=')'))
		# )
		# select(treble, 43).replace('b', 'fs`')
		# select(treble, 46).replace('fs', 'b')
		# select(treble, 80).tones = tonify('d` fs` a` d``')

		# select(treble, 1).dynamics = 'p'
		# select(treble, 3).dynamics = '<'
		# select(treble, 5).dynamics = '!'
		# select(treble, 6).dynamics = '>'
		# select(treble, 8).dynamics = '!'
		# select(treble, 11).dynamics = '<'
		# select(treble, 13).dynamics = '!'
		# select(treble, 14).dynamics = '>'
		# select(treble, 16).dynamics = '!'
		# select(treble, 19).dynamics = '<'
		# select(treble, 21).dynamics = '!'
		# select(treble, 22).dynamics = '>'
		# select(treble, 23).dynamics = '!'
		# select(treble, 32).markdown = '\\italic{cresc. poco a poco}'
		# select(treble, 48).dynamics = '<'
		# select(treble, 50).dynamics = '!'
		# select(treble, 51).dynamics = '>'
		# select(treble, 52).dynamics = '!'
		# select(treble, 77).dynamics = '<'
		# select(treble, 79).dynamics = '!'
		# select(treble, 80).dynamics = 'f\\>'
		# select(treble, 82).dynamics = '!'
		# select(treble, 87).markdown = '\\italic{sempre cresc. e sempre} Ped.'
		# select(treble, 99).dynamics = 'f'
		# select(treble, 105).dynamics = '<'
		# select(treble, 112).dynamics = '!'
		# select(treble, 113).dynamics = 'ff'
		# select(treble, 114).markdown = '\\italic{sempre} Ped.'
		# select(treble, 121).markdown = '\\italic{Poco accel.}'
		# select(treble, 129).dynamics = 'sf'
		# select(treble, 130).markdown = '\\italic{rinf. molto}'
		# select(treble, 141).markdown = '\\italic{dim. poco a poco, ma sempre pedale}'
		# select(treble, 146).markdown = '\\italic{poco rall. \\bold{p}}'
		# select(treble, 147).markup = '\\italic{ten.}'
		# select(treble, 148).dynamics = '>'
		# select(treble, 150).dynamics = '!'


		# bass = (
		# 	rep(plod('fs,, es,,'), 44) + rep(octoplod('fs,, es,,'), 20) +
		# 	rep(superoctoplod('fs,, es,,'), 8) + rep(harmoctoplod('fs,, es,, cs,'), 4) + rep(superoctoplod('fs,, es,,'), 8) +
		# 	rep(octoplod('fs,, es,,'), 8) + rep(harmoplod('fs,, es,, cs,'), 4) +
		# 	rep(harmoplod('fs,, es,, as,,'), 2) + rep(plod('fs,, es,,'), 2)
		# )

		# plods = {
		# 	'treble': key_signature(self.key, treble),
		# 	'bass': key_signature(self.key, ottava(bass, -1))
		# }

		# #################
		# # Bridge melody #
		# #################

		# self.set_key('bf major')

		# treble_melody = melody('f```', [2, 4], self.key)
		# treble_harmony = rests(8, 4, prefix='\\omit ') + chords(['c``` ef```', 'bf`` d```', 'ef`` g``', 'd`` f``', 'df`` e``', 'c`` f``'], 4)
		# treble_harmonyb = rests(8, prefix='\\omit ') + rests(4) + rests(4, 2, prefix='\\omit ') + notes('f`', '2.')

		# select(treble_melody, 6).articulation = ')'
		# select(treble_melody, 7).articulation = '('
		# select(treble_melody, 7).ornamentation = "arpeggio"
		# select(treble_harmony, 3).prefix = '\\stemDown ' + select(treble_harmony, 3).prefix
		# select(treble_harmony, 6).ornamentation = "arpeggio"
		# select(treble_harmony, 8).suffix += '\\stemNeutral '
		# select(treble_harmonyb, 5).ornamentation = "arpeggio"

		# treble_part1 = rests('2.', 8) + voices(treble_melody, treble_harmonyb, treble_harmony) + rests(4)
		# bass_part1 = self.transpose(treble_part1, -2, 'octave')
		# for t in bass_part1:
		# 	t.dynamics = ''
		# select(treble_part1, 3).markup = '\\italic{Voci principali \\bold{pp} in entrambe le mani}'
		# select(treble_part1, 4).markdown = '\\italic{Altre voci \\bold{ppp}}'
		# select(treble_part1, 2).suffix += '\\omit \\sustainOn'
		# select(treble_part1, 3).suffix += '\\sustainOff'
		# select(treble_part1, 1).prefix = '\\set Score.connectArpeggios = ##f \\set Staff.connectArpeggios = ##t\n' + select(treble_part1, 1).prefix
		# select(bass_part1, 1).prefix = '\\set Score.connectArpeggios = ##f \\set Staff.connectArpeggios = ##t\n' + select(bass_part1, 1).prefix

		# treble_melody2 = melody('c```', [2, 4], self.key)
		# treble_harmony2 = rests(8, 4, prefix='\\omit ') + chords(['g`` bf``', 'f`` a``', 'bf` d``', 'a` c``', 'af` b`', 'c` g` c``'], 4)
		# treble_harmonyb2 = rests(8, prefix='\\omit ') + rests(4) + rests(4, 2, prefix='\\omit ') + notes('c`', 2) + rests(4, prefix='\\omit ')

		# select(treble_melody2, 6).articulation = ')'
		# select(treble_melody2, 7).articulation = '('
		# select(treble_melody2, 7).ornamentation = 'arpeggio'
		# select(treble_melody2, 8).replace('ef``', 'e``')
		# select(treble_harmony2, 3).prefix = '\\stemDown ' + select(treble_harmony, 3).prefix
		# select(treble_harmony2, 6).ornamentation = "arpeggio"
		# select(treble_harmony2, 8).suffix += '\\stemNeutral '
		# select(treble_harmonyb2, 5).ornamentation = "arpeggio"

		# treble_part2 = rests(4, 8) + voices(treble_melody2, treble_harmonyb2, treble_harmony2) + rests(2, 8)
		# bass_part2 = self.transpose(treble_part2, -2, 'octave')
		# for t in bass_part2:
		# 	t.dynamics = ''

		# select(treble_part2, 24).ornamentation = 'arpeggio'
		# select(bass_part2, 24).remove('c,')

		# treble_melody3 = slur(notes('a` a``', [8, '2.'])) + rests(8, prefix='\\omit ') + slur(notes('bf` bf``', [8, '2.'])) + rests(8, prefix='\\omit ') + slur(notes('b` b``', [8, '2.']))
		# treble_harmony3 = rests(8, 4, prefix = '\\omit ') + slur(chords(['e`` g``', 'fs``', 'f``'], [4, 4, 8])) + rests(8, 4, prefix='\\omit ') + slur(chords(['f`` af``', 'g``', 'gf``'], [4, 4, 8])) + rests(8, 4, prefix='\\omit ') + slur(chords(['fs`` a``', 'gs``', 'g``'], [4, 4, 8]))
		# treble_harmonyb3 = rests(8, prefix='\\omit ') + rests(4) + rests(4, prefix='\\omit ') + notes('d``', '4.') + rests(8, prefix='\\omit ') + rests(4) + rests(4, prefix='\\omit ') + notes('ef``', '4.') + rests(8, prefix='\\omit ') + rests(4) + rests(4, prefix='\\omit ') + notes('e``', '4.')

		# bass_melody3 = self.transpose(treble_melody3, -2, 'octave')
		# bass_harmony3 = rests(8, prefix='\\omit ') + rests(4) + chords(['cs e', 'd fs', 'f a'], [4, 4, 8]) + rests(8, prefix='\\omit ') + rests(4) + chords(['d f', 'ef g', 'gf bf'], [4, 4, 8]) + rests(8, prefix='\\omit ') + rests(4) + chords(['ds fs', 'e gs', 'g b'], [4, 4, 8])
		# select(treble_melody3, 1).markdown = '\\italic{Voci principali \\bold{p}, altre voci \\bold{pp}}'
		# select(treble_melody3, 7).markdown = '\\italic{poco cresc.}'
		# select(treble_harmony3, 3).prefix = '\\stemDown \\slurDown' + select(treble_harmony, 3).prefix
		# select(treble_harmony3, 15).suffix += '\\stemNeutral \\slurNeutral'
		# select(treble_harmony3, 14).markdown = '\\italic{poco rinf}'

		# treble_part3 = voices(treble_melody3, treble_harmonyb3, treble_harmony3)
		# bass_part3 = voices(bass_melody3, bass_harmony3)

		# shared_melody = slur(notes('c``', 8) + notes('c```', 2, articulation='~')) + notes('c``` ef``` d``` bf`` g`` ef`` c`` d``', 8) + notes('ef``', 4) + chords(['ef`` g``', 'd`` f``'], 8)
		# select(shared_melody, 1).ornamentation = '('
		# select(shared_melody, 6).ornamentation = ')'
		# select(shared_melody, 7).ornamentation = '('
		# select(shared_melody, 13).ornamentation = ')'
		
		# treble_melody4 = self.harmonize(subset(shared_melody, 1, 10), -1, 'octave')  + subset(shared_melody, 11, 13) + chords(['c`` ef``', 'bf` d``'], [4, 8])
		# treble_harmony4 = rests(8, 4) + chords(['gs`` bf``', 'a``'], 4) + rests(4, 4) + chords(['g`', 'c` g`', 'f` a`'], 4) + notes('f`', '4.')
		# treble_harmonyb4 = rests(8, 1, 2, prefix='\\omit ') + notes('c`` bf`', 8, prefix='\\stemDown ', suffix='\\stemNeutral ') + rests(4, '4.', prefix='\\omit ')
		# select(treble_melody4, 11).ornamentation = 'arpeggio'
		# select(treble_melody4, 12).ornamentation = 'arpeggio'
		# select(treble_harmony4, 8).ornamentation = 'arpeggio'
		# select(treble_harmony4, 9).ornamentation = 'arpeggio'

		# bass_melody4 = self.transpose(shared_melody, -2, 'octave')
		# bass_harmony4 = rests(8, 4) + chords(['e gs bf', 'f a', 'bf, f'], 4) + rests(4) + chords(['ef, g,', 'c, g,', 'f, a,'], 4)
		# bass_harmonyb4 = rests(8, 1, 2, prefix='\\omit ') + notes('c bf,', 8, prefix='\\stemDown ', suffix='\\stemNeutral ') + rests(4, prefix='\\omit ')
		# select(bass_melody4, 5).ornamentation = 'arpeggio'
		# select(bass_harmony4, 5).ornamentation = 'arpeggio'
		# select(bass_harmony4, 8).ornamentation = 'arpeggio'
		# select(bass_harmony4, 9).ornamentation = 'arpeggio'

		# select(treble_melody4, 2).dynamics = '<'
		# select(treble_melody4, 4).dynamics = '!'
		# select(treble_melody4, 7).markdown = '\\italic{dim}'
		# select(treble_melody4, 12).dynamics = '>'
		# select(treble_melody4, 15).dynamics = '!'

		# treble_part4 = voices(treble_melody4, treble_harmony4, treble_harmonyb4)
		# bass_part4 = voices(bass_melody4, bass_harmony4, bass_harmonyb4)

		# bridge = {
		# 	'treble': key_signature(self.key, ottava(treble_part1, 1) + treble_part2 + treble_part3 + treble_part4),
		# 	'bass': key_signature(self.key, bass_part1 + bass_part2 + bass_part3 + bass_part4)
		# }

		# ############
		# # Chords 4 #
		# ############

		# treble = (
		# 	rests(8, 4, 8) + subset(melody('f`', [4, 8], self.key), 1, 6) + slur(notes('ef` d`', [4, 8])) +
		# 	rests(8, 4, 8) + slur(notes('f f`', [8, 4])) + rests(8) +
		# 	notes('f f` g` ef` c`', 8) + slur(notes('ef` d`', [4, 8])) + rests(8, 4, 8) +
		# 	slur(notes('bf', 8) + tied_note('bf`', [2, 8]) + notes('c`` af` fs`', 8)) + slur(notes('g` af` f` d` ef` c` af fs', 8)) +
		# 	slur(notes('g a bf', 8) + chords(['ef ef`'], 8)) +
		# 	voices(slur(chords(['bf d`', 'a c`', 'bf'], [4, '8.', 16])), notes('f', 2))
		# )
		# select(treble, 4).markdown = '\\italic{dolce}'
		# select(treble, 9).articulation = ')'
		# select(treble, 15).dynamics = '<'
		# select(treble, 16).dynamics = '!'
		# select(treble, 18).articulation = '('
		# select(treble, 18).dynamics = '<'
		# select(treble, 20).dynamics = '!'
		# select(treble, 22).articulation = ')'
		# select(treble, 28).markdown = '\\italic{poco cresc.}'
		# select(treble, 29).dynamics = '<'
		# select(treble, 31).dynamics = '!'
		# select(treble, 33).dynamics = '<'
		# select(treble, 35).dynamics = '!'
		# select(treble, 39).markdown = '\\italic{dim.}'
		# select(treble, 46).markdown = '\\italic{ten.}'

		# bass_harmony = rep(triple(notes('f,', 8)), 4*4) + triple(notes('f, fs, g, af, af, af, af,', 8)) + notes('af,', 8)
		# bass_melody = notes('bf,, b,,', 2) + notes('c, d, ef, a,, bf,, b,, c, d, ef, c, g,, a,, bf,, bf,, bf,, bf,, b,, c, cs,', 4) + notes('d,', 8)
		# bass_joined = notes('bf, bf c` af fs g af f d', 8) + voices(notes('ef c d g,', 8) + notes('f, ef', 4), rests(2, prefix='\\omit ') + notes('f,', 2))
		# select(bass_harmony, 1).suffix += ' ^\\p '
		# select(bass_melody, 1).ornamentation = '('
		# select(bass_melody, 6).ornamentation = ')'
		# select(bass_melody, 7).ornamentation = '('
		# select(bass_melody, 14).ornamentation = ')'
		# select(bass_melody, 19).ornamentation = '('
		# select(bass_melody, 22).ornamentation = ')'
		# select(bass_joined, 1).ornamentation = '('
		# select(bass_joined, 9).ornamentation = ')'
		# select(bass_joined, 10).ornamentation = '('
		# select(bass_joined, 15).ornamentation = ')'

		# chords4 = {
		# 	'treble': treble,
		# 	'bass': ottava(voices(bass_harmony, bass_melody), -1) + bass_joined
		# }

		# ############
		# # Chords 5 #
		# ############

		# bass = (
		# 	slur(notes('bf, d ef f g a', ['2.', 8, 8])) + slur(notes('bf d` c`', [2, '4.', 8])) + slur(notes('bf a af', [2, 4, 4])) +
		# 	slur(notes('g c` ef`', ['2.', 8, 8])) + slur(notes('ef` f bf d`', [4, 2, 8, 8])) + slur(notes('f ef d ef c', ['8.', 16, 2, 8, 8]))
		# )

		# treble = triple(chords(['f bf d` f`', 'f bf d` f`', 'f bf d` f`', 'f bf d` f`',
		# 						'bf c` f`', 'bf c` f`', 'a c` f`', 'c` f`',
		# 						'g d` f`', 'g d` f`', 'g bf e`', 'g bf e`',
		# 						'f c` f`', 'f c` f`', 'f c` f`', 'f c` f`',
		# 						'f b d` f`', 'f b d` f`', 'f c` ef` f`', 'f f`',
		# 						'f a c` f`', 'a c` ef` f`', 'bf d` f`', 'f f`',
		# 						'bf d` f`', 'f bf d` f`', 'f bf d` f`'
		# 						], 8)) + triplets(chords(['f a c` f`', 'f a c` f`', 'f a ef` f`'], 8))

		# select(treble, 1).dynamics = 'pp'
		# select(treble, 1).markup = '\\italic{sostenuto sempre}'

		# select(bass, 1).markdown = '\\italic{dolce cantabile}'
		# select(bass, 4).dynamics = '<'
		# select(bass, 7).dynamics = '!'
		# select(bass, 8).dynamics = '>'
		# select(bass, 11).dynamics = '!'
		# select(bass, 13).dynamics = '<'
		# select(bass, 15).dynamics = '!'
		# select(bass, 16).dynamics = '>'
		# select(bass, 17).dynamics = '<'
		# select(bass, 19).dynamics = '!'
		# select(bass, 20).dynamics = '>'
		# select(bass, 24).dynamics = '!'
		# select(bass, 24).suffix += ' \\pageBreak '

		# chords5 = {
		# 'treble': treble,
		# 'bass': bass
		# }

		# ####################
		# # Opening Chords 3 #
		# ####################

		# treble = (
		# 	chords(['g, bf,', 'a, c', 'bf, df', 'a, c', 'c ef', 'bf, df', 'ef gf', 'df f'], 2, ornamentation='arpeggio') +
		# 	chords(['f af', 'ef g', 'bf, d', 'bf, ef', 'g bf', 'f a', 'c e', 'c f', 'a c`', 'g bf', 'd fs', 'd g', 'b d`', 'a c`', 'ef gs', 'ef a'], 4, ornamentation='arpeggio')
		# )
		# bass = (
		# 	chords(['bf,, df, e,', 'f,, c, f,', 'bf,, e, g,', 'f,, c, f,', 'a,, c, gf,', 'bf,, df, f,', 'c, ef, af,', 'df, f, af,'], 2, ornamentation='arpeggio') +
		# 	chords(['d, f, bf,', 'ef, g, bf,', 'af,, bf,, f,', 'g,, bf,, ef,', 'e, g, c', 'f, a, c', 'bf,, c, g,', 'a,, c, f,', 'fs, a, d', 'g, bf, d', 'c, d, a,', 'bf,, d, g,', 'gf, b, ef', 'a, c ef', 'd, ef, b,', 'c, ef, a,'], 4, ornamentation='arpeggio')
		# )

		# select(treble, 1).articulation = '('
		# select(treble, 4).articulation = ')'
		# for i in [5, 7, 9, 11, 13, 15, 17, 19, 21, 23]:
		# 	select(treble, i).articulation = '('
		# 	select(treble, i+1).articulation = ')'
		# select(treble, 1).dynamics = 'p\\<'
		# for i in [3, 5, 7, 9, 13, 17, 21]:
		# 	select(treble, i).dynamics = '>'
		# 	select(treble, i+1).dynamics = '!'

		# select(treble, 11).markup = '\\italic{cresc - - - - - - - - - - - - - poco - - - - - - - a - - - - - - poco}'

		# treble2 = (
		# 	chords(
		# 		['ef f c` ef`', 'd f bf d`', 'g a c` ef` g`', 'f bf d` f`',
		# 		'a c` ef` f` a`', 'f bf d` f` bf`', 'ef` f` c`` ef``', 'd` f` bf` d``',
		# 		'g` a` c`` ef`` g``', 'f` bf` d`` f``', 'a` c`` ef`` f`` a``', 'f` bf` d`` f`` bf``',
		# 		'ef`` f`` c``` ef```', 'd`` f`` bf`` d```', 'ef`` a`` c``` ef```', 'ef`` a`` c``` ef``` e```',
		# 		'ef`` a`` c``` ef``` f```', 'ef`` a`` c``` ef``` e```', 'ef`` a`` c``` ef``` f```', 'ef`` a`` c``` ef``` fs```',
		# 		'ef`` a`` c``` ef``` f```', 'ef`` a`` c``` ef``` fs```', 'ef`` a`` c``` ef``` g```', 'ef`` a`` c``` ef``` fs```',
		# 		'ef`` a`` c``` ef``` g```', 'ef`` a`` c``` ef``` gs```'], 4, ornamentation = 'arpeggio') +
		# 	tied_note('a```', [2, 1, 1], ornamentation='startTrillSpan')
		# )
		# select(treble2, 29).prefix = '\\afterGrace ' + select(treble2, 29).prefix
		# select(treble2, 29).suffix += ' { g```16\\stopTrillSpan a```16 } '
		# select(treble2, 1).markup = "\\italic{sostenuto}"
		# select(treble2, 1).prefix = "\\set Staff.pedalSustainStyle = #'mixed " + select(treble2, 1).prefix
		# select(treble2, 1).suffix = '\\sustainOn '
		# for i in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]:
		# 	select(treble2, i).suffix = '\\sustainOn\\sustainOff '
		# select(treble2, 7).markdown = "\\italic{sempre cresc}"
		# select(treble2, 15).suffix = '\\sustainOff '
		# select(treble2, 15).markdown = 'Ped. \\italic{sempre}'
		# select(treble2, 15).dynamics = 'f'
		# select(treble2, 17).markup = '\\italic{poco accel.}'
		# select(treble2, 18).markdown = '\\italic{sempre cresc.}'
		# select(treble2, 23).dynamics = '<'
		# select(treble2, 27).dynamics = 'sf'

		# bass2 = (
		# 	chords(
		# 		['a,, c, ef, f, a,', 'bf,, d, f, bf,', 'c, ef, f, a, ef', 'd, f, bf, d',
		# 		'f, a, c, ef f', 'bf,, d, f, bf, d', 'a, c ef f a', 'bf, d f bf',
		# 		'c ef f a ef`', 'd f bf d`', 'f a c ef` f`', 'bf, d f bf d`',
		# 		'a c` ef` f` a`', 'bf d` f` bf`', 'f a c` ef` a`', 'f a c` ef` a`',
		# 		'f a c` ef` a`', 'f a c` ef` a`', 'f a c` ef` a`', 'f a c` ef` a`',
		# 		'f, a, c ef a', 'f a c` ef` a`', 'f a c` ef` a`', 'f, a, c ef a',
		# 		'f, a, c ef a', 'f a c` ef` a`', 'f` a` c`` ef`` a``', 'f a c` ef` a`',
		# 		'f, a, c ef a', 'f a c` ef` a`', 'f, a, c ef a', 'f,, a,, c, ef, a,',
		# 		'f, a, c ef a', 'f, ef g', 'f, d f', 'f c ef'], 4, ornamentation='arpeggio')
		# )

		# select(bass2, 28).dynamics = 'ff'
		# select(bass2, 29).markdown = '\\italic{dim poco a poco}'
		# select(bass2, 33).markdown = 'Ped. \\italic{sempre}'
		# select(bass2, 33).markup = '\\italic{poco ritard}'
		# select(bass2, 33).dynamics = '>'
		# select(bass2, 35).prefix = '\\set Staff.pedalSustainStyle = #\'text '
		# select(bass2, 35).suffix = '\\omit \\sustainOn '
		# select(bass2, 36).dynamics = '!'
		# select(bass2, 36).suffix = '\\sustainOff \\break'

		# treble_tones = tonify('f` bf` d`` f`` bf`` d``` f``` bf```')
		# bass_tones = tonify('bf,, d, f, bf, d f bf d`')

		# treble3 = [chord(subset(treble_tones, max(i-3, 1), i), 4, ornamentation='arpeggio') for i in [8, 7, 6, 5, 4, 3, 2, 3, 4, 5, 6, 7]]
		# bass3 = [chord(subset(bass_tones, i, min(i+3, 8)), 4, ornamentation='arpeggio') for i in [1, 2, 3, 4, 5, 6, 7, 6, 5, 4, 3, 2]]

		# select(treble3, 1).dynamics = 'p'
		# select(treble3, 1).markup = '\\italic{a tempo}'
		# select(treble3, 1).markdown = 'Ped. \\italic{sempre}'
		# select(bass3, 12).suffix = ' \\break '

		# ending = voices(
		# 	chords(['bf`` d``` f``` bf```', 'f`` bf`` d``` f```', 'd`` f`` bf`` d```'], 1) + rests(1, prefix ='\\omit '),
		# 	chords(['bf,, d, f, bf,'], [1, 1, 1]) + rests(1, prefix='\\omit '),
		# 	rests(4, 8, prefix ='\\omit ') + slur(notes('f f`', [8, 2])) + rests(4, 8, prefix ='\\omit ') + slur(notes('d` d``', [8, 2])) + rests(4, 8, prefix ='\\omit ') + notes('bf` bf`` bf``', [8, 2, 1])
		# )
		# select(ending, 1).prefix = '\\set Staff.connectArpeggios = ##f ' + select(ending, 1).prefix
		# select(ending, 1).ornamentation = 'arpeggio'
		# select(ending, 2).markdown = '\\italic{smorzando}'
		# select(ending, 5).ornamentation = 'arpeggio'
		# select(ending, 11).dynamics = '<'
		# select(ending, 12).dynamics = '!'
		# select(ending, 15).dynamics = '<'
		# select(ending, 16).dynamics = '!'
		# select(ending, 19).dynamics = '<'
		# select(ending, 19).articulation = '('
		# select(ending, 20).dynamics = '!'
		# select(ending, 20).articulation = '~-)'

		# ending2 = voices(
		# 	chords(['d f bf d`'], [2, 2, 1]),
		# 	chords(['bf,, bf,'], [2, 2]) + chords(['bf,, f, bf,'], 1)
		# )

		# select(ending2, 1).dynamics = 'ppp'
		# select(ending2, 1).suffix += '\\omit \\sustainOn '
		# select(ending2, 1).prefix = '\\set Staff.connectArpeggios = ##t ' + select(ending2, 1).prefix
		# select(ending2, 3).ornamentation = 'arpeggio'
		# select(ending2, 6).suffix += ' \\bar "|." '
		# select(ending2, 3).suffix = '\\sustainOff ' + select(ending2, 3).suffix
		# select(ending2, 6).ornamentation = 'arpeggio\\fermata'
		

		# opening_chords3 = {
		# 	'treble': ottava(voices(treble, bass), -1) + voices(treble2 + treble3, bass2 + bass3) + ending + ending2,
		# 	'bass': rep(rests(1), 24)
		# }

		self.score = join(opening_chords, melody1, opening_chords2, melody2, chords1) # chords2, chords3, plods, bridge, chords4, chords5, opening_chords3)

	def end_score(self):
		if self.improvements:
			return '>> \\layout { } \\midi { } }'
		else:
			return '>>\n>> \\layout { } \\midi { } }'

if __name__ == "__main__":
	Salut()
