from piece import Piece
from staves import Treble, Dynamics, Bass
from points import (
    notes, rests, chords, merge, chord, add, replace, tied_note, tied_chord)
from util import rep, flatten, subset, select
from markup import (
    slur, voices, italic, clef, crescendo, diminuendo, thinthick_barbreak)
from copy import deepcopy
from tones import tonify


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
            '\\paper { #(set-paper-size "letter")}\n'
            '#(set-global-staff-size 19)\n'
            '\\paper { page-count = #2 }\n'
        )

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
        # part 2
        ###########

        def lh_motif(top, bottom, held_note):
            length = max([len(tonify(top)), len(tonify(bottom)),
                          len(tonify(held_note))])
            high_chords = merge(notes(top, [4]*length),
                                notes(bottom, [4]*length))
            low_notes = flatten(
                [[n] + notes(held_note, 8)
                 for n in notes(bottom, [8]*length)])
            return(voices(high_chords, low_notes))

        high_treble_2 = deepcopy(high_treble_1)
        low_treble_2 = rep(tremolo(), 4)
        treble_2 = voices(high_treble_2, low_treble_2)

        bass_2 = (
            rep(lh_motif('cs` a gs fs', 'e es es fs', 'a,'), 3) +
            voices(notes('e cs', 2),
                   slur(notes('e e, a,, e,', 8)) +
                   slur(notes('cs es, a,, es,', 8))))

        ###########
        # part 3
        ###########

        treble_3 = voices(
            deepcopy(high_treble_1),
            subset(deepcopy(low_treble_2), 1, 53) +
            self.scale('cs`', 'fs``', 16))
        select(treble_3, 29).tones = []

        bass_3 = (
            lh_motif('fs a gs es fs a', 'cs fs es cs cs cs', 'a,') +
            voices([chord('ds cs`', 2)],
                   rests('8.') + notes('b,, fs, b, ds fs', 16)) +
            lh_motif('cs` a gs es', 'a ds ds ds', 'b,') +
            voices(chords(['ds fs'], [2, 2]),
                   rep(slur(notes('ds b,, fs, ds', 8)), 2)))
        select(bass_3, 38).prefix = (
            select(bass_3, 38).prefix + '\\mergeDifferentlyHeadedOn ')
        select(bass_3, 43).phrasing += '~'

        ###########
        # part 4
        ###########

        def lh_motif_2(top, bottom, held_note):
            high_chords = add(notes(bottom, [8, 8, 8, 8]), top)
            melody = []
            for i in range(4):
                melody += notes(held_note, 8) + [high_chords[i]]
            return melody

        treble_4 = (
            voices(
                rep(notes('gs`` e`` ds`` cs``', 4, articulation='>'), 3),
                rep(notes('gs`` gs` b` gs` e`` e` gs` e` '
                          'ds`` ds` gs` ds` cs`` cs` gs` cs`', 16), 3)) +
            voices(
                notes('b` gs`', 2, articulation='>'),
                notes('b` b', 16) + rep(notes('e` b', 16), 3) +
                notes('gs` b', 16) + rep(notes('e` b', 16), 3)))
        select(treble_4, 13).prefix = (
            select(treble_4, 13).prefix + '\\mergeDifferentlyHeadedOn ')

        bass_4 = (
            rep(lh_motif_2('gs', 'b, bs, bs, cs', 'e,'), 3) +
            lh_motif_2('gs', 'b,', 'e,'))

        ###########
        # part 5
        ###########

        high_treble_5 = deepcopy(high_treble_1)
        low_treble_5 = (
            rep(tremolo(), 3) + subset(tremolo(), 1, 11) +
            self.scale('e`', 5, 16))
        select(low_treble_5, 25).tones = []
        treble_5 = voices(high_treble_5, low_treble_5)

        bass_5 = (
            lh_motif('fs a gs es fs a', 'ds', 'b,') +
            deepcopy(subset(bass_3, 19, len(bass_3))))

        ###########
        # part 6
        ###########

        def mini():
            return notes('cs` ds` cs`', 16)

        def minis():
            return (notes('cs``', 16) + mini() + notes('a`', 16) + mini() +
                    notes('gs`', 16) + mini() + notes('fs`', 16) + mini())

        treble_6 = voices(
            notes('cs``', [1, 1, 1, 1], articulation='>'),
            minis() + tremolo() + minis() + tremolo(),
            (rep(notes('cs``', 4, prefix='\\tweak X-offset #-0.25 '
                                         '\\tweak Stem.X-offset #1 ') +
             notes('a` gs` fs`', 4, articulation='>') +
             rests(1, prefix='%{ spacer %}'), 2)))
        select(treble_6, 1).prefix = (
            select(treble_6, 1).prefix + '\\mergeDifferentlyHeadedOn ')

        bass_6 = (
            lh_motif('e es es fs', 'cs', 'a,') +
            lh_motif('cs` a gs fs', 'e es es fs', 'a,'))
        select(bass_6, 1).phrasing = '('
        select(bass_6, 2).phrasing = ')'
        select(bass_6, 3).phrasing = '('
        select(bass_6, 4).phrasing = ')'
        select(bass_6, 13).articulation = '>'
        select(bass_6, 14).articulation = '>'
        select(bass_6, 15).articulation = '>'
        select(bass_6, 16).articulation = '>'
        bass_6 = rep(bass_6, 2)

        ###########
        # part 7
        ###########

        treble_7 = (
            rep(voices(notes('cs``', 1, articulation='>'), tremolo()), 5) +
            rep(voices(notes('cs``', 1, articulation='>',
                             markup=italic('m. s.')),
                       rep(notes('ds` cs`', 16), 8)), 2) +
            [chord('a fs`', 1, ornamentation='fermata')])

        def rumblet():
            return notes('es, a,, es,', 8)

        def rumble():
            return subset(rumblet(), 1, 2) + tied_note('es,', [8, 8])

        bass_7 = (
            voices(
                notes('e cs', 1),
                slur(replace(notes('cs', 8) + rumble() + rumblet(),
                             'es,', 'e,')) +
                notes('cs', 8) + rep(rumble(), 5) + rumblet() +
                tied_chord('a,, es,', [1, 1, '2.']) + rests(4)) +
            clef('treble', notes('cs``', 1, suffix='_\\fermata',
                                 articulation='>')))
        select(bass_7, 11).phrasing += '('
        select(bass_7, 18).phrasing += ')'
        select(bass_7, 19).prefix = '\\stemUp '
        select(bass_7, 19).phrasing += '('
        select(bass_7, 26).phrasing += ')'
        select(bass_7, 27).phrasing += '('
        select(bass_7, 34).phrasing += ')~'
        select(bass_7, len(bass_7)).suffix += thinthick_barbreak

        ###########
        # dynamics
        ###########

        dynamics = (
            rests(1, dynamics='pp') + rests(1) +  # part 1
            rests(1, markup=italic('segue legato')) + rests(1) +
            rests(1, markup='\\dynamic{mp} \\italic{ ben marcato}') +  # part 2
            rests(1, 1, 1) +
            rests(1) + crescendo(rests('4..', 16)) + rests(2) +  # part 3
            rests('4.') + diminuendo(rests(8, 2, 4)) +
            rests(16) + rests(16, dynamics='<') + rests(8, 2) +
            rests(4, dynamics='!', markup=italic('poco ') + '\\dynamic{f}') +
            diminuendo(rests(2, 16, '8.')) + diminuendo(rests('2.', 4)) +
            rests('8.') + diminuendo(rests(16, 4, 4, 4)) + rests(1) +
            rests(1, dynamics='mf') + crescendo(rests('4..', 16)) + rests(2) +
            rests('4.') +
            rests(8, prefix='\\once \\override Hairpin.to-barline = ##f ',
                  dynamics='>') + rests(2) + rests(1, dynamics='!') +
            rests(1, dynamics='mf') + rests(1) +
            rests(1, markup=italic('poco a poco dim.')) + rests(1, 1, 1) +
            rests(2, 8) + rests('4.', markup=italic('dim. molto')) +
            rests(1, 1) + rests(1, dynamics='pp') +
            diminuendo(rests(4, 4, 4, 4)) + rests(1, dynamics='ppp'))

        ###########
        # pedal
        ###########

        on = '\\sustainOn '
        off = '\\sustainOff '

        pedal = (
            rests(1, suffix=on) +  # bar 1
            rests(1, 1, 1) +  # bars 2-4
            rep(rests(4, 4, suffix=on) + rests(16) + rests(16, suffix=off) +
                rests(8, 4), 3) +  # bars 5 - 7
            rep(rests('4.', suffix=on) + rests(8, suffix=off), 2) +  # bar 8
            rests(2, suffix=on) + rests(16) + rests(16, suffix=off) +
            rests(8, 4) +  # bar 9
            rests(4, suffix=on) + rests(16) + rests(16, suffix=off) +
            rests(8) + rests(2, suffix=on) +  # bar 10
            rests(16) + rests(16, suffix=off) + rests(8) +
            rests(2, suffix=on) + rests(16) + rests(16, suffix=off) +
            rests(8) +  # bar 11
            rests(1, suffix=on) +  # bar 12
            rep(rests(4, 4, suffix=on) + rests(4) +
                rests(4, suffix=off), 3) +  # bars 13 - 15
            rests('2..', suffix=on) + rests(8, suffix=off) +  # bar 16
            rests(1, suffix=on) +  # bar 17
            rests('4.', 8, suffix=on) + rests(2) +  # bar 18
            rests(8) + rests(8, suffix=off) + rests(4, suffix=on) +
            rests('8.') + rests(16, suffix=off) + rests(4) +  # bar 19
            rests('2..', suffix=on) + rests(8, suffix=off) +  # bar 20
            rep(rests(4, 2, suffix=on) + rests(4, suffix=off), 2) +  # b 21-22
            rests(4, '4.', suffix=on) + rests('4.', suffix=off) +  # bar 23
            rests(4, 2, suffix=on) + rests(4, suffix=off) +  # bar 24
            rests(1, 1, suffix=on) +  # bars 25-26
            rests(1, 1, 1, 1) +  # bars 27-30
            rests('2..') + rests(8, suffix=off) +  # bar 31
            rests(1, suffix=on)  # bar 32
        )

        ###########
        # combine
        ###########

        self.score = {
            'treble': (
                treble_1 + treble_2 + treble_3 + treble_4 +
                treble_5 + treble_6 + treble_7),
            'dynamics': dynamics,
            'bass': (
                bass_1 + bass_2 + bass_3 + bass_4 + bass_5 + bass_6 + bass_7),
            'pedal': pedal
        }


if __name__ == "__main__":
    IltaTulee()
