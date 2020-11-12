from piece import Piece
from lilylib import note, notes


class Arpeggios(Piece):

    def details(self):
        self.title = "Arpeggios"

    def write_score(self):
        # The basic section manually builds a scale note by note
        basic = {
            "treble": [note("c`", 8), note("e`", 8), note("g`", 8), note("c``", 8)],
            "bass": [note("c", 8), note("e", 8), note("g", 8), note("c`", 8)]
        }

        # The notes section uses the notes function to build a list of notes from a single string
        intermediate = {
            "treble": notes('d` fs` a` d``', 8),
            "bass": notes('d fs a d`', 8)
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
            'treble': [[self.arpeggio(start, self.transpose(start, 7), 16, step=step) for step in [3, 3, 1]] for start in starts],
            'bass': [[self.arpeggio(self.transpose(start, -7), start, 16, step=step) for step in [1, 3, 3]] for start in starts]
        }

        for staff in ["treble", "bass"]:
            self.score[staff] = [basic[staff], intermediate[staff], arpeggio[staff], length[staff], stepped[staff]]


if __name__ == "__main__":
    Arpeggios()
