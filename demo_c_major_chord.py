from piece import Piece
from models import Chord


class CMajorChord(Piece):

    def details(self):
        self.title = "C Major Chord"

    def write_score(self):
        self.score["treble"] = Chord("c` e` g` c``", 1)
        self.score["bass"] = Chord("c, c", 1)


CMajorChord()
