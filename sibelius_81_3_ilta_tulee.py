from piece import Piece
from staves import Treble, Dynamics, Bass
from points import notes, rests, chords, merge, chord
from util import rep, flatten, subset, select
from markup import slur, voices
from copy import deepcopy


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
            high_chords = merge(notes(top, 4), notes(bottom, 4))
            low_notes = flatten(
                [[n] + notes(held_note, 8) for n in notes(bottom, 8)])
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
            select(bass_3, 38).prefix + '\\mergeDifferentlyHeadedOn')
        select(bass_3, 43).phrasing += '~'

        ###########
        # combine
        ###########

        self.score = {
            'treble': treble_1 + treble_2 + treble_3,
            'dynamics': rests(1, 1, 1, 1),
            'bass': bass_1 + bass_2 + bass_3,
            'pedal': rests(1, 1, 1, 1)
        }


if __name__ == "__main__":
    IltaTulee()
