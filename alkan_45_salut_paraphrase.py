from piece import Piece
from points import rest, rests, note, notes, tied_note, chords, chord, arpeggio
from staves import Bass, Super
from markup import voices, ottava, clef
from util import join, rep, pattern, omit, select

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
		self.key = "G Minor"
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

		dim7 = chord(self.diminished7('bf,,', 6), 2, ornamentation="arpeggio")
		dim7.replace('ff,', 'e,')
		fmaj = chord(omit(arpeggio('f,,', 6, key='f major'), 2), 2, ornamentation="arpeggio")

		opening_chords = {
			'treble': rests(1, 2, 4, 8),
			'bass': ottava(voices(
				[dim7.select(4, 5), fmaj.select(4, 5), dim7.select(5, 6), fmaj.select(4, 5)],
				[dim7.subset(1, 3), fmaj.subset(1, 3), dim7.select(1, 3, 4), fmaj.subset(1, 3)]
			), -1)
		}
		select(opening_chords['treble'], 1).prefix = '\\tempo 4 = 69'
		select(opening_chords['treble'], 1).prefix += ' \\override Rest.transparent = ##t '
		select(opening_chords['treble'], 1).markup = "\\italic{adagio sostenuto}"
		select(opening_chords['treble'], 1).dynamics = "mf"

		############
		# Melody 1 #
		############

		def melody1(tone, durs):
			tones = self.scale(self.transpose(tone, -1, 'octave'), 9)
			melody = notes(pattern(tones, 1, 8, 8, 9, 7, 5, 4, 3), [8, 2, 8, 8, 8, 8]+durs)
			select(melody, 1).ornamentation += '('
			select(melody, 2).phrasing += '~'
			select(melody, len(melody)).ornamentation += ')'
			return(melody)

		lower_treble_voice = rests(8, 4) + notes('c` bf g f e f ef', 4) + rests(4) + notes('e f d c b,', 4) + notes('bf,', 2)
		select(lower_treble_voice, 4).add('d`')
		select(lower_treble_voice, 12).add('a')

		melody1 = {
			'treble': voices(
				melody1('f`', [2, '4.']) + melody1('c`', ['2.', 4]),
				lower_treble_voice
			),
			'bass': (
				rests(4) + notes('a, bf,', 4) +
				voices(self.chromatic('ef', -4, dur=[4, 4, 4, '4.']) + rests(8), self.chromatic('ef,', 3, dur=[4, '2.', 4])) +
				rests(4) + notes('g, a,', 4) +
				voices(self.chromatic('bf,', -4, dur=[4, 4, 4, 2]), notes('bf,, c, c,', [4, '2.', 4]))
			)
		}

		select(melody1['treble'], 1).dynamics = 'p'
		select(melody1['treble'], 2).markup = '\\italic{Dolce cantabile e legatissimo}'
		select(melody1['treble'], 2).dynamics = '<'
		select(melody1['treble'], 4).dynamics = '!\\>'
		select(melody1['treble'], 6).dynamics = '!'
		select(melody1['treble'], 10).dynamics = '<'
		select(melody1['treble'], 12).dynamics = '!\\>'
		select(melody1['treble'], 14).dynamics = '!'
		select(melody1['treble'], 17).prefix += ' \\hide '

		select(melody1['bass'], 4).ornamentation = '('
		select(melody1['bass'], 7).ornamentation = ')'
		select(melody1['bass'], 9).ornamentation = '('
		select(melody1['bass'], 11).ornamentation = ')'
		select(melody1['bass'], 15).ornamentation = '('
		select(melody1['bass'], 18).ornamentation = ')'
		select(melody1['bass'], 19).ornamentation = '('
		select(melody1['bass'], 21).ornamentation = ')'

		self.score = join(opening_chords, melody1)

if __name__ == "__main__":
	Salut()
