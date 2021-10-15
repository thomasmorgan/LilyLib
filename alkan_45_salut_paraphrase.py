from piece import Piece
from points import rest, rests, note, notes, tied_note, chords, chord, arpeggio, diminished7, scale, transpose, add
from staves import Bass, Super
from markup import voices, ottava, clef, key_signature, triplets, linebreak, nolinebreak
from util import join, rep, pattern, omit, select, rep, flatten
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

			select(melody, 1).ornamentation += '('
			select(melody, 2).suffix = '^\\<'
			if not alt:
				select(melody, 2).phrasing += '~'
				select(melody, 4).suffix = '^\\!'
			else:
				select(melody, 8).phrasing += "~"
				select(melody, 5).suffix = '^\\!'
			select(melody, len(melody)).ornamentation += ')'
			return(melody)

		lower_treble_voice = rests(8, 4) + notes('c` bf g f e f ef', 4) + rests(4) + notes('e f d c b,', 4) + notes('bf,', 2)
		select(lower_treble_voice, 4).add('d`')
		select(lower_treble_voice, 12).add('a')

		melody1 = {
			'treble': voices(
				melody('f`', [2, '4.'], self.key) + melody('c`', ['2.', 4], self.key),
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

		select(melody2['treble'], 1).markup = '\\italic{\\bold{p} e dolce}'
		select(melody2['treble'], 18).markdown = '\\italic{tenuto}'
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
			return flatten([triplets(rep(point, 3)) for point in flatten([points])])

		def triple_octaves(tones):
			return flatten([triple(octave(t)) for t in tonify(tones)])

		upper_treble4 = notes('a cs` d` e` fs` gs`', ['2.', 8, 8]) + notes('a` b` fs` a` gs` g`', [2, '4.', 8, 2, 4, 4])
		lower_treble4 = triple(chords(['cs e', 'cs e', 'cs e', 'e a', 'e b', 'e gs b', 'e gs b', 'b e`', 'a cs`', 'a cs`', 'b d` fs`', 'b d`', 'cs` e`', 'a cs` e`', 'gs b e`', 'g b e`'], 8))
		bass4 = triple_octaves('a, e cs a, gs, b, gs, e fs, a, d, fs, e, ds e') + triple(chord('e, d', 8))

		select(upper_treble4, 1).markup = '\\italic{Sempre sostenuto}'
		select(lower_treble4, 1).markdown = '\\italic{Poco crescendo}'
		select(lower_treble4, 25).dynamics = '<'
		select(lower_treble4, 31).dynamics = '!\\>'
		select(lower_treble4, 36).dynamics = '!'
		select(bass4, 1).markdown = 'Ped: \\italic{sostenuto}'

		upper_treble8 = notes('gs` b` d``', ['2.', 8, 8]) + notes('d`` e` a` cs`` cs`` d` cs` e`', [4, 2, 8, 8]) + notes('cs` b c`', [2, 4, 4])
		lower_treble8 = triple(chords(['fs as cs`', 'fs as cs`', 'fs b d`', 'd` fs`', 'd` e`', 'e gs b', 'e a cs`', 'cs` e`', 'd` a`', 'e b', 'e b', 'e a', 'e a', 'fs a', 'gs', 'fs gs'], 8))
		bass8 = add(triple(notes('cs e d b, gs, d cs a, fs,', 8)) + triple_octaves('gs, a, cs') + triple(notes('e, ds e', 8)), 'e,') + triple_octaves('d')

		select(upper_treble8, 4).dynamics = '>'
		select(upper_treble8, 5).dynamics = '!\\<'
		select(upper_treble8, 7).dynamics = '!'
		select(upper_treble8, 8).dynamics = '>'
		select(upper_treble8, 9).dynamics = '!'
		select(upper_treble8, 9).markdown = '\\italic{dim.}'
		select(lower_treble8, 1).dynamics = '<'
		select(lower_treble8, 11).dynamics = '!'
		select(lower_treble8, 37).dynamics = '>'
		select(lower_treble8, 43).dynamics = '!'
		select(lower_treble8, 46).dynamics = 'p'

		chords1 = {
			'treble':key_signature(self.key, voices(upper_treble4 + upper_treble8, lower_treble4 + lower_treble8)),
			'bass': key_signature(self.key, bass4 + bass8)
		}




		self.score = join(opening_chords, melody1, opening_chords2, melody2, chords1)

if __name__ == "__main__":
	Salut()
