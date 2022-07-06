from piece import Piece
from staves import Treble, Bass, Dynamics
from points import rests, notes, chords, tied_note
from markup import slur, voices
from util import select, rep, subset


class Velisurmaaja(Piece):

    def details(self):
        self.title = "Velisurmaaja"
        self.composer = "Jean Sibelius"
        self.date = "1903"
        self.mutopiacomposer = "SibeliusJ"
        self.mutopiainstrument = "piano"
        self.source = "Breitkopf und Härtel, 1906"
        self.style = "Romantic"
        self.license = "Creative Commons Attribution-ShareAlike 4.0"
        self.maintainer = "Thomas Morgan"
        self.mantainer_email = "thomas.j.h.morgan@gmail.com"
        self.opus = "JS 81, No. 5"
        self.auto_add_bars = True
        self.key = 'cs minor'
        self.tempo_name = 'Andante con moto'
        self.staves = [
            Treble(),
            Dynamics(),
            Bass(),
            Dynamics('pedal')]

    def subtext(self):
        return '\\paper { #(set-paper-size "letter")}\n'

    def write_score(self):

        #########
        # part 1
        #########

        def bass_motif():
            motif = slur(notes('gs, a, fs, bs, a, gs, fs, fs,,', 8))
            select(motif, 1).phrasing = '^('
            return motif

        treble_1 = rests(1, 1, 1, 1)
        bass_1 = (
            notes('fs,,', 8) + rep(bass_motif(), 2) +
            subset(bass_motif(), 1, 5) +
            notes('ds bs, fs ds a fs bs a ds` bs', 8)
        )
        select(bass_1, 32).phrasing = ')'

        #########
        # part 2
        #########

        def chord_motif(chord1, chord2=None):
            if chord2:
                return (
                    rests(8) +
                    chords([chord1, chord2, chord2, chord1], [4, 4, 4, 8]))
            else:
                return rests(8) + chords([chord1], [4, 4, 4, 8])

        treble_2 = (
            notes('cs` cs` cs` cs` gs` gs` ds` e` fs`', 4, articulation='-') +
            notes('fs` gs`', 8) + notes('fs` e`', 4, articulation='-'))

        bass_2 = voices(
          chord_motif('cs e as') + rep(chord_motif('cs e as', 'ds fs bs'), 2),
          rests(2) + tied_note('fs,,', [2, 4]) + rests(4, 2, 1)
        )
        select(bass_2, 13).articulation = '>'

        #########
        # combine
        #########

        self.score = {
            'treble': treble_1 + treble_2,
            'dynamics': [],
            'bass': bass_1 + bass_2,
            'pedal': []
        }


if __name__ == "__main__":
    Velisurmaaja()
