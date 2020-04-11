from piece import Piece
from models import Note
from keys import CMajor, DMajor, EMajor, FMajor, GMajor, AMajor, BMajor


class CMajorModalScales(Piece):

    def __init__(self):
        super().__init__()
        self.title = "C Major Modal Scales"
        self.create_sections("basic", "notes", "scale", "looped", "super")

        self.score["treble"]["basic"] = [Note("c`", 8), Note("d`", 8), Note("e`", 8), Note("f`", 8), Note("g`", 8), Note("a`", 8), Note("b`", 8), Note("c``", 8)]
        self.score["bass"]["basic"] = [Note("c", 8), Note("d", 8), Note("e", 8), Note("f", 8), Note("g", 8), Note("a", 8), Note("b", 8), Note("c`", 8)]

        self.score["treble"]["notes"] = self.notes('d` e` f` g` a` b` c`` d``', dur=8)
        self.score["bass"]["notes"] = self.notes('d e f g a b c` d`', dur=8)

        self.score["treble"]["scale"] = self.scale('e`', 'e``', dur=8)
        self.score["bass"]["scale"] = self.scale('e', 'e`', dur=8)

        self.score["treble"]["looped"] = []
        self.score["bass"]["looped"] = []
        for start in ['f`', 'g`', 'a`', 'b`', 'c``']:
            self.score["treble"]["looped"] += [Note(t, 8) for t in self.key.scale(start, start + '`')]
            self.score["bass"]["looped"] += [Note(t, 8) for t in self.key.scale(start[:-1], start)]

        keys = [CMajor, BMajor, AMajor, GMajor, FMajor, EMajor, DMajor, CMajor]
        notes = self.key.scale('c```', 'c``')
        self.score["treble"]["super"] = [self.scale(str(start), str(start.shift(-1)), key=key, dur=8) for start, key in zip(notes, keys)]
        self.score["bass"]["super"] = [self.scale(str(start.shift(-1)), str(start.shift(-2)), key=key, dur=8) for start, key in zip(notes, keys)]

        print(self)


CMajorModalScales()
