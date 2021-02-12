from piece import Piece
from points import notes


class MiddleC(Piece):

    def details(self):
        self.title = "Middle C"

    def write_score(self):
        self.score["treble"] = notes('c` c` f` e`', '4 8 4. 4') * 2
        self.score["bass"] = notes('c g g c', '4. 8 8 4.') * 2


if __name__ == "__main__":
    MiddleC()
