from piece import Piece
from points import (notes, tied_note, chords, rests, add, merge, scale,
                    transpose)
from staves import Treble, Super, Bass
from markup import voices
from util import select, omit, flatten


class GenreAncien(Piece):

    def details(self):
        self.title = "No. 3"
        self.subtitle = "Dans le genre ancien"
        self.composer = "Charles-Valentin Alkan"
        self.date = "1847"
        self.mutopiacomposer = "AlkanCV"
        self.mutopiainstrument = "piano"
        self.source = "A.M. Schlesinger, 1847"
        self.style = "Romantic"
        self.license = "Creative Commons Attribution-ShareAlike 4.0"
        self.maintainer = "Thomas Morgan"
        self.mantainer_email = "thomas.j.h.morgan@gmail.com"
        self.opus = "Op. 31, No. 3"
        self.auto_add_bars = True
        self.key = 'bf minor'
        self.improvements = False
        if self.improvements:
            self.staves = [Treble("treble"), Super("middle"), Bass("bass")]

    def subtext(self):
        return (
          "\\layout { \\context { \\PianoStaff "
          "\\consists #Span_stem_engraver } }\n"
          "\\layout { \\context { \\Staff \\RemoveEmptyStaves } }\n")

    def write_score(self):

        # section 1

        upper_melody = [
            [],
            notes('af` df`` f``', [2, 4, 4]),
            notes('f`` ef`` gf``', [2, 4, 4]),
            notes('gf`` ef`` df`` c``', 4),
            notes('af`` f`` ef`` d``', 4),
            notes('bf`` gf`` ef``', [2, 4, 4]),
            notes('ef```', '4.') + self.scale('df```', -5, 8),
            notes('f`` ef`` df`` ef`` c`` df``', [8, 8, 8, 8, '4.', 8]),
            notes('df`` ', ['2.', 4])
        ]
        select(upper_melody[1], 1).prefix += '\\tempo "Molto lento" '
        select(upper_melody[1], 1).markdown = '\\italic{piacévole}'

        lower_melody = [
            [],
            rests(1),
            rests(1),
            rests(1),
            rests(1),
            notes('gf bf ef`', [2, 4, 4]),
            tied_note('c`', [2, 8]) + rests(8, 4),
            rests(2) + notes('af', 2),
            notes('df', 4) + rests(4, 2)
        ]

        upper_harmony = [
            [],
            rests(1),
            self.scale('bf`', -4, 8) + self.scale('gf`', -4, 8),
            omit(self.scale('c`', 7, 8), 2) + self.scale('af`', -2, 8),
            (omit(scale('d`', 7, dur=8, key='ef minor harmonic'), 2) +
             self.scale('bf`', -2, 8)),
            (notes('af`', 8) + self.scale('f`', 3, 8) +
             self.scale('gf`', 3, 8) + notes('bf`', 8)),
            (self.scale('bf`', -3, 8) + self.scale('af`', -2, 8) +
             self.scale('c`', 3, 8))
        ]
        select(upper_harmony[4], 8).articulation = '~'
        select(upper_harmony[5], 8).articulation = '~'

        lower_harmony = [
            [],
            self.scale('f`', -8, 8),
            tied_note('gf', [2, 8]) + self.scale('ef', 3, 8),
            self.transpose(upper_harmony[3], -2),
            transpose(upper_harmony[4], -2, key='ef minor harmonic'),
            transpose(upper_harmony[5], -2, key='ef minor harmonic'),
            self.transpose(upper_harmony[6], -2)
        ]

        # put it all together
        if not self.improvements:
            bar3e = (
                rests(8, prefix='\\omit ') +
                notes('ef`', 8,
                      prefix=(
                        '\\voiceOne \\autoBeamOff \\stemDown \\crossStaff {'),
                      suffix='} \\autoBeamOn \\stemNeutral ') +
                rests(2, 4, prefix='\\omit '))

            self.score = {
                'treble': [
                    [],
                    upper_melody[1],
                    voices(upper_melody[2], upper_harmony[2]),
                    voices(upper_melody[3], bar3e),
                    voices(upper_melody[4], merge(upper_harmony[4],
                                                  lower_harmony[4])),
                    voices(upper_melody[5], merge(upper_harmony[5],
                                                  lower_harmony[5])),
                    voices(upper_melody[6], merge(upper_harmony[6],
                                                  lower_harmony[6])),
                    upper_melody[7],
                    upper_melody[8]],
                'bass': [
                    [],
                    lower_harmony[1],
                    lower_harmony[2],
                    merge(upper_harmony[3], lower_harmony[3]),
                    lower_melody[4],
                    lower_melody[5],
                    lower_melody[6],
                    lower_melody[7],
                    lower_melody[8]]
            }

            select(self.score['bass'][3], 1).prefix = (
                '\\override Beam.auto-knee-gap = #10 ')
            select(self.score['bass'][3], 2).remove('ef`')
            select(self.score['bass'][3], 3).prefix = (
                '\\change Staff = "treble" \\voiceTwo ')
            select(self.score['bass'][3], 5).prefix = (
                '\\override Beam.auto-knee-gap = #5.5 ')
            select(self.score['bass'][4], 1).prefix = (
                '\\change Staff = "bass" \\omit ')
            select(self.score['bass'][6], 3).prefix = ('\\omit ')
            select(self.score['bass'][6], 4).prefix = ('\\omit ')
            select(self.score['bass'][7], 1).prefix = ('\\omit ')
            select(self.score['bass'][8], 2).prefix = ('\\omit ')
            select(self.score['bass'][8], 3).prefix = ('\\omit ')
            select(self.score['bass'][6], 2).prefix += (
                ' \\stemDown \\crossStaff { ')
            select(self.score['bass'][6], 2).suffix += ' } \\stemNeutral'
            select(self.score['treble'][6], 12).prefix += (
                '\\change Staff = "bass" ')
        else:
            self.score = {
                'treble': upper_melody,
                'middle': self.merge_harmonies(upper_harmony, lower_harmony),
                'bass': lower_melody
            }

    def merge_harmonies(self, upper_harmony, lower_harmony):
        return([
            [],
            lower_harmony[1],
            voices(upper_harmony[2], lower_harmony[2]),
            merge(upper_harmony[3], lower_harmony[3]),
            merge(upper_harmony[4], lower_harmony[4]),
            merge(upper_harmony[5], lower_harmony[5]),
            merge(upper_harmony[6], lower_harmony[6]),
        ])


if __name__ == "__main__":
    GenreAncien()
