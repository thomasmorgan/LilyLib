from piece import Piece
from points import rests, merge


class Merge(Piece):

    def details(self):
        self.title = "Merged Scales"

    def write_score(self):
        scale_1 = self.scale("c`", 8, 8)
        scale_2 = self.scale("c``", -8, 8)

        self.score["treble"] = scale_1 + scale_2 + merge(scale_1, scale_2)
        self.score["bass"] = rests(1, 1, 1)


if __name__ == "__main__":
    Merge()
