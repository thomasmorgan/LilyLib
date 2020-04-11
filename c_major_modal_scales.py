from piece import Piece
from models import Note


class CMajorModalScales(Piece):

    def __init__(self):
        super().__init__()
        self.title = "C Major Modal Scales"
        self.create_sections("basic", "scale", "looped", "super")

        self.score["treble"]["basic"] = [Note("c`", 8), Note("d`", 8), Note("e`", 8), Note("f`", 8), Note("g`", 8), Note("a`", 8), Note("b`", 8), Note("c``", 8)]
        self.score["bass"]["basic"] = [Note("c", 8), Note("d", 8), Note("e", 8), Note("f", 8), Note("g", 8), Note("a", 8), Note("b", 8), Note("c`", 8)]

        self.score["treble"]["scale"] = [Note(t, 8) for t in self.key.scale('d`', 'd``')]
        self.score["bass"]["scale"] = [Note(t, 8) for t in self.key.scale('d', 'd`')]

        self.score["treble"]["looped"] = []
        for start in ['e`', 'f`', 'g`', 'a`', 'b`', 'c``']:
            self.score["treble"]["looped"] += [Note(t, 8) for t in self.key.scale(start, start + '`')]
        self.score["bass"]["looped"] = []
        for start in ['e', 'f', 'g', 'a', 'b', 'c`']:
            self.score["bass"]["looped"] += [Note(t, 8) for t in self.key.scale(start, start + '`')]

        self.score["treble"]["super"] = []
        for start in self.key.scale('c```', 'c``'):
            self.score["treble"]["super"] += [Note(t, 8) for t in self.key.scale(str(start), str(start)[:-1])]
        self.score["bass"]["super"] = []
        for start in self.key.scale('c``', 'c`'):
            self.score["bass"]["super"] += [Note(t, 8) for t in self.key.scale(str(start), str(start)[:-1])]
        print(self)


CMajorModalScales()
