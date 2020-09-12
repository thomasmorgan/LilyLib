from piece import Piece
from util import flatten, pattern


class MadRush(Piece):

    def details(self):
        self.title = "Mad Rush"
        self.composer = "Philip Glass"
        self.key = "F Major"

    def write_score(self):

        root_chord = self.arpeggio(self.key.root, 6)
        iii_chord = [self.transpose(t, -1, "scale") if t.letter == self.key.root else t for t in root_chord]
        iii7_chord = [self.transpose(t, 1, "scale") if t.letter == self.key.root else t for t in root_chord]

        def triplet_bar(note_pair, bars=1):
            return self.triplets(self.notes(note_pair, 8) * int(6 * bars))

        def doublet_bar(note_pair, bars=1):
            return self.notes(note_pair, 8) * int(4 * bars)

        def arpeggio1(arp, bars=1, tempo=True):
            notes = pattern(arp, 1, 2, 3, 4, 3, 2) * int(4 * bars)
            if tempo:
                notes = self.tempo_change("12/8") + notes
            return notes

        def arpeggio2(arp):
            return arpeggio1(arp, tempo=False) + self.tempo_change("14/8") + pattern(arp, 1, 2, 3, 4, 3, 4, 3, 2, 1, 2, 3, 4, 3, 2) * 2

        def A_motif(chord, bars, *tweaks):
            if chord == "root":
                motif = {
                    'treble': triplet_bar(pattern(root_chord, 6, 5), bars=bars),
                    'bass1': doublet_bar(pattern(root_chord, 2, 3), bars=bars),
                    'bass2': self.notes(pattern(root_chord, 1, 1), 1, "~ ") * int(bars / 2)
                }
            elif chord == "iii":
                motif = {
                    'treble': triplet_bar(pattern(iii_chord, 6, 4), bars=bars),
                    'bass1': doublet_bar(pattern(iii_chord, 2, 3), bars=bars),
                    'bass2': self.notes(pattern(iii_chord, 1, 1), 1, "~ ") * int(bars / 2)
                }
                if 'low first' in tweaks:
                    motif['bass1'][0] = iii_chord[0]
                    motif['bass2'] = self.transpose(motif['bass2'], -9, "scale")
            elif chord == "iii7":
                motif = {
                    'treble': triplet_bar(pattern(iii7_chord, 6, 4), bars=bars),
                    'bass1': doublet_bar(pattern(iii7_chord, 2, 3), bars=bars)
                }

            if 'no treble' in tweaks:
                motif['treble'] = self.rests(1) * bars

            return motif

        def merge(*motifs):
            combined = {
                'treble': [],
                'bass1': [],
                'bass2': []
            }
            for motif in motifs:
                combined['treble'] += motif['treble']
                combined['bass1'] += motif['bass1']
                combined['bass2'] += motif['bass2']
            return combined

        sections = {}

        sections['A1'] = merge(A_motif('root', 2, 'no treble'), A_motif('iii', 2, 'no treble', 'low first'))

        sections['A2'] = merge(A_motif('root', 2), A_motif('iii', 2))

        # sections['A3'] = merge(A_motif('root', 1), A_motif('iii7', 0.5), A_motif('root', 0.5), A_motif('iii', 2))
        # sections['A3']['bass2'] = self.notes(pattern(root_chord, 1), 1) + self.notes(pattern(iii7_chord, 1, 1) + pattern(root_chord, 1, 1), 4) + self.notes(pattern(iii_chord, 1, 1), 1, "~ ")

        # sections['A3'] = {}
        # sections['A3'] = {
        #     'treble': triplet_bar(pattern(root_chord, 6, 5), bars=1) + triplet_bar(pattern(iii7_chord, 7, 5), bars=0.5) + triplet_bar(pattern(root_chord, 6, 5), bars=0.5) + triplet_bar(pattern(iii_chord, 6, 4), bars=2),
        #     'bass1': doublet_bar(pattern(root_chord, 2, 3), bars=1) + doublet_bar(pattern(iii7_chord, 2, 3), bars=0.5) + doublet_bar(pattern(root_chord, 2, 3), bars=0.5) + doublet_bar(pattern(iii_chord, 2, 3), bars=2),
        #     'bass2': self.notes(pattern(root_chord, 1), 1) + self.notes(pattern(iii7_chord, 1, 1) + pattern(root_chord, 1, 1), 4) + self.notes(pattern(iii_chord, 1) * 2, 1, "~ ")
        # }

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

        A = ['A1', 'A2']

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
