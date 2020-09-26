from piece import Piece
from util import pattern


class PreludeInC(Piece):

    def details(self):
        self.title = "Prelude in C"
        self.composer = "J. S. Bach"
        self.opus = "BVW 846"

    def write_score(self):
        notes, tones, arpeggio, dominant7, rests, voices = self.notes, self.tones, self.arpeggio, self.dominant7, self.rests, self.voices
        ii, V = 'D Minor', 'G Major'
        self.score["treble"], self.score["bass"] = [], []

        def motif(tones):
            self.score["bass"] += 2 * voices(rests(16) + notes(pattern(tones, [2, 2]), ['8.', 4], "~ "), notes(pattern(tones, [1]), 2))
            self.score["treble"] += 2 * (rests(8) + notes(pattern(tones, [3, 4, 5, 3, 4, 5]), 16)) + ["\n"]

        shapes = [
            arpeggio('c`', 'e``'),
            tones('c` d`') + arpeggio('a`', 'f``', key=ii),
            pattern(dominant7('b', 'f``', key=V), [1, 2, 4, 6, 7]),
            arpeggio('c`', 'e``')
        ]

        for s in shapes:
            motif(s)


if __name__ == "__main__":
    PreludeInC()
