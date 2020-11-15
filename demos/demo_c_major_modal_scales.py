from piece import Piece
from tones import letter
from points import scale
from util import join


class CMajorModalScales(Piece):

    def details(self):
        self.title = "C Major Modal Scales"

    def write_score(self):
        # The looped section programmatically builds a series of scales
        # Note that the bass clef is just a tansposition of the treble clef
        looped = {"treble": []}
        for start in self.scale('c`', 'c``'):
            looped["treble"] += self.scale(start, 8, 8)
        looped["bass"] = self.transpose(looped["treble"], -1, 'octave')

        # The smart section programmatically builds a series of scales in different keys
        # Note how we use list comprehension to avoid a for loop, and use step = 2 to play every other note in the treble clef
        start_notes = self.scale('c```', 'c``')
        smart = {
            "treble": [scale(start, -8, key=letter(start) + " major", dur=8, step=2) for start in start_notes],
            "bass": [scale(self.transpose(start, -1, 'octave'), -8, key=letter(start) + " major", dur=8) for start in start_notes]
        }

        self.score = join(looped, smart)


if __name__ == "__main__":
    CMajorModalScales()
