from piece import Piece
from points import chord, rests, tied_note, notes, tied_chord, chords, replace
from markup import slur, voices, italic, thinthick_barbreak, pagebreak
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
            Treble(_with='\\override Beam.breakable = ##t'),
            Dynamics(),
            Bass(_with='\\consists "Mark_engraver"'),
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
            [chord('cs g', 2, phrasing='_(^(')] +
            [chord('ds a', 2, phrasing='_)_(^)^(')] +
            [chord('e g', 1, phrasing='_)^)')])
        select(bass_4, 6).phrasing = '_(^('
        select(bass_4, 7).phrasing = ')'

        ###########
        # part 5
        ###########

        high_treble_5 = (
            notes('e`', '2.') + melody_2() + notes('e`', 1, phrasing='~') +
            notes('e`', 1))

        bass_5 = (
            rep(subset(bass_4, 1, 10), 1) +
            [chord('e g', 1, phrasing='_)^)~')] +
            [chord('e g', 1, phrasing='~')] +
            [chord('e g', 1)])

        select(bass_5, len(bass_5)).prefix = select(bass_5, 1).prefix + (
            '\\override Staff.RehearsalMark.direction = #DOWN\n'
            "\\override Staff.RehearsalMark.rotation = #'(180 0 0)")
        select(bass_5, len(bass_5)).suffix += (
            '\\mark \\markup { \\smaller \\smaller '
            '\\musicglyph "scripts.ufermata" }')

        ###########
        # part 6
        ###########

        treble_6 = rep(subset(treble_1, 1, 6), 1) + tied_chord('b e`', [2, 1])
        bass_6 = (
            rep(subset(bass_1, 1, 6), 1) +
            voices(
                tied_chord('e g', [2, 1]),
                rests(2, prefix='\\omit ') + [chord('e,, g,, e,', 1)]))

        ###########
        # dynamics
        ###########

        dynamics = (
            rests(1, markup='\\dynamic{p} \\italic{dolce}') + rests(1, 2) +
            rests(2, dynamics='>') + rests(4) + rests('2', dynamics='!') +
            rests(4, markup=italic('dolce')) + rep(rests(1), 7) +
            rests(8, dynamics='>') + rests(8, dynamics='!') + rests('2.', 1) +
            rests(2, dynamics='>') + rests(2, dynamics='!') + rests(1, 1) +
            rests(4, dynamics='>') + rests(4, dynamics='!') + rests(8) +
            rests(8, markdown=italic('  più ') + '\\dynamic{p}') + rests(4) +
            rests(1) + rests('4.', dynamics='>') + rests(8, dynamics='!') +
            rests(2) + rests(2, 4, 8) +
            rests(8, markup=italic('dim. e allargando')) + rests(2, 8) +
            rests('4.', dynamics='>') + rests(1) + rests(1, dynamics='!') +
            rests(1, dynamics='pp') + rests(1, 1, 1))

        ###########
        # pedal
        ###########

        on = '\\sustainOn '
        off = '\\sustainOff '

        pedal = (
            rests(1, 1, 2) + rests(2, suffix=on) + rests(2, 4, 8) +
            rests(8, suffix=off) + rests(1, 1, 1) + rests(1, suffix=on) +
            rests('4.') + rests(8, suffix=off) + rests(2) +
            rests('4.', suffix=on) + rests(8, suffix=off) + rests(2) +
            rests(1) + rests(1, suffix=on) + rests(2, 4, 8) +
            rests(8, suffix=off + pagebreak) + rests(1, 1, 1) +
            rests(1, suffix=on) +
            rests(2, 4, 8) + rests(8, suffix=off) + rests(1) +
            rests(2, 2, 1, suffix=on) + rests(1) +
            rests(2, 4, 8, 16, 32, 64, 128) +
            rests(128, suffix='\\tweak X-offset #-0.4 ' + off) +
            rests(1, 1, 2) +
            rests(2, suffix=on) + rests(2, 4, 8) + rests(8, suffix=off))

        ###########
        # markup
        ###########

        select(high_treble_2, 3).markup = italic('cantabile')
        select(treble_6, 1).prefix = '\\tempo "  Lento"'
        select(treble_6, len(treble_6)).ornamentation = 'fermata'
        select(treble_6, len(treble_6)).suffix += thinthick_barbreak

        ###########
        # combine
        ###########

        self.score = {
            'treble': (
                voices(rests(1, 1, 1, prefix='\\omit ') + high_treble_2,
                       treble_1 + low_treble_2) +
                voices(high_treble_3 + high_treble_4 + high_treble_5,
                       low_treble_345) + treble_6),
            'dynamics': dynamics,
            'bass': (
                bass_1 + bass_2 + bass_3 + bass_4 + bass_5 + bass_6),
            'pedal': pedal
        }


if __name__ == "__main__":
    SydamestaniRakastan()
