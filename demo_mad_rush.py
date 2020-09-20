from piece import Piece
from util import flatten, pattern, subset, select, merge, duplicate


class MadRush(Piece):

    def details(self):
        self.title = "Mad Rush"
        self.composer = "Philip Glass"
        self.key = "F Major"

    def write_score(self):

        root = self.arpeggio(self.key.root, 6)
        iii = [self.transpose(t, -1, "scale") if t.letter == self.key.root else t for t in root]
        iii7 = [self.transpose(t, 1, "scale") if t.letter == self.key.root else t for t in root]
        ii = self.transpose(root, 1, "scale")
        ii7 = self.transpose(select(ii, 1), -1, "scale") + subset(ii, 2, 6)

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
            return arpeggio1(arp, tempo=False) + self.tempo_change("14/8") + pattern(arp, [1, 2, 3, 4, 3, 4, 3, 2, 1, 2, 3, 4, 3, 2]) * 2

        def A_motif(chord, bars, *tweaks):
            motif = {}

            if chord == root:
                motif['treble'] = triplet_bar(pattern(chord, [6, 5]), bars=bars)
            elif chord == ii and 'low triplets' in tweaks:
                motif['treble'] = triplet_bar(pattern(chord, [5, 4]), bars=bars)
            else:
                motif['treble'] = triplet_bar(pattern(chord, [6, 4]), bars=bars)

            motif['bass1'] = doublet_bar(pattern(chord, [2, 3]), bars=bars)

            if 'crotchet bass' in tweaks:
                motif['bass2'] = self.notes(select(chord, 1), 4) * int(bars * 4)
            else:
                motif['bass2'] = self.notes(select(chord, 1) * bars, 1, "~")
                if 'extend tie' not in tweaks:
                    motif['bass2'][-1].ornamentation = ""

            if 'low first' in tweaks:
                motif['bass1'][0] = chord[0]
                motif['bass2'] = self.transpose(motif['bass2'], -9, "scale")

            if 'no treble' in tweaks:
                motif['treble'] = self.rests(1) * bars

            return motif

        sections = {}

        sections['A1'] = merge(A_motif(root, 2, 'no treble'), A_motif(iii, 2, 'no treble', 'low first'))

        sections['A2'] = merge(A_motif(root, 2), A_motif(iii, 2))

        sections['A3'] = merge(A_motif(root, 1), A_motif(iii7, 0.5, 'crotchet bass'), A_motif(root, 0.5, 'crotchet bass'), A_motif(iii, 2))

        sections['A4'] = merge(A_motif(ii, 1, 'low triplets', 'extend tie'), A_motif(ii, 1), A_motif(root, 2))

        sections['A5'] = merge(A_motif(ii, 1, 'low triplets'), A_motif(ii7, 0.5, 'crotchet bass'), A_motif(ii, 0.5, 'crotchet bass'), A_motif(root, 2))

        for section in sections:
            self.name(sections[section]['treble'], section)

        A = ['A1', 'A2', 'A2', 'A3', 'A3', 'A4', 'A4', 'A5']

        structure = [A, A, 'A1']

        self.score["treble"] = []
        self.score["bass"] = []
        for section in flatten(structure):
            self.score["treble"] += sections[section]['treble']
            if 'A' in section:
                self.score['bass'] += self.voices(sections[section]['bass1'], sections[section]['bass2'])
            else:
                self.score['bass'] += sections[section]['bass']

    def end_score(self):
        return ('>>\n  \\layout {\n \\context {\n \\Score\n \\override SpacingSpanner.common-shortest-duration =\n #(ly:make-moment 1/8)\n }\n }\n }')


if __name__ == "__main__":
    MadRush()
