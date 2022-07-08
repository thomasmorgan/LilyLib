from piece import Piece
from staves import Treble, Bass, Dynamics
from points import rests, notes, chord, chords, tied_note
from markup import slur, voices, clef
from util import select, rep


class Haamuistelma(Piece):

    def details(self):
        self.title = "Häämuistelma"
        self.composer = "Jean Sibelius"
        self.date = "1903"
        self.mutopiacomposer = "SibeliusJ"
        self.mutopiainstrument = "piano"
        self.source = "Breitkopf und Härtel, 1906"
        self.style = "Romantic"
        self.license = "Creative Commons Attribution-ShareAlike 4.0"
        self.maintainer = "Thomas Morgan"
        self.mantainer_email = "thomas.j.h.morgan@gmail.com"
        self.opus = "JS 81, No. 6"
        self.auto_add_bars = True
        self.key = 'af major'
        self.tempo_name = 'Moderato'
        self.staves = [
            Treble(),
            Dynamics(),
            Bass(),
            Dynamics('pedal')]

    def subtext(self):
        return (
            "\\layout { \\context { \\Score \\override "
            "SpacingSpanner.base-shortest-duration = "
            "#(ly:make-moment 1/36)}}\n"
            '\\paper { #(set-paper-size "letter")}\n')

    def write_score(self):

        #########
        # part 1
        #########

        treble_1 = (
            rests(8) +
            slur(notes('ef`` af`` g`` f`` g`` f`` df`` bf` c`` bf` '
                       'af` f` af` f` df` bf c` bf af f af f df', 8)))

        bass_1 = self.transpose(treble_1, -9, 'scale')

        #########
        # part 2
        #########

        def lh_motif(c, cs=['f', 'af', 'f']):
            return slur([chord(c, 8)] + chords(cs, 8))

        treble_2 = voices(
            rests(2) + clef("treble",
                            [chord('ef` c`` ef``', 2, articulation='>')]) +
            rests(2) + notes('ef``', 2, articulation='>') +
            rests(2) + chords(['ef` ef``'], 2, articulation='>') +
            rep(rests(1, prefix='%{ spacer %}'), 3),
            rests(1, prefix='%{ spacer %}') +
            notes('c` c` df`', 1) + tied_note('df`', [1, 1]),
            [chord('c ef', 1)] +
            slur(notes('ef` af`', [4, 8])) + notes('g`', 8) +
            slur(notes('f` g`', 8)) + notes('af`', 4) +
            slur(notes('ef` af`', [4, 8])) + notes('af` bf` c``', [8, 4, 4]) +
            slur(notes('af` df``', [4, 8])) + notes('bf`', 8) +
            slur(notes('c`` af`', 8)) + notes('bf`', 4) +
            notes('f` g`', 4) + tied_note('af`', [2, 1])
        )

        select(treble_2, 17).prefix = '\\slurDown '
        select(treble_2, 28).prefix = '\\slurUp '

        bass_2 = (
            rep(lh_motif('c, af,') + lh_motif('af, ef'), 3) +
            rep(lh_motif('df, af,') + lh_motif('f, df'), 3)
        )

        #########
        # markup
        #########

        select(treble_1, 17).prefix = '\\clef "bass" '

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
    Haamuistelma()
