from piece import Piece


class MiddleC(Piece):

    def details(self):
        self.title = "Middle C"

    def write_score(self):
        self.score["treble"] = self.note("c`", 1)
        self.score["bass"] = self.note("c`", 1)


if __name__ == "__main__":
    MiddleC()
