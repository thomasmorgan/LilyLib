from piece import Piece
from staves import Treble, Bass, Dynamics
from points import rests, notes
from markup import slur
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
        # combine
        #########

        self.score = {
            'treble': treble_1,
            'dynamics': [],
            'bass': bass_1,
            'pedal': []
        }


if __name__ == "__main__":
    Velisurmaaja()
