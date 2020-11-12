from piece import Piece
from points import note


class MiddleC(Piece):

    def details(self):
        self.title = "Middle C"

    def write_score(self):
        self.score["treble"] = note("c`", 1)
        self.score["bass"] = note("c`", 1)


if __name__ == "__main__":
    MiddleC()
