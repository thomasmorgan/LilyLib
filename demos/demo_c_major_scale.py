from piece import Piece
from points import scale


class CMajorScale(Piece):

    def details(self):
        self.title = "C Major Scale"

    def write_score(self):
        self.score["treble"] = scale("c`", "c``", 'C Major', 8) + scale("c``", -8, 'C Major', 8)
        self.score["bass"] = self.scale("c`", "c", 8) + self.scale("c", 8, 8)


if __name__ == "__main__":
    CMajorScale()
