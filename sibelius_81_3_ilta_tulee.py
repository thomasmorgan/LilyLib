from piece import Piece
from staves import Treble, Dynamics, Bass
from points import notes, rests, chords, merge, chord, add
from util import rep, flatten, subset, select
from markup import slur, voices
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
        return '\\paper { #(set-paper-size "letter")}\n'

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
        # combine
        ###########

        self.score = {
            'treble': (
                treble_1 + treble_2 + treble_3 + treble_4 +
                treble_5 + treble_6),
            'dynamics': rests(1, 1, 1, 1),
            'bass': bass_1 + bass_2 + bass_3 + bass_4 + bass_5 + bass_6,
            'pedal': rests(1, 1, 1, 1)
        }


if __name__ == "__main__":
    IltaTulee()
