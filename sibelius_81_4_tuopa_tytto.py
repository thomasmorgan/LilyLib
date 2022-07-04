from piece import Piece
from staves import Bass, Dynamics
from points import chord, tied_chord, notes
from markup import slur
from util import rep, select


class TuopaTytto(Piece):

    def details(self):
        self.title = "Tuopa tyttö, kaunis tyttö, kanteletta soittaa"
        self.composer = "Jean Sibelius"
        self.date = "1903"
        self.mutopiacomposer = "SibeliusJ"
        self.mutopiainstrument = "piano"
        self.source = "Breitkopf und Härtel, 1906"
        self.style = "Romantic"
        self.license = "Creative Commons Attribution-ShareAlike 4.0"
        self.maintainer = "Thomas Morgan"
        self.mantainer_email = "thomas.j.h.morgan@gmail.com"
        self.opus = "JS 81, No. 4"
        self.auto_add_bars = True
        self.key = 'd minor'
        self.tempo = ("2/4")
        self.beaming = ('\\set Timing.baseMoment = #(ly:make-moment 1/8)\n'
                        '\\set Timing.beatStructure = 1, 1, 1, 1')
        self.tempo_name = 'Moderato'
        self.staves = [
            Bass(name='treble'),
            Dynamics(),
            Bass(),
            Dynamics('pedal')]

    def write_score(self):

        #########
        # part 1
        #########

        treble_1 = [chord('c, g,', 2)] + tied_chord('c, g,', [2, 2, 2])
        bass_1 = (
            slur(rep(notes('e, e c e', 32), 5) +
                 rep(notes('e` g e g', 32), 3)) +
            slur(rep(notes('e e` c` e`', 32), 5) +
                 rep(notes('e`` g` e` g`', 32), 3)))
        select(bass_1, 1).phrasing = '_('
        select(bass_1, 33).phrasing = '_('
        select(bass_1, 53).prefix += (
            '\\change Staff = "treble" \\clef "treble" ')

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
    TuopaTytto()
