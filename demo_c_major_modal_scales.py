from piece import Piece
from keys import CMajor, DMajor, EMajor, FMajor, GMajor, AMajor, BMajor


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
        # Note the start values are just strings, and so they can be modified by adding or removing `
        # Note also that the score ends up being a list-of-lists-of-notes, but nested lists are fine
        looped = {"treble": []}
        for start in ['f`', 'g`', 'a`', 'b`', 'c``']:
            looped["treble"] += self.scale(start, 8, 8)
        looped["bass"] = self.transpose(looped["treble"], -1)

        # The smart section programmatically builds a series of scales in different keys
        # Note the use of key.scale to build a series of tones to start each scale but that self.scale it used to actually build the scales.
        # This is because key.scale returns a scale of durationless tones, while self.scale returns a scale of proper Notes
        # Note also the use of Piece.transpose() to change the pitches of the Tones that define the limits of the scale
        # Finally, note how we use zip and list comprehension to avoid the need for a for loop, and use * 2 to double the scales in the treble clef
        keys = [CMajor, BMajor, AMajor, GMajor, FMajor, EMajor, DMajor, CMajor]
        start_notes = self.scale('c```', 'c``', 8)
        smart = {
            "treble": [self.scale(start, -8, 16, key=key) * 2 for start, key in zip(start_notes, keys)],
            "bass": [self.scale(self.transpose(start, -1), -8, 8, key=key) for start, key in zip(start_notes, keys)]
        }

        for staff in ["treble", "bass"]:
            self.score[staff] = [basic[staff], notes[staff], scale[staff], looped[staff], smart[staff]]


CMajorModalScales()
