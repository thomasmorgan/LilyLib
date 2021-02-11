from piece import Piece
from markup import key_signature


class ChromaticScales(Piece):

    def details(self):
        self.title = "Chromatic Scales in C and F Major"

    def write_score(self):
        self.score["treble"] = self.chromatic('c`', 'c``', [16] * 12 + [4]) + self.chromatic('c``', 'c`', [16] * 12 + [4])

        self.set_key("f major")
        self.score["treble"] += key_signature(self.key, self.chromatic('f`', 'f``', [16] * 12 + [4])) + self.chromatic('f``', 'f`', [16] * 12 + [4])

        self.score["bass"] = self.transpose(self.score["treble"], -1, 'octave')


if __name__ == "__main__":
    ChromaticScales()
