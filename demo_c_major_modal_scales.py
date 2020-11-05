from piece import Piece
from util import letter


class CMajorModalScales(Piece):

    def details(self):
        self.title = "C Major Modal Scales"

    def write_score(self):
        # The basic section manually builds a scale note by note
        basic = {
            "treble": [self.notes("c`", 8), self.notes("d`", 8), self.notes("e`", 8), self.notes("f`", 8), self.notes("g`", 8), self.notes("a`", 8), self.notes("b`", 8), self.notes("c``", 8)],
            "bass": [self.notes("c", 8), self.notes("d", 8), self.notes("e", 8), self.notes("f", 8), self.notes("g", 8), self.notes("a", 8), self.notes("b", 8), self.notes("c`", 8)]
        }

        # The notes section uses the notes function to build a list of notes from a single string
        notes = {
            "treble": self.notes('d` e` f` g` a` b` c`` d``', 8),
            "bass": self.notes('d e f g a b c` d`', 8)
        }

        # The scale section uses the scale function to build a scale from A to B, or from A with length B
        scale = {
            "treble": self.scale('e`', 'e``', 8),
            "bass": self.scale('e', 8, 8)
        }

        # The looped section programmatically builds a series of scales
        # Note that the bass clef is just a tansposition of the treble clef
        looped = {"treble": []}
        for start in self.scale('f`', 'c``', 8):
            looped["treble"] += self.scale(start, 8, 8)
        looped["bass"] = self.transpose(looped["treble"], -1)

        # The smart section programmatically builds a series of scales in different keys
        # Note how we use list comprehension to avoid a for loop, and use step = 2 to play every other note in the treble clef
        start_notes = self.scale('c```', 'c``')
        smart = {
            "treble": [self.scale(start, -8, 8, step=2, key=letter(start) + " major") for start in start_notes],
            "bass": [self.scale(self.transpose(start, -1), -8, 8, key=letter(start) + " major") for start in start_notes]
        }

        for staff in ["treble", "bass"]:
            self.score[staff] = [basic[staff], notes[staff], scale[staff], looped[staff], smart[staff]]


if __name__ == "__main__":
    CMajorModalScales()
