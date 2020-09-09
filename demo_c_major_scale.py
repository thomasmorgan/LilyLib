from piece import Piece


class CMajorScale(Piece):

    def details(self):
        self.title = "C Major Scale"

    def write_score(self):
        self.score["treble"] = self.scale("c`", "c``", 8) + self.scale("c``", -8, 8)
        self.score["bass"] = self.scale("c`", "c", 8) + self.scale("c", 8, 8)


def main():
    CMajorScale()
