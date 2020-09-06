from piece import Piece


class MiddleC(Piece):

    def details(self):
        self.title = "Middle C"

    def write_score(self):
        self.score["treble"] = self.notes("c`", 1)
        self.score["bass"] = self.notes("c`", 1)


MiddleC()
