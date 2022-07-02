from piece import Piece
from staves import Treble, Dynamics, Bass
from points import notes, rests
from util import rep
from markup import slur, voices


class IltaTulee(Piece):

    def details(self):
        self.title = "Ilta Tulee, Ehto Joutuu"
        self.composer = "Jean Sibelius"
        self.date = "1903"
        self.mutopiacomposer = "SibeliusJ"
        self.mutopiainstrument = "piano"
        self.source = "Breitkopf und Härtel, 1906"
        self.style = "Romantic"
        self.license = "Creative Commons Attribution-ShareAlike 4.0"
        self.maintainer = "Thomas Morgan"
        self.mantainer_email = "thomas.j.h.morgan@gmail.com"
        self.opus = "JS 81, No. 3"
        self.auto_add_bars = True
        self.key = 'cs minor'
        self.tempo_name = "Andantino"
        self.staves = [
            Treble(),
            Dynamics(),
            Bass(),
            Dynamics("pedal")]

    def subtext(self):
        return (
            "\\layout { \\context { \\Score \\override "
            "SpacingSpanner.base-shortest-duration = "
            "#(ly:make-moment 1/36)}}\n"
            '\\paper { #(set-paper-size "letter")}\n')

    def write_score(self):

        ###########
        # part 1
        ###########

        high_treble_1 = notes('cs``', [1, 1, 1, 1], articulation='>')

        def tremolo():
            return notes('cs`` cs`', 16) + rep(notes('ds` cs`', 16), 7)

        low_treble_1 = rep(slur(tremolo()), 2) + rep(tremolo(), 2)
        treble_1 = voices(high_treble_1, low_treble_1)
        bass_1 = rests(1, 1, 1, 1, prefix='%{ spacer %}')

        ###########
        # combine
        ###########

        self.score = {
            'treble': treble_1,
            'dynamics': rests(1, 1, 1, 1),
            'bass': bass_1,
            'pedal': rests(1, 1, 1, 1)
        }


if __name__ == "__main__":
    IltaTulee()
