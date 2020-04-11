from piece import Piece
from models import Note
from keys import CMajor, DMajor, EMajor, FMajor, GMajor, AMajor, BMajor


class CMajorModalScales(Piece):

    def __init__(self):
        super().__init__()
        self.title = "C Major Modal Scales"
        self.create_sections("basic", "scale", "looped", "super")

        self.score["treble"]["basic"] = [Note("c`", 8), Note("d`", 8), Note("e`", 8), Note("f`", 8), Note("g`", 8), Note("a`", 8), Note("b`", 8), Note("c``", 8)]
        self.score["bass"]["basic"] = [Note("c", 8), Note("d", 8), Note("e", 8), Note("f", 8), Note("g", 8), Note("a", 8), Note("b", 8), Note("c`", 8)]

        self.score["treble"]["scale"] = self.scale('d`', 'd``', dur=8)
        self.score["bass"]["scale"] = self.scale('d', 'd`', dur=8)

        self.score["treble"]["looped"] = []
        for start in ['e`', 'f`', 'g`', 'a`', 'b`', 'c``']:
            self.score["treble"]["looped"] += [Note(t, 8) for t in self.key.scale(start, start + '`')]
        self.score["bass"]["looped"] = []
        for start in ['e', 'f', 'g', 'a', 'b', 'c`']:
            self.score["bass"]["looped"] += [Note(t, 8) for t in self.key.scale(start, start + '`')]

        keys = [CMajor, BMajor, AMajor, GMajor, FMajor, EMajor, DMajor, CMajor]
        self.score["treble"]["super"] = []
        self.score["bass"]["super"] = []
        for start, key in zip(self.key.scale('c```', 'c``'), keys):
            self.score["treble"]["super"] += self.scale(str(start), str(start)[:-1], key=key, dur=8)
            self.score["bass"]["super"] += self.scale(str(start)[:-1], str(start)[:-2], key=key, dur=8)

        print(self)


CMajorModalScales()
