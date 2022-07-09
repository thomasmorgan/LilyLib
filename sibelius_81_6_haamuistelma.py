from piece import Piece
from staves import Treble, Bass, Dynamics
from points import rests, notes, chord, chords, tied_note
from markup import slur, voices, clef
from util import select, rep, subset
from copy import deepcopy


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
            motif = slur([chord(c, 8)] + chords(cs, 8))
            select(motif, 1).prefix += '\\stemUp '
            select(motif, 4).suffix += '\\stemNeutral '
            return motif

        treble_2 = voices(
            rests(2) + clef("treble",
                            [chord('ef` c`` ef``', 2, articulation='>')]) +
            rests(2, prefix='%{ spacer %}') +
            notes('ef``', 2, articulation='>') +
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
        # part 3
        #########

        treble_3 = rests(8) + deepcopy(subset(treble_1, 10, len(treble_1)))
        bass_3 = voices(
            rests(8) + deepcopy(subset(bass_1, 10, len(bass_1))),
            [chord('df, af,', 1)] + rests(1, prefix='%{ spacer %} ')
            )
        select(treble_3, 2).phrasing = '('
        select(bass_3, 2).phrasing = '('
        select(treble_3, 9).prefix = '\\clef "bass" '

        #########
        # part 4
        #########

        treble_4 = voices(
            rests(2) + clef("treble",
                            [chord('ef` c`` ef``', 2, articulation='>')]) +
            rests(2, prefix='%{ spacer %}') +
            notes('ef``', 2, articulation='>') +
            rests(2) + chords(['ef` ef``'], 2, articulation='>') +
            rep(rests(1, prefix='%{ spacer %}'), 2),
            rests(1, prefix='%{ spacer %}') +
            notes('c` c`', 1) + rests(1, 1, prefix='%{ spacer %}'),
            [chord('c ef', 1)] +
            slur(notes('ef` af`', [4, 8])) + notes('g`', 8) +
            slur(notes('f` g`', 8)) + notes('af`', 4) +
            slur(notes('ef` af`', [4, 8])) + notes('af` bf` c``', [8, 4, 4]) +
            chords(['c` af`', 'ef` c``', 'f` df``'], [4, 8, 8]) +
            slur(chords(['ef` ef``', 'c` c``'], 8)) +
            [chord('bf f` bf`', 4, articulation='>')] +
            chords(['bf f`', 'g df` g`'], 2, articulation='>')
        )

        bass_4 = (
            rep(lh_motif('c, af,') + lh_motif('af, ef'), 3) +
            [chord('af, ef', 4)] + chords(['c af', 'df'], 8) +
            slur(chords(['c, af, ef', 'c'], 8)) +
            [chord('df, af, df af', 4)] +
            lh_motif('bf,, df', ['f', 'bf, af', 'f']) +
            lh_motif('ef, bf,', ['ef', 'bf', 'ef'])
        )

        #########
        # part 5
        #########

        treble_5 = (
            voices(
                deepcopy(subset(treble_3, 1, 16)),
                [chord('af df` af`', 1,
                       prefix='\\arpeggioParenthesis ',
                       articulation='>',
                       ornamentation='arpeggio')] +
                rests(1, prefix='%{ spacer %}')
            ) + slur(chords(['c ef', 'df f', 'c af'], [2, 2, '2.'])) +
            rests(4, ornamentation='fermata')
        )
        bass_5 = (
            voices(
                rests(8) + deepcopy(subset(bass_1, 10, len(bass_1))),
                [chord('df, af, f', 1,
                       prefix='\\arpeggioParenthesis ',
                       ornamentation='arpeggio')] +
                rests(1, prefix='%{ spacer %}')
            ) + slur(chords(['c, af,', 'bf,, af,', 'af,, ef, af,'],
                            [2, 2, '2.'])) +
            rests(4, ornamentation='fermata')
        )
        select(bass_5, 2).phrasing = '('

        #########
        # dynamics
        #########

        def dyn(dur, dy):
            return rests(dur, dynamics=dy)

        dynamics = (
            rests(8) + dyn(8, 'p') + rests('2.', 1, 1, 1) +
            dyn(1, 'mf') + rests(16) + dyn('2.', '<') + dyn('8.', '!') +
            rests(4) + dyn(2, '>') + dyn(4, '!') + rests(1, 1) +
            dyn(1, 'p') + rests(1, 1) + dyn(1, 'mf') +
            rests(16) + dyn(16, '<') + rests('4.', '8.') + dyn(16, '!') +
            rests(4) + rests(1, markdown='\\italic{poco }\\dynamic{f}') +
            rests(1, 16) + dyn(16, 'p') + rests(8, 4, 2, 1) + dyn(1, '>') +
            dyn(1, '!')

        )

        #########
        # pedal
        #########

        def on(dur):
            return rests(dur, suffix='\\sustainOn')

        def off(dur):
            return rests(dur, suffix='\\sustainOff')

        pedal = (
            rests(1, 1, 1) + on(1) + rep(on(2) + off(2), 3) + rep(on(1), 2) +
            on(2) + rests(4, 16) + off(16) + rests(8, 1) + on(2) +
            rests('8.') + off(16) + rests(4) +
            rep(on(2) + rests(8) + off('4.'), 2) +
            on(2) + rests(8) + off(8) + on(4) + rep(on(2), 2) + on(1) +
            off(1) + rests(1, 1)
        )

        #########
        # markup
        #########

        select(treble_1, 17).prefix = '\\clef "bass" '

        #########
        # combine
        #########

        self.score = {
            'treble': treble_1 + treble_2 + treble_3 + treble_4 + treble_5,
            'dynamics': dynamics,
            'bass': bass_1 + bass_2 + bass_3 + bass_4 + bass_5,
            'pedal': pedal
        }


if __name__ == "__main__":
    Haamuistelma()
