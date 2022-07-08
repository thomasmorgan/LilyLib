from piece import Piece
from staves import Treble, Bass, Dynamics
from points import rests, notes, chords, tied_note, chord, tied_chord
from markup import slur, voices, clef, thinthick_barbreak, italic
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
            Treble(
                _with='\\consists "Span_arpeggio_engraver"',
                extra_text=(
                    '\\set Score.connectArpeggios = ##t\n'
                    '\\override Score.Arpeggio.stencil = '
                    '#ly:arpeggio::brew-chord-slur\n'
                    "\\override Score.Arpeggio.X-extent = #'(-0.9 . -0.2)\n"
                    '\\revert Score.Arpeggio.dash-definition\n')),
            Dynamics(),
            Bass(),
            Dynamics('pedal')]

    def subtext(self):
        return (
            "\\layout { \\context { \\Score \\override "
            "SpacingSpanner.base-shortest-duration = "
            "#(ly:make-moment 1/16)}}\n"
            '\\paper { page-count = #2 }\n'
            '\\paper { #(set-paper-size "letter")}\n')

    def write_score(self):

        #########
        # part 1
        #########

        def bass_motif():
            motif = slur(notes('gs, a, fs, bs, a, gs, fs, fs,,', 8))
            select(motif, 1).phrasing = '^('
            return motif

        treble_1 = rests(1, 1, 1, 1, prefix='%{ full %} ')
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
        # part 3
        #########

        treble_3 = (
            [chord('fs a ds`', 1)] + rests(1, 1, prefix='%{ full %} ') +
            clef('bass', notes('fs fs fs', 4, articulation='-')) +
            notes('gs fs', 8) + slur(notes('e ds', ['4.', 8])) +
            notes('cs', 4, articulation='-') + notes('cs ds', 8) +
            notes('e', 4, articulation='-') + notes('e e', 8) +
            notes('ds ds', 4, articulation='-') + notes('cs', 1) +
            rests(1, prefix='%{ full %} ')
        )

        bass_3 = voices(
            notes('bs,', 1) + rep(rests(1, prefix='%{ spacer %}'), 7),
            rests(8) + rep(bass_motif(), 6) +
            slur(notes('b, bs, a, ds b, fs ds a fs bs a ds` bs fs` ds`', 8))
        )
        select(bass_3, 10).phrasing = '_('
        select(bass_3, 17).prefix = '\\stemUp '
        select(bass_3, len(bass_3)-14).phrasing = '^('

        #########
        # part 4
        #########

        treble_4 = (
            clef('treble', notes('e` e` e` e` b` b` fs` g` a`', 4)) +
            notes('a` b`', 8) + notes('a` g`', 4))

        bass_4 = voices(
            chord_motif('e g cs`') +
            rep(chord_motif('e g cs`', 'fs a ds`'), 2),
            rests(2) + tied_note('fs,,', [2, 4]) + rests(4, 2, 1))
        select(bass_4, 8).articulation = '>'
        select(bass_4, 13).articulation = '>'

        #########
        # part 5
        #########

        treble_5 = (
            tied_chord('c` fs`', [1, 4]) + rests(4, 2) +
            rests(1, prefix='%{ full %} ') +
            rep(
                notes('fs fs fs', 4) + notes('gs fs', 8) +
                slur(notes('e ds', ['4.', 8])) + notes('cs', 4) +
                notes('cs ds', 8) + notes('e', [4, 8, 8]) +
                notes('ds ds', 4) + notes('cs', 1) +
                rests(1, prefix='%{ full %} '), 2) +
            rests(1, 1, prefix='%{ full %} ')
            )
        select(treble_5, 1).phrasing = '^~\\arpeggio'
        select(treble_5, 6).prefix += '\\clef "bass" '

        bass_5 = voices(
            tied_chord('ds a', [1, 4]) + rests(4, 2) +
            rep(rests(1, prefix='%{ spacer %}'), 13),
            rests(1, 8) + rep(bass_motif(), 13)
        )
        select(bass_5, 1).ornamentation = 'arpeggio'
        select(bass_5, 27).prefix += '\\stemUp '
        select(bass_5, len(bass_5)).dur = 1
        select(bass_5, len(bass_5)).suffix = (
            '^\\fermata' + select(bass_5, len(bass_5)).suffix)
        select(bass_5, len(bass_5)).suffix += thinthick_barbreak

        #########
        # dynamics
        #########

        dynamics = (
            rests(1, dynamics='p') + rests(1, 4) + rests('2.', dynamics='<') +
            rests(2) + rests(2, dynamics='!') + rests(4, dynamics='mf') +
            rests('2.', dynamics='<') + rests(16) + rests(16, dynamics='!') +
            rests(16, 4) + rests(4, dynamics='>') + rests(4, dynamics='!') +
            rests(16) + rests(1) + rests(4, dynamics='>') +
            rests('4.', dynamics='!') + rests('4.', markup=italic('dim.')) +
            rests(1, 1) + rests(1, dynamics='mp') + rests(1, 1, 2) +
            rests(2, dynamics='<') + rests(2, 8) + rests('4.', dynamics='!') +
            rests(8, dynamics='mf') + rests('2..', dynamics='<') +
            rests(1, dynamics='!') + rests(1, 1, 2) +
            rests(2, markup=italic('dim.')) + rests(1) +
            rests(1, dynamics='mp') + rests(1, 1, 2) +
            rests(2, markup=italic('dim.')) + rests(1) +
            rests(1, markup='\\italic{più } \\dynamic{p}') + rests(1, 2) +
            rests(2, markup=italic('dim. e allarg.')) + rests(1, 1, 1, 1)
        )

        #########
        # pedal
        #########

        def on(dur):
            return rests(dur, suffix='\\sustainOn')

        def off(dur):
            return rests(dur, suffix='\\sustainOff')

        pedal = (
            on(2) + rests(8) + off('4.') +
            on(2) + rests(8) + off('4.') +
            on(1) + rests('2..') + off(8) +
            on(1) + rests(8) + off(8) + on(2) + off(4) +
            rests('4.') + on('4.') + off(4) +
            rep(on(2) + rests('8.') + off(16) + rests(4), 6) +
            on(1) + rests(2, 4, 8, 16) + off(16) +
            rests(8) + on(8) + rests('2.') +
            rests(8) + off(8) + on(2) + off(4) +
            rests('4.') + on('4.') + off(4) + on(1) +
            rests(2, '8.') + off('8.') + rests(8) +
            rep(on(2) + rests('8.') + off('8.') + rests(8), 7) +
            on(1) +
            rep(on(2) + rests('8.') + off('8.') + rests(8), 5)
        )

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
    Velisurmaaja()
