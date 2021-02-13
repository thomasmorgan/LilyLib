from piece import Piece
from points import rest, note, notes, merge
from markup import voices
from util import rep, flatten
from staves import Treble, Bass


class Alleluia(Piece):

    def details(self):
        self.title = "Alleluia"
        self.composer = "Charles Valentin Alkan"
        self.opus = "Op. 25"
        self.staves = [Treble(), Bass()]
        self.staves[1].clef = '"bass_8"'
        self.tempo = "12/8"
        self.key = "F Major"

    def write_score(self):
        melody = [[]] * 20
        melody[0] = notes('c`` f`` g``', 8)
        melody[1] = rep(note('a``', 8), 7) + self.scale('g``', 3, 8) + self.scale('d``', 2, 8)
        melody[2] = note('e``', 8), rep(note('f``', 8), 8) + self.scale('g``', 3, 8)
        melody = flatten(melody)

        treble1 = merge(melody, self.transpose(melody, 2), self.transpose(melody, 1, 'octave'))
        treble1[0].prefix = '\\partial 4.'

        treble2 = self.harmonize(self.transpose(melody, -1, 'octave'), -5)
        treble2[0].tones = ['c`']

        bass = rest('4.') + self.harmonize(notes('f, c, f,', '2. 2. 1.'), -1, 'octave')

        i = 3
        for b in bass:
            treble2[i].tones = []
            dur = b.dur
            if dur == '2.':
                i += 6
            if dur == '1.':
                i += 12

        self.score = {
            'treble': voices(treble1, treble2),
            'bass': bass
        }


if __name__ == "__main__":
    Alleluia()
