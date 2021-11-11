from piece import Piece
from staves import Bass, Super
from points import chords, chord, notes, note, add, tied_note, tied_chord
from points import rests, rest
from util import select, subset, rep
from tones import tonify
from markup import voices, slur, diminuendo, repeat, linebreak
from markup import double_barbreak, doublethick_barbreak
from copy import deepcopy


class Priere(Piece):

    def details(self):
        self.title = "Priere"
        self.subtitle = ""
        self.composer = "Charles-Valentin Alkan"
        self.date = "1847"
        self.mutopiacomposer = "AlkanCV"
        self.mutopiainstrument = "piano"
        self.source = "A.M. Schlesinger, 1847"
        self.style = "Romantic"
        self.license = "Creative Commons Attribution-ShareAlike 4.0"
        self.maintainer = "Thomas Morgan"
        self.mantainer_email = "thomas.j.h.morgan@gmail.com"
        self.opus = "Op. 31, No. 25"
        self.tempo = "6/4"
        self.auto_add_bars = True
        self.improvements = False
        self.piano_staff = not self.improvements
        if self.improvements:
            self.staves = [Super('super')]
        else:
            self.staves = [Bass('treble'), Bass('bass')]

    def subtext(self):
        if self.improvements:
            return (
              "\\paper { system-system-spacing = #'((basic-distance . 24)) }")
        else:
            return "\\paper { page-count = #1 }"

    def write_score(self):

        rhythm = ['2.', 2, 4]

        def split_chords(shared, first, second=''):
            return chords([
                ' '.join((shared, first)),
                ' '.join((shared, second))
                ], '2.')

        treble1 = (
            chords(['c e c`', 'e g c`', 'e g c`'], rhythm) +
            split_chords('d g', 'b', 'b,') +
            chords(['a c` f`'], rhythm) +
            split_chords('g c`', 'e`', 'e') +
            chords(['d` g`', 'b d` g`', 'b d` g`'], rhythm) +
            split_chords('c` e`', 'g`', 'a`') +
            voices(slur(tied_note('fs`', ['2.', 2]) + notes('g`', 4)),
                   notes('c` b c` d`', [2, 4])) +
            [chord('b d` g`', '1.')]
        )
        bass1 = (
            notes('c', rhythm) +
            split_chords('g,', 'b,') +
            add(notes('f, a, c', rhythm), 'f') +
            split_chords('c', 'e') +
            add(notes('b, g, g,', rhythm), 'g') +
            chords(['c g', 'a, a'], '2.') +
            [chord('d a', '1.')] +
            voices(notes('g', '1.'),
                   notes('g,', '2.') + notes('e, f, d,', 4))
        )

        select(treble1, 1).prefix += '\\tempo "Lento" '
        select(treble1, 1).markdown = (
            '\\dynamic{p} \\italic{e molto sostenuto sempre}')
        if not self.improvements:
            select(treble1, 11).prefix += '\\clef "treble" '
        select(treble1, len(treble1)).suffix += double_barbreak

        treble2 = (
            chords(['e g c`'], rhythm) +
            split_chords('d g', 'b') +
            chords(['a c` f`'], rhythm) +
            split_chords('g c`', 'e`', 'e') +
            chords(['d` g`', 'b d` g`', 'b d` g`'], rhythm) +
            chords(['c` e` g`', 'c` e` a`', 'c` e`'], rhythm) +
            voices(tied_note('fs`', ['2.', 2]) + notes('g`', 4),
                   notes('c`', 2) + notes('b c` e` d`', 4)) +
            [chord('b d` g`', '1.')]
        )

        bass2 = (
            add(notes('c, e, g,', rhythm), 'c') +
            split_chords('g,', 'b,') +
            voices(notes('f', rhythm),
                   notes('f,', '2.') + notes('f, a, c', 4)) +
            split_chords('c', 'e') +
            add(notes('b, g, g,', rhythm), 'g') +
            chords(['c g', 'a, a'], '2.') +
            [chord('d a', '1.')] +
            [chord('g, g', '1.')]
        )

        if not self.improvements:
            select(treble2, 1).prefix += '\\clef "bass" '
            select(treble2, 11).prefix += '\\clef "treble" '
        select(treble2, len(treble2)).suffix += (
            '\\bar ".|:-||" %{ bar %} ' + linebreak)

        treble3 = (
            chords(['g b d`'], rhythm) +
            chords(['f a f`'], ['2.', '2.']) +
            voices(notes('c` b c` d`', [2, 4]),
                   chords(['f a'], rhythm)) +
            voices(notes('e` e`', '2.'),
                   chords(['e gs'], ['2.', '2.'])) +
            chords(['bf e` g`'], rhythm) +
            voices([chord('a a` c``', '1.')],
                   diminuendo(notes('g` f` e`', rhythm))) +
            voices(notes('d`', '2.') + chords(['d`', 'e`', 'd` f`'], 4),
                   notes('g', rhythm)) +
            chords(['g d` f`', 'g c` e`'], '2.') +
            voices(chords(['e` g`'], rhythm),
                   notes('bf', 2) + notes('a bf d` c`', 4)) +
            diminuendo(chords(['a g` a` c``', 'a f`', 'g e`'], rhythm)) +
            chords(['e c`', 'f d`'], '2.') +
            [chord('e c`', '1.')]
        )

        bass3 = (
            chords(['g, d'], rhythm) +
            chords(['d, d'], ['2.', '2.']) +
            chords(['f, c'], rhythm) +
            rep(chord('e, b,', '2.'), 2) +
            chords(['c, c'], rhythm) +
            [chord('f, c', '1.')] +
            chords(['g, b,'], rhythm) +
            [chord('c, c', '1.')] +
            chords(['c, c'], rhythm) +
            tied_chord('f, c', ['2.', 2]) + [chord('g, c', 4)] +
            chords(['a, c', 'g, b,'], '2.') +
            [chord('c, c', '1.')]
        )

        if not self.improvements:
            select(treble3, 1).prefix += '\\clef "bass" '
        select(treble3, 1).markdown = '\\italic{sempre }\\dynamic{p}'
        if not self.improvements:
            select(treble3, 17).prefix += '\\clef "treble" '
        select(treble3, 24).dynamics = 'p'
        select(treble3, 33).dynamics = 'f'
        select(treble3, 41).phrasing = '~'
        select(treble3, 44).dynamics = 'p'
        select(bass3, 14).markdown = '\\italic{Ped. o Mani}'
        select(bass3, 22).markdown = '\\italic{Ped. o Mani}'

        treble4 = (
            chords(['e g c`'], rhythm) +
            split_chords('d g', 'b', 'b,') +
            chords(['a c` f`'], rhythm) +
            split_chords('g c`', 'e`', 'e') +
            split_chords('d` g`', '', 'b') +
            split_chords('c` e`', 'g`', 'a`') +
            voices(slur(tied_note('fs`', ['2.', 2]) + [note('g`', 4)]),
                   notes('c` b c` d`', [2, 4])) +
            [chord('b d` g`', '1.')]
        )

        bass4 = (
            deepcopy(subset(bass1, 1, 10)) +
            chords(['b, g', 'g, g'], '2.') +
            chords(['c g', 'a, a'], '2.') +
            [chord('d a', '1.')] +
            [chord('g, g', '1.')]
        )

        select(treble4, 1).dynamics = 'ppp'
        if not self.improvements:
            select(treble4, 4).prefix += '\\clef "bass" '
            select(treble4, 11).prefix += '\\clef "treble" '
        select(treble4, len(treble4)).suffix += double_barbreak

        treble5 = (
            chords(['g b d`'], rhythm) +
            rep(chord('f a f`', '2.'), 2) +
            voices(notes('c` b c` d`', [2, 4]),
                   chords(['f a'], rhythm)) +
            rep(chord('e gs e`', '2.'), 2) +
            chords(['bf e` g`'], rhythm) +
            voices([chord('a c``', '1.')],
                   diminuendo(notes('g` f` e`', rhythm))) +
            voices(chords(['d`', 'd`', 'e`', 'd` f`'], ['2.', 4, 4, 4]),
                   notes('g', rhythm)) +
            chords(['g d` f`', 'g c` e`', 'c`', 'e`'], ['2.', 4, 4, 4]) +
            voices(chords(['e` g`'], rhythm),
                   notes('bf', '2') + notes('a bf d` c`', 4)) +
            chords(['a g` c``', 'a f` c``', 'g e`'], rhythm) +
            voices(notes('c` d` c`', rhythm),
                   notes('e f', '2.')) +
            [chord('e c`', '1.', ornamentation='fermata')]
        )

        bass5 = (
            chords(['g, d'], rhythm) +
            rep(chord('d, d', '2.'), 2) +
            chords(['f, c'], rhythm) +
            rep(chord('e, b,', '2.'), 2) +
            chords(['c, c'], rhythm) +
            [chord('f, c', '1.')] +
            chords(['g, b,'], rhythm) +
            chords(['c, c'], ['2.', 4]) + rests(4, 4) +
            chords(['c, c'], rhythm) +
            tied_chord('f, c', ['2.', 2]) + [chord('g, c', 4)] +
            chords(['a, c', 'g, b,'], '2.') +
            [chord('c, c', '1.', ornamentation='fermata')]
        )

        if not self.improvements:
            select(treble5, 1).prefix += '\\clef "bass" '
            select(treble5, 15).prefix += '\\clef "treble" '
        select(treble5, 15).dynamics = 'p'
        select(treble5, 41).phrasing = '~'
        select(treble5, 22).dynamics = 'pp'
        select(treble5, 33).dynamics = 'p\\>'
        select(treble5, 35).dynamics = '!'
        select(treble5, 42).markdown = '\\italic{rall.}'
        select(treble5, 44).dynamics = 'ppp'
        select(treble5, len(treble5)).suffix = doublethick_barbreak

        select(bass5, 14).markdown = '\\italic{Ped. o Mani}'

        if self.improvements:
            select(treble1, 1).prefix = (
                '<< { \\voiceOne ' + select(treble1, 1).prefix)
            select(bass1, 1).prefix = (
                '} \\new Voice { \\voiceTwo ') + select(bass1, 1).prefix
            select(bass5, len(bass5)).suffix += '} >> \\oneVoice'
            self.score = {'super': (
                treble1 + treble2 + repeat(treble3) + treble4 + treble5 +
                bass1 + bass2 + bass3 + bass4 + bass5)}
        else:
            self.score = {
                'treble': (
                    treble1 + treble2 + repeat(treble3) + treble4 + treble5),
                'bass': bass1 + bass2 + bass3 + bass4 + bass5
            }


if __name__ == "__main__":
    Priere()
