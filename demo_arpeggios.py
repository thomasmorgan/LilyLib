from models import Note
from piece import Piece
from keys import EMajor, FMajor


class Arpeggios(Piece):

    def details(self):
        self.title = "Arpeggios"

    def write_score(self):
        # The basic section manually builds a scale note by note
        basic = {
            "treble": [Note("c`", 8), Note("e`", 8), Note("g`", 8), Note("c``", 8)],
            "bass": [Note("c", 8), Note("e", 8), Note("g", 8), Note("c`", 8)]
        }

        # The notes section uses the notes function to build a list of notes from a single string
        notes = {
            "treble": self.notes('d` fs` a` d``', dur=8),
            "bass": self.notes('d fs a d`', dur=8)
        }

        # The arpeggio section uses the arpeggio function to build a scale from one note to the next
        arpeggio = {
            "treble": self.arpeggio('e`', 'e``', key=EMajor, dur=8),
            "bass": self.arpeggio('e', 'e`', key=EMajor, dur=8)
        }

        # The length section uses the arpeggio function to build an arpeggio, but specifies a length, rather than a stop note
        length = {
            "treble": self.arpeggio('f`', 4, key=FMajor, dur=8),
            "bass": self.arpeggio('f', 4, key=FMajor, dur=8)
        }

        starts = self.arpeggio('c`', 'c``')
        stepped = {
            'treble': [[self.arpeggio(start, self.transpose(start, 1), step=step, dur=16) for step in [3, 3, 1]] for start in starts],
            'bass': [[self.arpeggio(self.transpose(start, -1), start, step=step, dur=16) for step in [1, 3, 3]] for start in starts]
        }

        for staff in ["treble", "bass"]:
            self.score[staff] = [basic[staff], notes[staff], arpeggio[staff], length[staff], stepped[staff]]


Arpeggios()
