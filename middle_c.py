from score import Score
from models import Note


class MiddleC(Score):

    def __init__(self):
        super().__init__()
        self.title = "Middle C"
        self.score["treble"] = Note("c`", 1)
        self.score["bass"] = Note("c`", 1)
        print(self)


MiddleC()
