from piece import Piece
from points import chord, rests, tied_note, notes, tied_chord, chords, replace
from markup import (
    slur, voices, clef, italic, diminuendo, thick_barbreak, pagebreak)
from util import rep, subset, select
from staves import Treble, Bass, Dynamics


class SydamestaniRakastan(Piece):

    def details(self):
        self.title = "Sydämestäni Rakastan"
        self.composer = "Jean Sibelius"
        self.date = "1903"
        self.mutopiacomposer = "SibeliusJ"
        self.mutopiainstrument = "piano"
        self.source = "Breitkopf und Härtel, 1906"
        self.style = "Romantic"
        self.license = "Creative Commons Attribution-ShareAlike 4.0"
        self.maintainer = "Thomas Morgan"
        self.mantainer_email = "thomas.j.h.morgan@gmail.com"
        self.opus = "JS 81, No. 2"
        self.auto_add_bars = True
        self.key = 'e minor'
        self.tempo_name = "Andante"
        self.staves = [
            Treble(_with='\\override Beam.breakable = ##t\n'),
            Dynamics(),
            Bass()]

    # def subtext(self):
    #     return (
    #         "\\layout { \\context { \\Score \\override "
    #         "SpacingSpanner.base-shortest-duration = "
    #         "#(ly:make-moment 1/24)}}\n")

    def write_score(self):

        ###########
        # part 1
        ###########

        def opening_scale():
            return (
                slur(notes('b` a` g`', 2)) +
                notes('fs` e` fs` g`', [4, 4, 2, 2]))
        treble_1 = self.harmonize(opening_scale(), -4)
        replace(select(treble_1, 7), 'c`', 'b')
        select(treble_1, 7).phrasing = '~'
        bass_1 = self.harmonize(
            self.transpose(opening_scale(), -1, 'octave'), -2)
        replace(bass_1, 'd', 'ds')
        replace(bass_1, 'c', 'cs')
        dynamics_1 = rests(1, 1, 1)

        ###########
        # part 2
        ###########

        def melody_1():
            return (
                notes('e`', 4) +
                notes('b` b` a` a` d`` d`` b`', 4, articulation='-') +
                notes('b` b`', 8) + notes('g` g` a` a`', 4, articulation='-'))

        high_treble_2 = rests(2, 4) + melody_1()
        low_treble_2 = (
            [chord('b g`', 1)] + notes('e` d` d` e` cs` ds`', 2))

        bass_2 = (
            [chord('g,, e, g,', 1)] +
            self.harmonize(notes('b a a b g a', 2), -2))

        ###########
        # part 3
        ###########

        def syncopated_b():
            motif = notes('b', [8, 8, 4, 4, 4])
            select(motif, 1).phrasing = '_~['
            select(motif, 2).phrasing = ']'
            return motif

        high_treble_3 = [chord('e` b`', '2.')] + melody_1()

        low_treble_345 = (
            rests(8) + notes('b b b', 4) +
            rep(syncopated_b(), 15) + notes('b', 8))

        bass_3 = (
            notes('g', 1) +
            voices(slur(notes('g fs a g', 2)) + slur(notes('e fs', 2)),
                   tied_note('e', [1, 1]) + notes('e', 1)))

        ###########
        # part 4
        ###########

        def melody_2():
            return(
                notes('e`', 4) +
                notes('b` b` g` e`', 4, articulation='-') +
                slur(notes('a` g`', [2, 4])) +
                notes('e` fs`', 8) +
                notes('g` g` fs` fs`', 4, articulation='-') +
                notes('e`', 1, phrasing='~'))

        high_treble_4 = notes('b`', '2.') + melody_2()

        bass_4 = (
            chords(['e,', 'e, cs'], 16, phrasing='~') +
            tied_chord('e, cs g', [8, '2.', 1]) +
            voices(
                chords(['fs, ds', 'g, e'], 2),
                notes('e,', 1)) +
            chords(['cs g', 'ds a', 'e g'], [2, 2, 1]))

        ###########
        # part 5
        ###########

        high_treble_5 = (
            notes('e`', '2.') + melody_2() + notes('e`', 1, phrasing='~') +
            notes('e`', 1))

        bass_5 = rep(subset(bass_4, 1, 10), 1) + tied_chord('e g', [1, 1, 1])

        ###########
        # combine
        ###########

        self.score = {
            'treble': (
                voices(rests(1, 1, 1, prefix='\\omit ') + high_treble_2,
                       treble_1 + low_treble_2) +
                voices(high_treble_3 + high_treble_4 + high_treble_5,
                       low_treble_345)),
            'dynamics': dynamics_1,
            'bass': (
                bass_1 + bass_2 + bass_3 + bass_4 + bass_5)
        }


if __name__ == "__main__":
    SydamestaniRakastan()
