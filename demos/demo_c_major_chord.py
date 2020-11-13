from piece import Piece
from points import chord


class CMajorChord(Piece):

    def details(self):
        self.title = "C Major Chord"

    def write_score(self):
        self.score["treble"] = chord("c` e` g` c``", 1)
        self.score["bass"] = chord(["c,", "c"], 1)


if __name__ == "__main__":
    CMajorChord()
