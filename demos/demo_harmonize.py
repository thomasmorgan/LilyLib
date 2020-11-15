from piece import Piece


class Harmonize(Piece):

    def details(self):
        self.title = "Harmonized notes"

    def write_score(self):

        rh_melody = self.arpeggio('c`', 4, 4)
        lh_melody = self.transpose(rh_melody, -1, 'octave')

        self.score = {
            'treble': self.harmonize(rh_melody, 3),
            'bass': self.harmonize(lh_melody, -1, 'octave')
        }


if __name__ == "__main__":
    Harmonize()
