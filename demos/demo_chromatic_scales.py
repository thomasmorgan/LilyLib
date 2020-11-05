from piece import Piece


class ChromaticScales(Piece):

    def details(self):
        self.title = "Chromatic Scales in C and F Major"

    def write_score(self):
        # The scale section uses the scale function to build a scale from one note to the next
        self.score["treble"] = self.chromatic('c`', 'c``', [16] * 12 + [4])

        self.set_key("f major")
        self.score["treble"] += self.key_signature + self.chromatic('f`', 'f``', [16] * 12 + [4])

        self.score["bass"] = self.transpose(self.score["treble"], -1)


if __name__ == "__main__":
    ChromaticScales()