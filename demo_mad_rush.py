from piece import Piece
from util import flatten, pattern, subset


class MadRush(Piece):

    def details(self):
        self.title = "Mad Rush"
        self.composer = "Philip Glass"
        self.tempo = "4/4"
        self.key = "F Major"

    def write_score(self):

        def triplet_bar(note_pair, bars=1):
            return self.triplets(self.notes(note_pair, 8) * int(6 * bars))

        def doublet_bar(note_pair, bars=1):
            return self.notes(note_pair, 8) * int(4 * bars)

        def arpeggio1(arp, bars=1, tempo=True):
            notes = pattern(arp, 1, 2, 3, 4, 3, 2, 1) * int(4 * bars)
            if tempo:
                notes = self.tempo_change("12/8") + notes
            return notes

        def arpeggio2(arp):
            return arpeggio1(arp, tempo=False) + self.tempo_change("14/8") + pattern(arp, 1, 2, 3, 4, 3, 4, 3, 2, 1, 2, 3, 4, 3, 2) * 2

        home_chord = self.arpeggio(self.key.root, 6)
        minor_third = self.arpeggio(self.transpose(self.key.root, -1, mode="scale"), 6, key=self.iii)

        sections = {}

        sections['A1'] = {}
        chord1 = subset(home_chord, 1, 3)
        chord2 = [self.iii.mediant + ','] + self.arpeggio(self.transpose(self.key.root, -1, mode="scale"), 3, key=self.iii)
        sections['A1'] = {
            'treble': self.rests(1) * 4,
            'bass1': doublet_bar(chord1[-2:], bars=2) + self.notes([chord2[1], chord2[3]], 8) + doublet_bar(chord2[2:], 1.75),
            'bass2': self.notes([chord1[0]] * 2 + [chord2[0]] * 2, 1, "~ ")
        }

        sections['A2'] = {}
        chord1 = home_chord
        chord2 = minor_third
        sections['A2'] = {
            'treble': triplet_bar(pattern(chord1, 6, 5), bars=2) + triplet_bar(pattern(chord2, 6, 4), bars=2),
            'bass1': doublet_bar(chord1[1:3], bars=2) + doublet_bar(chord2[1:3], bars=2),
            'bass2': self.notes([chord1[0]] * 2 + [chord2[0]] * 2, 1, "~ ")
        }

        sections['A3'] = {}
        chord1 = home_chord
        chord1b = self.arpeggio7(self.iii.subtonic, 7, key=self.iii)
        chord2 = minor_third
        sections['A3'] = {
            'treble': triplet_bar(chord1[-2:], bars=1) + triplet_bar([chord1b[-3], chord1b[-1]], bars=0.5) + triplet_bar(chord1[-2:], bars=0.5) + triplet_bar([chord2[3], chord2[5]], bars=2),
            'bass1': doublet_bar(chord1[1:3], bars=1) + doublet_bar(chord1b[1:3], bars=0.5) + doublet_bar(chord1[1:3], bars=0.5) + doublet_bar(chord2[1:3], bars=2),
            'bass2': self.notes(chord1[0], 1) + self.notes([chord1b[0], chord1b[0], chord1[0], chord1[0]], 4) + self.notes([chord2[0]] * 2, 1, "~ ")
        }

        #     'A3': {
        #         'treble': self.repeat(triplet_bar("c`` a`") + triplet_bar('c`` g`', 0.5) + triplet_bar("c`` a`", 0.5) + triplet_bar('c`` e`', 2)),
        #         'bass1': doublet_bar("a c`", 4),
        #         'bass2': self.notes('f', 1) + self.notes('g g f f', 4) + self.notes('e e', 1, "~ ")
        #     },
        #     'A4': {
        #         'treble': self.repeat(triplet_bar("bf` g`") + triplet_bar('d`` g`') + triplet_bar('c`` a`', 2)),
        #         'bass1': doublet_bar('bf d`', 2) + doublet_bar('a c`', 2),
        #         'bass2': self.notes("g g f f", 1, "~ ")
        #     },
        #     'A5': {
        #         'treble': triplet_bar("bf` g`") + triplet_bar('d`` g`') + triplet_bar('c`` a`', 2),
        #         'bass1': doublet_bar('bf d`', 2) + doublet_bar('a c`', 2),
        #         'bass2': self.notes('g', 1) + self.notes('f f g g', 4) + self.notes('f f', 1, "~ ")
        #     },
        #     'B1': {
        #         'treble': self.repeat(arp1(self.arpeggio7('a`', 'f``', dur=16), 2) + arp2(self.arpeggio('a`', 'a``', key=AMinor, dur=16))),
        #         'bass': arp1(self.arpeggio('f', 'f,', dur=16), 2) + arp2(self.arpeggio('e', 'e,', key=AMinor, dur=16))
        #     }
        # }

        # sections.update({
        #     'B2': copy_section('B1')
        # })
        # sections['B2']['treble'] = self.repeat(sections['B2']['treble'][1:-1], 3)
        # sections['B2']['treble'][26].tone.letter = 'g'
        # sections['B2']['treble'][32].tone.letter = 'g'
        # sections['B2']['bass'][24].tone.letter = 'g'
        # sections['B2']['bass'][30].tone.letter = 'g'

        # sections.update({
        #     'B3': {
        #         'treble': self.repeat(arp1(self.arpeggio7('g`', 'f``', key=GMinor, dur=16), 2) + arp2(self.arpeggio7('a`', 'f``'))),
        #         'bass': arp1(self.arpeggio('g', 'g,', key=GMinor, dur=16), 2) + arp2(self.arpeggio('f', 'f,', dur=16))
        #     }
        # })

        for section in sections:
            self.name(sections[section]['treble'], section)

        A = ['A1']

        structure = [A]

        self.score["treble"] = []
        self.score["bass"] = []
        for section in flatten(structure):
            self.score["treble"] += sections[section]['treble']
            if 'A' in section:
                self.score['bass'] += self.voices(sections[section]['bass1'], sections[section]['bass2'])
            else:
                self.score['bass'] += sections[section]['bass']

    def end_score(self):
        return ('>>\n  \\layout {\n \\context {\n \\Score\n \\override SpacingSpanner.common-shortest-duration =\n #(ly:make-moment 1/7)\n }\n }\n }')


if __name__ == "__main__":
    MadRush()
