from models import Note
from piece import Piece
from keys import EMajor, FMajor


class Arpeggios(Piece):

    def write_score(self):
        self.title = "Arpeggios"

        self.create_sections("basic", "notes", "arpeggio", "length", 'stepped')

        # The basic section manually builds a scale note by note
        self.score["treble"]["basic"] = [Note("c`", 8), Note("e`", 8), Note("g`", 8), Note("c``", 8)]
        self.score["bass"]["basic"] = [Note("c", 8), Note("e", 8), Note("g", 8), Note("c`", 8)]

        # The notes section uses the notes function to build a list of notes from a single string
        self.score["treble"]["notes"] = self.notes('d` fs` a` d``', dur=8)
        self.score["bass"]["notes"] = self.notes('d fs a d`', dur=8)

        # The arpeggio section uses the arpeggio function to build a scale from one note to the next
        self.score["treble"]["arpeggio"] = self.arpeggio('e`', 'e``', key=EMajor, dur=8)
        self.score["bass"]["arpeggio"] = self.arpeggio('e', 'e`', key=EMajor, dur=8)

        # The length section uses the arpeggio function to build an arpeggio, but specifies a length, rather than a stop note
        self.score["treble"]["length"] = self.arpeggio('f`', length=4, key=FMajor, dur=8)
        self.score["bass"]["length"] = self.arpeggio('f', length=4, key=FMajor, dur=8)

        starts = self.key.arpeggio('c`', 'c``')
        self.score['treble']['stepped'] = [[self.arpeggio(start, start.shift(1), step=step, dur=16) for step in [3, 3, 1]] for start in starts]
        self.score['bass']['stepped'] = [[self.arpeggio(start.shift(-1), start, step=step, dur=16) for step in [1, 3, 3]] for start in starts]
