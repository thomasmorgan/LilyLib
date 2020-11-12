from piece import Piece
from points import note, notes, arpeggio


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
        arpeggios = {
            "treble": arpeggio('e`', 'e``', 'E Major', 8),
            "bass": arpeggio('e', 4, 'E major', 8)
        }

        # The length section uses the arpeggio function to build an arpeggio, but specifies a length, rather than a stop note
        length = {
            "treble": arpeggio('f`', 4, 'F Major', 8),
            "bass": arpeggio('f', 4, 'F Major', 8)
        }

        starts = self.arpeggio('c`', 'c``')
        stepped = {
            'treble': [[self.arpeggio(start, self.transpose(start, 7), 16, step=step) for step in [3, 3, 1]] for start in starts],
            'bass': [[self.arpeggio(self.transpose(start, -7), start, 16, step=step) for step in [1, 3, 3]] for start in starts]
        }

        for staff in ["treble", "bass"]:
            self.score[staff] = [basic[staff], intermediate[staff], arpeggios[staff], length[staff], stepped[staff]]


if __name__ == "__main__":
    Arpeggios()
