from piece import Piece
from keys import FMajor


class ChromaticScales(Piece):

    def write_score(self):
        self.title = "Chromatic Scales in C and F Major"

        # The scale section uses the scale function to build a scale from one note to the next
        self.score["treble"] = self.chromatic('c`', 'c``', dur=16)
        self.score["bass"] = self.chromatic('c', 'c`', dur=16)
        self.score["treble"][-1].dur = 4
        self.score["bass"][-1].dur = 4

        self.score["treble"] += self.chromatic('f`', 'f``', dur=16, key=FMajor)
        self.score["bass"] += self.chromatic('f', 'f`', dur=16, key=FMajor)
        self.score["treble"][-1].dur = 4
        self.score["bass"][-1].dur = 4


ChromaticScales()
