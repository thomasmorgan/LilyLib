from util import subset, select
from tones import letter
from points import arpeggio
from demos.demo_mad_rush import MadRush


class MadRushKeyless(MadRush):

    def details(self):
        super().details()
        self.key = "F Major"

    def create_chords(self):

        self.aI = self.arpeggio(self.key.root, 6)
        self.aiii = [self.transpose(t, -1) if letter(t) == self.key.root else t for t in self.aI]
        self.aiii7 = [self.transpose(t, 1) if letter(t) == self.key.root else t for t in self.aI]
        self.aii = self.transpose(self.aI, 1)
        self.aii7 = self.transpose(select(self.aii, 1), -1) + subset(self.aii, 2, 6)

        self.bI7 = self.arpeggio(self.transpose(self.key.root, -1, 'octave'), 4) + self.arpeggio7(self.transpose(self.key.root, 9), 4)
        self.biii = arpeggio(self.transpose(self.key.root, -8), 4, key=self.IIIt)
        self.biii += arpeggio(self.transpose(self.key.root, 9), 4, key=self.IIIt)
        self.biii7 = [self.transpose(t, i) for t, i in zip(self.bI7, [1, 0, 0, 1, -1, 0, 0, 0])]
        self.bii7 = self.transpose(subset(self.bI7, 1, 4), 1) + self.transpose(subset(self.bI7, 5, 7), -1) + select(self.bI7, 8)
        self.bii7d5 = [self.transpose(t, i, 'semitone') for t, i in zip(self.bii7, [0, 0, -1, 0, 0, 0, -1, 0])]

        self.diii = self.transpose(self.transpose(self.arpeggio(self.key.root, 3), 2), 1, 'octave')
        self.dI = [self.transpose(self.key.root, 2, 'octave')]
        self.dii = self.transpose([self.key.root, self.transpose(self.IIt.v, -1, "semitone")], 2, 'octave') + [self.transpose(self.key.v, 2, 'octave')]


if __name__ == "__main__":
    MadRushKeyless()
