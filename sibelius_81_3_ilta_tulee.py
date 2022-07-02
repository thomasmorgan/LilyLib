from piece import Piece
from staves import Treble, Dynamics, Bass
from points import notes, rests, chords, merge
from util import rep, flatten
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

        high_treble_2 = deepcopy(high_treble_1)
        low_treble_2 = rep(tremolo(), 4)
        treble_2 = voices(high_treble_2, low_treble_2)
        top_scale = 'cs` a gs fs'
        bottom_scale = 'e es es fs'
        high_bass_chords = merge(notes(top_scale, 4), notes(bottom_scale, 4))
        high_bass_2 = (
            rep(high_bass_chords, 3) +
            notes('e cs', 2))
        low_bass_notes = flatten(
            [[n] + notes('a,', 8) for n in notes(bottom_scale, 8)])
        low_bass_2 = (
            rep(low_bass_notes, 3) + slur(notes('e e, a,, e,', 8)) +
            slur(notes('cs es, a,, es,', 8)))
        bass_2 = voices(high_bass_2, low_bass_2)
        ###########
        # combine
        ###########

        self.score = {
            'treble': treble_1 + treble_2,
            'dynamics': rests(1, 1, 1, 1),
            'bass': bass_1 + bass_2,
            'pedal': rests(1, 1, 1, 1)
        }


if __name__ == "__main__":
    IltaTulee()
