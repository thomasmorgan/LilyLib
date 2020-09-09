from piece import Piece


class CMajorChord(Piece):

    def details(self):
        self.title = "C Major Chord"

    def write_score(self):
        self.score["treble"] = self.chord("c` e` g` c``", 1)
        self.score["bass"] = self.chord("c, c", 1)


def main():
    CMajorChord()
