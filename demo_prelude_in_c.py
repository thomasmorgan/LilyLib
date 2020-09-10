from piece import Piece


class PreludeInC(Piece):

    def details(self):
        self.title = "Prelude in C"
        self.composer = "J. S. Bach"
        self.opus = "BVW 846"
        self.tempo = "4/4"

    def motif(self, tones):
        notes = self.notes(tones, 16)
        self.score["bass"] += 2 * (notes[0:2] + self.rests([8, 4]))
        self.score["treble"] += 2 * (self.rests(8) + 2 * (notes[2:]))

    def write_score(self):
        self.score["treble"] = []
        self.score["bass"] = []

        shapes = [
            self.arpeggio('c`', 'e``'),
            self.tones('c` d`') + self.arpeggio('a`', 'f``', root='d'),
            self.arpeggio('b', 'g`', root='g') + self.arpeggio('d``', 'f``', root='d'),
            self.arpeggio('c`', 'e``')
        ]

        for s in shapes:
            self.motif(s)


if __name__ == "__main__":
    PreludeInC()
