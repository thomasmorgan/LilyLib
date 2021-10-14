from piece import Piece
from points import rest, rests, note, notes, tied_note, chords, chord, arpeggio, diminished7, scale, transpose
from staves import Bass, Super
from markup import voices, ottava, clef, key_signature, triplets
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

		############
		# Melody 2 #
		############

		lower_treble_voice = rests(8, 4) + notes('ef` df` bf af g af af', 4) + rests(4) + chords(['e c`', 'e cs`'], 4) + notes('fs e fs d', [4, 4, 4, 2])

		melody2 = {
			'treble': voices(
				melody('af`', [2, '4.'], 'bf minor') + melody('e`', ['2.', 4], 'a major', True),
				lower_treble_voice
			),
			'bass': rests(4) + voices(
				notes('af gf, gf f e ef   d cs d, d cs d b, e,', [2, 8, 8, 4, 4, '4.', 8, 4, 4, 4, 8, 8, 4, 4, 4, 4]),
				notes('c df gf, af, gs,  gs, a, d, e, e,', [4, 4, 4, '2.', 4, 4, 4, 4, 4, '2.', 4])
			) 
		}

		select(melody2['treble'], 1).markup = '\\italic{\\bold{p} e dolce}'
		select(melody2['treble'], 18).markdown = '\\italic{tenuto}'
		select(melody2['treble'], 21).prefix += ' \\hide '
		select(melody2['treble'], 23).dynamics = 'pp'

		############
		# Chords 1 #
		############

		self.set_key('a major')

		def octave(tone):
			return chord([tone, transpose(tone, -1, 'a major', 'octave')], 8)

		def triple(point):
			return triplets(rep(point, 3))

		def triple_octaves(tones):
			return flatten([triple(octave(t)) for t in tonify(tones)])

		upper_treble = notes('a cs` d` e` fs` gs`', ['2.', 8, 8]) + notes('a` b` gs` a` gs` g', [2, '4.', 8, 2, 4, 4])
		lower_treble = triple_octaves('a, e cs a, gs, b, gs, e fs, a, d, fs, e, ds e d')

		chords1 = {
			'treble':key_signature(self.key, voices(upper_treble, lower_treble)),
			'bass': key_signature(self.key, rests(1, 1, 1, 1))
		}




		self.score = join(opening_chords, melody1, opening_chords2, melody2, chords1)

if __name__ == "__main__":
	Salut()
