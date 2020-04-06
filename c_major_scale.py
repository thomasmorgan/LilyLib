from score import Score
from models import Note


class CMajorScale(Score):

    def __init__(self):
        super().__init__()
        self.title = "C Major Scale"
        self.score["treble"] = [Note("c`", 8), Note("d`", 8), Note("e`", 8), Note("f`", 8), Note("g`", 8), Note("a`", 8), Note("b`", 8), Note("c``", 8)]
        self.score["bass"] = [Note("c", 8), Note("d", 8), Note("e", 8), Note("f", 8), Note("g", 8), Note("a", 8), Note("b", 8), Note("c`", 8)]
        print(self)


CMajorScale()
