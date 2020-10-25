from piece import Piece
from staves import Bass


class DemoScale(Piece):

    def details(self):
        self.title = "Demo Scale"
        self.key = 'C Minor'
        self.staves = [Bass()]

    def write_score(self):
        self.score["bass"] = self.scale('c`', 'c', ['8.', 16])


if __name__ == "__main__":
    DemoScale()
