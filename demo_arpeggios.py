from piece import Piece


class Arpeggios(Piece):

    def details(self):
        self.title = "Arpeggios"

    def write_score(self):
        # The basic section manually builds a scale note by note
        basic = {
            "treble": [self.notes("c`", 8), self.notes("e`", 8), self.notes("g`", 8), self.notes("c``", 8)],
            "bass": [self.notes("c", 8), self.notes("e", 8), self.notes("g", 8), self.notes("c`", 8)]
        }

        # The notes section uses the notes function to build a list of notes from a single string
        notes = {
            "treble": self.notes('d` fs` a` d``', 8),
            "bass": self.notes('d fs a d`', 8)
        }

        # The arpeggio section uses the arpeggio function to build a scale from one note to the next
        arpeggio = {
            "treble": self.arpeggio('e`', 'e``', 8, key="E Major"),
            "bass": self.arpeggio('e', 4, 8, key="E Major")
        }

        # The length section uses the arpeggio function to build an arpeggio, but specifies a length, rather than a stop note
        length = {
            "treble": self.arpeggio('f`', 4, 8, key="F Major"),
            "bass": self.arpeggio('f', 4, 8, key="F Major")
        }

        starts = self.arpeggio('c`', 'c``')
        stepped = {
            'treble': [[self.arpeggio(start, self.transpose(start, 1), 16, step=step) for step in [3, 3, 1]] for start in starts],
            'bass': [[self.arpeggio(self.transpose(start, -1), start, 16, step=step) for step in [1, 3, 3]] for start in starts]
        }

        for staff in ["treble", "bass"]:
            self.score[staff] = [basic[staff], notes[staff], arpeggio[staff], length[staff], stepped[staff]]


Arpeggios()
