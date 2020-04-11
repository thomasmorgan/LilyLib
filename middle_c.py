from piece import Piece
from models import Note


class MiddleC(Piece):

    def __init__(self):
        super().__init__()
        self.title = "Middle C"
        self.score["treble"] = Note("c`", 1)
        self.score["bass"] = Note("c`", 1)
        print(self)


MiddleC()
