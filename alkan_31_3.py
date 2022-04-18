from piece import Piece
from points import notes, tied_note
from staves import Treble, Super
from markup import voices
from util import select


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

    def write_score(self):

        # section 1
        # treble
        s1_treble1 = notes('af` df`` f``', [2, 4, 4])
        s1_treble2 = notes('f`` ef`` gf``', [2, 4, 4])
        s1_treble2b = self.scale('bf`', -4, 8) + self.scale('gf`', -4, 8)

        select(s1_treble1, 1).prefix += '\\tempo "Molto lento" '
        select(s1_treble1, 1).markdown = '\\italic{piacévole}'

        # bass
        s1_bass1 = self.scale('f`', -8, 8)
        s1_bass2 = tied_note('gf', [2, 8]) + self.scale('ef', 3, 8)

        # put it all together
        self.score = {
            'treble': s1_treble1 + voices(s1_treble2, s1_treble2b),
            'bass': s1_bass1 + s1_bass2
        }


if __name__ == "__main__":
    GenreAncien()
