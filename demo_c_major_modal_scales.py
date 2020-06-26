from piece import Piece
from models import Note
from keys import CMajor, DMajor, EMajor, FMajor, GMajor, AMajor, BMajor


class CMajorModalScales(Piece):

    def details(self):
        self.title = "C Major Modal Scales"

    def write_score(self):
        # The basic section manually builds a scale note by note
        basic = {
            "treble": [Note("c`", 8), Note("d`", 8), Note("e`", 8), Note("f`", 8), Note("g`", 8), Note("a`", 8), Note("b`", 8), Note("c``", 8)],
            "bass": [Note("c", 8), Note("d", 8), Note("e", 8), Note("f", 8), Note("g", 8), Note("a", 8), Note("b", 8), Note("c`", 8)]
        }

        # The notes section uses the notes function to build a list of notes from a single string
        notes = {
            "treble": self.notes('d` e` f` g` a` b` c`` d``', dur=8),
            "bass": self.notes('d e f g a b c` d`', dur=8)
        }

        # The scale section uses the scale function to build a scale from one note to the next
        scale = {
            "treble": self.scale('e`', 'e``', dur=8),
            "bass": self.scale('e', 'e`', dur=8)
        }

        # The looped section programmatically builds a series of scales
        # Note the start values are just strings, and so they can be modified by adding or removing `
        # Note also that the score ends up being a list-of-lists-of-notes, but nested lists are fine
        looped = {
            "treble": [],
            "bass": []
        }
        for start in ['f`', 'g`', 'a`', 'b`', 'c``']:
            looped["treble"] += self.scale(start, start + '`', dur=8)
            looped["bass"] += self.scale(start[:-1], start, dur=8)

        # The smart section programmatically builds a series of scales in different keys
        # Note the use of key.scale to build a series of tones to start each scale but that self.scale it used to actually build the scales.
        # This is because key.scale returns a scale of durationless tones, while self.scale returns a scale of proper Notes
        # Note also the use of Piece.transpose() to change the pitches of the Tones that define the limits of the scale
        # Finally, note how we use zip and list comprehension to avoid the need for a for loop, and use * 2 to double the scales in the treble clef
        keys = [CMajor, BMajor, AMajor, GMajor, FMajor, EMajor, DMajor, CMajor]
        tones = self.scale('c```', 'c``')
        smart = {
            "treble": [self.scale(start, self.transpose(start, -1), key=key, dur=16) * 2 for start, key in zip(tones, keys)],
            "bass": [self.scale(self.transpose(start, -1), self.transpose(start, -2), key=key, dur=8) for start, key in zip(tones, keys)]
        }

        for staff in ["treble", "bass"]:
            self.score[staff] = [basic[staff], notes[staff], scale[staff], looped[staff], smart[staff]]


CMajorModalScales()
