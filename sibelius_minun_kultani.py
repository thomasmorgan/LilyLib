from piece import Piece
from points import chord, rests, tied_note, notes, tied_chord
from markup import slur, voices, clef, italic
from util import rep, subset, select
from staves import Treble, Bass, Dynamics


class MinunKultani(Piece):

    def details(self):
        self.title = "Minun Kultani"
        self.composer = "Jean Sibelius"
        self.date = "1903"
        self.mutopiacomposer = "SibeliusJ"
        self.mutopiainstrument = "piano"
        self.source = "Breitkopf und Härtel, 1906"
        self.style = "Romantic"
        self.license = "Creative Commons Attribution-ShareAlike 4.0"
        self.maintainer = "Thomas Morgan"
        self.mantainer_email = "thomas.j.h.morgan@gmail.com"
        self.opus = "JS 81, No. 1"
        self.auto_add_bars = True
        self.key = 'fs minor'
        self.tempo_name = "Allegretto"
        self.staves = [Treble(), Dynamics(), Bass()]

    def write_score(self):

        ###########
        # part 1
        ###########

        def chord_motif(*args):
            motif = slur(self.harmonize(
                notes('gs fs e', 4) + tied_note('fs', [8, 8]), -2))
            if "short" in args:
                motif = subset(motif, 1, 4)
                select(motif, 4).phrasing = ')'
            return motif

        treble_1 = (
            rests(8) + rep(chord_motif(), 2) + chord_motif("short") +
            rests(4) + tied_chord('b, d', ['2.', 1, 1]))
        bass_1 = rep(chord('e, b,', 1), 3) + tied_chord('b,, fs,', [1, 1, 1])

        for i in [1, 7, 11, 16]:
            select(treble_1, i).suffix += '\\sustainOn'
        for i in [4, 9, 14]:
            select(treble_1, i).suffix += '\\sustainOff'

        dynamics_1 = rep(rests(1, prefix='%{ spacer %}'), 5)
        select(dynamics_1, 1).dynamics = 'mp'

        ###########
        # part 2
        ###########

        mini_motif = (
            slur(notes('fs e', ['4.', 8])) +
            notes('cs e', 4, articulation='-'))
        treble_2 = (
            clef('bass', rep(notes('fs', 4, articulation='-'), 4)) +
            mini_motif + self.transpose(mini_motif, -1) +
            notes('d', 2, articulation='-') +
            tied_note('cs', [2, 1], articulation='-')
            )
        select(treble_2, 2).dynamics = '<'
        for i in [4, 7, 11, 14]:
            select(treble_2, i).dynamics = '!'
        for i in [5, 9, 13]:
            select(treble_2, i).dynamics = '>'
        bass_2 = rep(rests(1), 4)
        dynamics_2 = rep(rests(1, prefix='%{ spacer %}'), 5)
        select(dynamics_2, 1).dynamics = 'mf'

        select(treble_2, 1).markup = italic('semplice')

        ###########
        # part 3
        ###########

        ###########
        # combine
        ###########

        self.score = {
            'treble': (
                rep(rests(1, prefix='%{ spacer %}'), 4) + rests(1) +
                treble_2),
            'dynamics': dynamics_1 + dynamics_2,
            'bass': voices(treble_1, bass_1) + bass_2
        }


if __name__ == "__main__":
    MinunKultani()
