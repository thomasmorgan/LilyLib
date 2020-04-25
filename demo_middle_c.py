from piece import Piece
from models import Note


class MiddleC(Piece):

    def details(self):
        self.title = "Middle C"

    def write_score(self):
        self.score["treble"] = Note("c`", 1)
        self.score["bass"] = Note("c`", 1)


MiddleC()
