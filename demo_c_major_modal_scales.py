from piece import Piece
from models import Note
from keys import CMajor, DMajor, EMajor, FMajor, GMajor, AMajor, BMajor


class CMajorModalScales(Piece):

    def details(self):
        self.title = "C Major Modal Scales"
        self.create_sections("basic", "notes", "scale", "looped", "super")

    def write_score(self):
        # The basic section manually builds a scale note by note
        self.score["treble"]["basic"] = [Note("c`", 8), Note("d`", 8), Note("e`", 8), Note("f`", 8), Note("g`", 8), Note("a`", 8), Note("b`", 8), Note("c``", 8)]
        self.score["bass"]["basic"] = [Note("c", 8), Note("d", 8), Note("e", 8), Note("f", 8), Note("g", 8), Note("a", 8), Note("b", 8), Note("c`", 8)]

        # The notes section uses the notes function to build a list of notes from a single string
        self.score["treble"]["notes"] = self.notes('d` e` f` g` a` b` c`` d``', dur=8)
        self.score["bass"]["notes"] = self.notes('d e f g a b c` d`', dur=8)

        # The scale section uses the scale function to build a scale from one note to the next
        self.score["treble"]["scale"] = self.scale('e`', 'e``', dur=8)
        self.score["bass"]["scale"] = self.scale('e', 'e`', dur=8)

        # The looped section programmatically builds a series of scales
        # Note the start values are just strings, and so they can be modified by adding or removing `
        # Note also that the score ends up being a list-of-lists-of-notes, but nested lists are fine
        # Finally note it uses key.scale to get a tone of scales, and then converts each tone to a Note
        self.score["treble"]["looped"] = []
        self.score["bass"]["looped"] = []
        for start in ['f`', 'g`', 'a`', 'b`', 'c``']:
            self.score["treble"]["looped"] += [Note(t, 8) for t in self.key.scale(start, start + '`')]
            self.score["bass"]["looped"] += [Note(t, 8) for t in self.key.scale(start[:-1], start)]

        # The super section programmatically builds a series of scales in different keys
        # Note the use of key.scale to build a series of tones to start each scale but that self.scale it used to actually build the scales.
        # This is because key.scale returns a scale of durationless tones, while self.scale returns a scale of proper Notes
        # Note also the use of Tone.shift to change the pitches of the Tones that define the limits of the scale
        # Finally, note how we use zip and list comprehension to avoid the need for a for loop, and use * 2 to double the scales in the treble clef
        keys = [CMajor, BMajor, AMajor, GMajor, FMajor, EMajor, DMajor, CMajor]
        tones = self.key.scale('c```', 'c``')
        self.score["treble"]["super"] = [self.scale(start, start.shift(-1), key=key, dur=16) * 2 for start, key in zip(tones, keys)]
        self.score["bass"]["super"] = [self.scale(start.shift(-1), start.shift(-2), key=key, dur=8) for start, key in zip(tones, keys)]


CMajorModalScales()
