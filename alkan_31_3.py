from piece import Piece
from points import notes, tied_note, chords, rests, add
from staves import Treble, Super, Bass
from markup import voices
from util import select, omit


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
          "\\consists #Span_stem_engraver } }\n")

    def write_score(self):

        # section 1
        # treble
        s1_treble1 = notes('af` df`` f``', [2, 4, 4])
        s1_treble2 = notes('f`` ef`` gf``', [2, 4, 4])
        s1_treble2b = self.scale('bf`', -4, 8) + self.scale('gf`', -4, 8)
        s1_treble3 = notes('gf`` ef`` df`` c``', 4)
        s1_treble3b = (
            rests(8, prefix='\\omit ') + notes('ef`', 8) +
            rests(2, 4, prefix='\\omit '))

        select(s1_treble1, 1).prefix += '\\tempo "Molto lento" '
        select(s1_treble1, 1).markdown = '\\italic{piacévole}'
        if not self.improvements:
            select(s1_treble3b, 2).prefix = (
                '\\voiceOne \\autoBeamOff \\stemDown \\crossStaff {')
            select(s1_treble3b, 2).suffix = '} \\autoBeamOn \\stemNeutral '

        # bass
        s1_bass1 = self.scale('f`', -8, 8)
        s1_bass2 = tied_note('gf', [2, 8]) + self.scale('ef', 3, 8)
        s1_bass3 = (
            chords(['af c`', 'c`'], 8) +
            self.harmonize(self.scale('df`', 4, 8) +
                           self.scale('f`', -2, 8), 2))
        if not self.improvements:
            select(s1_bass3, 3).prefix = (
                '\\change Staff = "treble" \\voiceTwo ')
        else:
            add(select(s1_bass3, 2), 'ef`')
        s1_bass4 = rests(1)

        # put it all together
        if not self.improvements:
            self.score = {
                'treble': (
                    s1_treble1 + voices(s1_treble2, s1_treble2b) +
                    voices(s1_treble3, s1_treble3b)),
                'bass': s1_bass1 + s1_bass2 + s1_bass3 + s1_bass4
            }
        else:
            self.score = {
                'treble': s1_treble1 + s1_treble2 + s1_treble3,
                'middle': (
                    s1_bass1 + voices(s1_treble2b, s1_bass2) +
                    s1_bass3 + rests(1)),
                'bass': rests(1, 1, 1, 1)
            }


if __name__ == "__main__":
    GenreAncien()
