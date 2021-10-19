from piece import Piece
from points import rest, rests, note, notes, tied_note, chords, chord, arpeggio, diminished7, scale, transpose, add, merge, tied_chord
from staves import Bass, Super
from markup import voices, ottava, clef, key_signature, triplets, linebreak, nolinebreak, grace, pagebreak
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
		self.opus = "45"
		self.key = "Bf major"
		self.auto_add_bars = True
		self.staves=[Super('treble'), Bass()]
		self.staves[0].extra_text += '\\set Score.connectArpeggios = ##t'

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

# piece is in G minor or Bf Major
# V: D Minor or F Major
# IV: C minor or Ef Major

	def write_score(self):

		##################
		# Opening Chords #
		##################

		def rolled_chords(chord1, chord2):
			return {
				'treble': rests(1, 2, 4, 8),
				'bass': ottava(voices(
					[chord1.select(4, 5), chord2.select(4, 5), chord1.select(5, 6), chord2.select(4, 5)],
					[chord1.subset(1, 3), chord2.subset(1, 3), chord1.select(1, 3, 4), chord2.subset(1, 3)]
				), -1)
			}

		dim7 = chord(self.diminished7('bf,,', 6), 2, ornamentation="arpeggio")
		dim7.replace('ff, aff,', 'e, g,')
		fmaj = chord(omit(arpeggio('f,,', 6, key='f major'), 2), 2, ornamentation="arpeggio")

		opening_chords = rolled_chords(dim7, fmaj)
		select(opening_chords['treble'], 1).prefix = '\\tempo 4 = 69'
		select(opening_chords['treble'], 1).prefix += ' \\override Rest.transparent = ##t '
		select(opening_chords['treble'], 1).markup = "\\italic{adagio sostenuto}"
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
				select(melody, 2).phrasing += '~'
				select(melody, 4).dynamics = '!'
			else:
				select(melody, 8).phrasing += "~"
				select(melody, 5).dynamics = '!'
			select(melody, len(melody)).articulation += ')'
			return(melody)

		upper_treble_voice = melody('f`', [2, '4.'], self.key) + melody('c`', ['2.', 4], self.key)
		select(upper_treble_voice, len(upper_treble_voice)).replace('ef', 'e')
		lower_treble_voice = rests(8, 4) + notes('c` bf g f e f ef', 4) + rests(4) + notes('e f d c b,', 4) + notes('bf,', 2)
		select(lower_treble_voice, 4).add('d`')
		select(lower_treble_voice, 12).add('a')

		melody1 = {
			'treble': voices(
				upper_treble_voice,
				lower_treble_voice
			),
			'bass': (
				rests(4) + notes('a, bf,', 4) +
				voices(self.chromatic('ef', -4, dur=[4, 4, 4, '4.']) + rests(8), notes('ef, f, fs,', [4, '2.', 4])) +
				rests(4) + notes('g, a,', 4) +
				voices(self.chromatic('bf,', -4, dur=[4, 4, 4, 2]), notes('bf,, c, c,', [4, '2.', 4]))
			)
		}

		select(melody1['treble'], 1).markup = '\\italic{Voce principale \\bold{p} e dolce cantabile}'
		select(melody1['treble'], 2).markdown = '\\italic{Altre voci \\bold{pp} e legatissimo}'
		select(melody1['treble'], 17).prefix += ' \\hide '
		select(melody1['treble'], len(melody1['treble'])).suffix += linebreak

		select(melody1['bass'], 4).ornamentation = '('
		select(melody1['bass'], 7).ornamentation = ')'
		select(melody1['bass'], 9).ornamentation = '('
		select(melody1['bass'], 11).ornamentation = ')'
		select(melody1['bass'], 15).ornamentation = '('
		select(melody1['bass'], 18).ornamentation = ')'
		select(melody1['bass'], 19).ornamentation = '('
		select(melody1['bass'], 21).ornamentation = ')'

		####################
		# Opening Chords 2 #
		####################

		dim7 = chord(diminished7('f,,', 6, key='f minor'), 2, ornamentation="arpeggio")
		dim7.replace('cf, eff,', 'b,, d,')
		cmaj = chord(omit(arpeggio('c,,', 6, key='c major'), 2), 2, ornamentation="arpeggio")
		opening_chords2 = rolled_chords(dim7, cmaj)

		select(opening_chords2['treble'], 1).prefix += ' \\override Rest.transparent = ##t '
		select(opening_chords2['treble'], 1).dynamics = "mf"
		select(opening_chords2['bass'], 2).suffix = nolinebreak

		############
		# Melody 2 #
		############

		lower_treble_voice = rests(8, 4) + chords(['ef` gf`', 'df` f`'], 4) + notes('bf af g af af', 4) + rests(4) + chords(['e c`', 'e cs`'], 4) + notes('fs e fs d', [4, 4, 4, 2])

		melody2 = {
			'treble': voices(
				melody('af`', [2, '4.'], 'bf minor') + melody('e`', ['2.', 4], 'a major', True),
				lower_treble_voice
			),
			'bass': rests(4) + voices(
				notes('af gf, gf f e ef   d cs d, d cs d b, e,', [2, 8, 8, 4, 4, '4.', 8, 4, 4, 4, 8, 8, 4, 4, 4, 4]),
				notes('c df gf, af, af,  gs, a, d, e, e,', [4, 4, 4, '2.', 4, 4, 4, 4, 4, '2.', 4])
			) 
		}

		select(melody2['treble'], 1).dynamics = 'p'
		select(melody2['treble'], 1).markup = '\\italic{dolce}'
		select(melody2['treble'], 18).markdown = '\\italic{ten.}'
		select(melody2['treble'], 21).prefix += ' \\hide '
		select(melody2['treble'], 23).dynamics = 'pp'
		select(melody2['treble'], len(melody2['treble'])).suffix += linebreak

		select(melody2['treble'], 1).suffix = nolinebreak
		select(melody2['treble'], 6).suffix = nolinebreak
		select(melody2['treble'], 9).suffix = nolinebreak
		select(melody2['treble'], 15).suffix = nolinebreak

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

		upper_treble4 = notes('a cs` d` e` fs` gs`', ['2.', 8, 8]) + notes('a` b` fs` a` gs` g`', [2, '4.', 8, 2, 4, 4])
		lower_treble4 = triple(chords(['cs e', 'cs e', 'cs e', 'e a', 'e b', 'e gs b', 'e gs b', 'b e`', 'a cs`', 'a cs`', 'b d` fs`', 'b d`', 'cs` e`', 'a cs` e`', 'gs b e`', 'g b e`'], 8))
		bass4 = triple_octaves('a, e cs a, gs, b, gs, e fs, a, d, fs, e, ds e') + triple(chord('e, d', 8))

		select(lower_treble4, 1).markdown = '\\italic{sempre sostenuto e poco cres.}'
		select(lower_treble4, 25).dynamics = '<'
		select(lower_treble4, 31).dynamics = '!\\>'
		select(lower_treble4, 36).dynamics = '!'

		upper_treble8 = notes('fs` b` d``', ['2.', 8, 8]) + notes('d`` e` a` cs`` cs`` d` cs` e`', [4, 2, 8, 8]) + notes('cs` b c`', [2, 4, 4])
		lower_treble8 = triple(chords(['fs as cs`', 'fs as cs`', 'fs b d`', 'd` fs`', 'd` e`', 'e gs b', 'e a cs`', 'cs` e`', 'd` a`', 'e b', 'e b', 'e a', 'e a', 'fs a', 'gs', 'fs gs'], 8))
		bass8 = add(triple(notes('cs e d b, gs, d cs a, fs,', 8)) + triple_octaves('gs, a, cs') + triple(notes('e, ds e', 8)), 'e,') + triple_octaves('d')

		select(upper_treble8, 4).dynamics = '>'
		select(upper_treble8, 5).dynamics = '!\\<'
		select(upper_treble8, 7).dynamics = '!'
		select(upper_treble8, 8).dynamics = '>'
		select(upper_treble8, 9).dynamics = '!'
		select(lower_treble8, 1).dynamics = '<'
		select(lower_treble8, 11).dynamics = '!'
		select(lower_treble8, 29).markdown = '\\italic{dim.}'
		select(lower_treble8, 37).dynamics = '>'
		select(lower_treble8, 43).dynamics = '!'
		select(lower_treble8, 46).dynamics = 'p'

		upper_treble12 = notes('cs` es` fs` gs` as` bs`', ['2.', 8, 8]) + notes('cs`` es`` ds``', [2, '4.', 8]) + notes('cs`` bs` b`', [2, 4, 4])
		lower_treble12 = triple(chords(['es gs', 'es gs', 'es gs', 'es gs cs`', 'gs ds`', 'gs bs ds`', 'gs bs ds`', 'bs ds` gs`', 'ds` as`', 'ds` fss` as`', 'fss` as` cs``', 'ds` as` cs``', 'ds` fss` as`', 'ds` fss` as`', 'ds` gs`', 'ds` gs`'], 8))
		bass12 = add(triple_octaves('cs gs es cs bs, ds bs, gs,'), 'gs,') + add(triple_octaves('fss, as, ds, fss,'), 'ds,') + add(triple_octaves('ds'), 'gs,') + triple_octaves('ds') + add(triple_octaves('gs'), 'ds') + add(triple(notes('b', 8)), 'gs')

		select(upper_treble12, 1).markdown = "\\italic{cres. poco a poco}"
		select(upper_treble12, 1).markup = "Gs Major"
		select(upper_treble12, 7).dynamics = "<"
		select(upper_treble12, 8).dynamics = "rfz"
		select(upper_treble12, 10).dynamics = ">"
		select(upper_treble12, 12).dynamics = "p"

		upper_treble16 = notes('b` e`` g``', ['2.', 8, 8]) + notes('g`` g` c`` e`` e`` e` a` c``', [4, 2, 8, 8]) + notes('c`', [2, '4.', 8])
		lower_treble16 = triple(chords(['ds` fs`', 'ds` a`', 'e` g`', 'g` b`', 'g` b` d``', 'b f`', 'c` e`', 'e` g`', 'e` gs`', 'fs d`', 'a c`', 'c` e`', 'f a', 'f a', 'e g', 'g bf'], 8))
		bass16 = add(triple(notes('a fs g e', 8)), 'b') + add(triple(chords(['f b', 'ds g', 'e', 'c'], 8)), 'g') + add(triple(notes('d b, c a,', 8)), 'e') + triple(chords(['f, c']*4, 8))

		select(lower_treble16, 1).markup = 'E Minor'
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

		upper_treble19 = notes('c` f` ef` df` g a bf', 4) + chords(['bf d`', 'a c`'], 8) + notes('bf a', [2, 4])
		lower_treble19 = triple(chords(['f a', 'f c`', 'f c`', 'f bf', 'f', 'f g', 'e g', 'e', 'e g', 'e g', 'f'], 8))
		bass19 = triple(chords(['f, c'], 8)) + triple_octaves('a, bf, df c c c c') + triple(chords(['f, c', 'c, f, c', 'f, c'], 8))

		select(lower_treble19, 4).dynamics = '>'
		select(lower_treble19, 12).dynamics = '!'
		select(lower_treble19, 13).dynamics = '<'
		select(lower_treble19, 22).dynamics = '!\\>'
		select(lower_treble19, 24).dynamics = '!'

		chords1 = {
			'treble':key_signature(self.key, voices(
				upper_treble4 + upper_treble8 + upper_treble12 + upper_treble16 + upper_treble19,
				lower_treble4 + lower_treble8 + lower_treble12 + lower_treble16 + lower_treble19
			)),
			'bass': key_signature(self.key, bass4 + bass8 + bass12 + bass16 + bass19)
		}

		############
		# Chords 2 #
		############

		self.set_key('bf major')

		def f_octave(dur):
			return [note('f', 8, articulation="("), note('f`', dur, articulation=')')]

		upper_bass = chords(['c ef', 'bf, d', 'gs, b,', 'a, c', 'd f', 'c ef', 'a, cs', 'bf, d', 'ef g', 'c ef', 'a, f', 'bf, d', 'g, ef', 'a, c'], 4)
		select(upper_bass, 1).articulation = '('
		select(upper_bass, 4).articulation = ')'
		select(upper_bass, 5).articulation = '('
		select(upper_bass, 8).articulation = ')'
		select(upper_bass, 8).markup = '\\italic{poco cresc.}'
		select(upper_bass, 9).articulation = '('
		select(upper_bass, 14).articulation = ')'

		chords2 = {
			'treble': rep(rests(8) + f_octave('2.'), 2) + rests(8) + rep(f_octave('4.'), 2),
			'bass': voices(upper_bass, rep(triple(notes('f,', 8)), 14))
		}

		select(chords2['treble'], 1).prefix += ' \\override Rest.transparent = ##f '
		select(chords2['treble'], 1).dynamics = 'p'

		############
		# Chords 3 #
		############

		upper_treble = subset(melody('f`', [2, 8], self.key), 1, 6) + tied_note('bf', [2, 8]) + notes('a g a', 8)
		select(upper_treble, 7).articulation = ')-('
		select(upper_treble, 11).articulation = ')'

		lower_treble = rests(8, 4) + triple(notes('af g g f e ef c', 8))
		select(lower_treble, 1).prefix += ' \\override Rest.transparent = ##t '
		select(lower_treble, 14).markdown = '\\italic{smorz.}'

		bass = merge(triple(notes('d, ef, ef,', 8)), notes('bf, bf, bf, bf, bf, b, c c ef,', 8)) + add(triple(notes('d cs c ef', 8)), 'f,')

		chords3 = {
			'treble': voices(upper_treble, lower_treble),
			'bass': bass
		}

		#########
		# Plods #
		#########

		self.set_key('b major')

		def plod(tones):
			tones = tonify(tones)
			return grace(notes(tones, 16)) + notes(select(tonify(tones), 1), 8) + rests(8)

		def octoplod(tones):
			plink = plod(tones)
			select(plink, 3).add(self.transpose(select(tonify(tones), 1), 1, 'octave'))
			return plink

		def superoctoplod(tones):
			plink = octoplod(tones)
			select(plink, 1).add(self.transpose(select(tonify(tones), 1), 1, 'octave'))
			return plink

		def harmoplod(tones):
			tones = tonify(tones)
			plink = plod(subset(tones, 1, 2))
			select(plink, 3).add(select(tones, 3))
			return plink

		def harmoctoplod(tones):
			tones = tonify(tones)
			plink = superoctoplod(subset(tones, 1, 2))
			select(plink, 1).add(select(tones, 3))
			select(plink, 3).add(select(tones, 3))
			return plink


		def treble_plod(one, two, three, held_note=2):
			if len(one) == 3:
				melody = chords(one, 8)
			elif len(one) == 2:
				tones = tonify(select(one, 1))
				melody = chords([subset(tones, 1, 3), subset(tones, 2, 4), select(one, 2)], 8)
			elif len(one) == 1:
				tones = tonify(select(one, 1))
				melody = chords([subset(tones, 1, 3), subset(tones, 2, 4), subset(tones, 3, 5)], 8)
			melody = triplets(melody)

			vs = voices(chords([omit(select(melody, 3).tones, held_note), two], ['4.', 8]), notes(select(select(melody, 3).tones, held_note), 2))
			select(vs, 1).articulation = '('
			select(vs, 2).articulation = ')'
			melody += vs + chords([three], 4)
			return melody

		def extended_treble_plod(one, two, three, four, five, six, seven, eight):
			melody = treble_plod(one, two, three)
			melody = (
				subset(melody, 1, 3) + chords([select(melody, 3).tones, two, three, three], [4, '8.', 16, 4]) +
				chords([four, five, six, seven, eight], [8, 8, '8.', 16, 4]) + rests(4)
			)
			select(melody, 4).articulation = '('
			select(melody, 5).articulation = ')'
			select(melody, 7).articulation = '('
			select(melody, 8).articulation = ')'
			select(melody, 10).articulation = '('
			select(melody, 12).articulation = ')'
			return melody

		def mini_treble_plod(one, two, three, alt=False):
			tones = tonify(select(one, 1))
			melody = (
				triplets(chords([subset(tones, 1, 3), subset(tones, 2, 4), subset(tones, 3, 5)], 8)) +
				chords([two], '8.', articulation='(') + chords([three], 16, articulation=')')
			)
			if not alt:
				return melody + chords([two], 2)
			else:
				tones = tonify(two)
				return (
					melody + 
					voices(chords([select(tones, 1, 3), three], ['4.', 8]), chords([select(tones, 2)], 2)) +
					tied_chord(two, [4, 8]) + chords([three], 8) + rep(chords([two], 8, articulation="(") + chords([three], 8, articulation=")"), 3)
				)

		treble = (
			rests(2, 4) + treble_plod(['as, cs fs as', 'e fs cs`'], 'd fs b', 'cs fs as') +
			treble_plod(['cs fs as', 'e fs cs`', 'g as e`'], 'fs d`', 'e a cs`') +
			extended_treble_plod(['e as cs`', 'g as e`', 'as e` g`'], 'as d` fs`', 'g as e`', 'fs as d`', 'e as cs`', 'd fs b', 'cs`', 'cs fs as') +
			treble_plod(['b, d fs b d`'], 'e cs`', 'd fs b', held_note=1) + treble_plod(['d d fs b d`'], 'e cs`', 'd fs b', held_note=1) +
			extended_treble_plod(['fs b d` fs` b`'], 'b d` g`', 'b d` fs`', 'g b e`', 'fs b d`', 'g as cs`', 'd`', 'd fs b') +
			treble_plod(['d es gs b d`'], 'as cs`', 'es gs b') + treble_plod(['es gs b d` es`'], 'cs` e`', 'gs b d`') +
			extended_treble_plod(['gs b d` es`', 'b d` es` gs`', 'd` es` gs` b`'], 'a d` fs` a`', 'fs a d` fs`', 'e a e`', 'd a d', 'ds a bs', 'e cs`', 'ds a bs') +
			mini_treble_plod(['ds a bs ds` a`'], 'ds` a` bs`', 'e` cs``') + mini_treble_plod(['ds` a` bs` ds`` a``'], 'ds`` a`` bs``', 'e`` cs```', alt=True) +
			merge(self.chromatic('ds``', -8, 8), self.chromatic('a``', -8, 8), self.chromatic('c```', -8, 8)) + 
			merge(self.chromatic('fs``', -8, 8), self.chromatic('c```', -8, 8), self.chromatic('ds```', -8, 8)) + 
			chords([subset(tonify('bs ds` fs` a` bs` ds`` fs`` a`` bs`` ds``` fs```'), i, i+3) for i in [8, 7, 6, 5, 4, 3, 2, 1]], 8) +
			chords(['as cs` e` g`', 'gs b d` f`', 'fs a c` ef`', 'es gs b d`'], 4, articulation='^') +
			chords(['ef fs a c`', 'd es gs b', 'as, cs fs', 'bf, df gf', 'bf, df gf', 'bf, df f'], [2, 2, 1]) + 
			voices(notes('e', 1), notes('df', 2, articulation='(') + notes('c', 4) + notes('bf,', 4, articulation=')'))
		)
		select(treble, 40).replace('b', 'fs`')
		select(treble, 42).replace('fs', 'b')
		select(treble, 74).tones = tonify('d` fs` a` d``')


		bass = (
			rep(plod('fs,, es,,'), 44) + rep(octoplod('fs,, es,,'), 20) +
			rep(superoctoplod('fs,, es,,'), 8) + rep(harmoctoplod('fs,, es,, cs,'), 4) + rep(superoctoplod('fs,, es,,'), 8) +
			rep(octoplod('fs,, es,,'), 8) + rep(harmoplod('fs,, es,, cs,'), 4) +
			rep(harmoplod('fs,, es,, as,,'), 4)
		)

		plods = {
			'treble': key_signature(self.key, treble),
			'bass': key_signature(self.key, ottava(bass, -1))
		}




		self.score = join(opening_chords, melody1, opening_chords2, melody2, chords1, chords2, chords3, plods)

if __name__ == "__main__":
	Salut()
