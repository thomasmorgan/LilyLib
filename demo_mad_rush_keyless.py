from piece import Piece
from util import flatten, pattern, subset, select, merge


class MadRushKeyless(Piece):

    def details(self):
        self.title = "Mad Rush"
        self.composer = "Philip Glass"
        self.key = "F Major"
        self.summary = True

    def subtext(self):
        if self.summary:
            return"""
                \\markup {
                    \\column {
                        \\line {\\bold {Overall:} \\bold{A}, \\bold{A}, A1, \\bold{B}, A1, \\bold{C}, A1, \\bold{C}, A1, \\bold{B}, \\bold{A}, \\bold{A}, A1, \\bold{B}, A1, \\bold{D}, \\bold{D}, A1}
                        \\line { - }
                        \\line {\\bold {Section A:} A1, A2, A2, A3, A3, A4, A4, A5}
                        \\line {\\bold {Section B:} B1, B1, B2, B2, B2, B3, B3, B4}
                        \\line {\\bold {Section C:} C1, C1, C2, C2, C3, C3, C4}
                        \\line {\\bold {Section D:} D1, D1, D2, D2, D3, D3, D4}
                        \\line { - }
                    }
                }"""
        else:
            return ""

    def write_score(self):
        sections = {}

        aI = self.arpeggio(self.key.root, 6)
        aiii = [self.transpose(t, -1, "scale") if t.letter == self.key.root else t for t in aI]
        aiii7 = [self.transpose(t, 1, "scale") if t.letter == self.key.root else t for t in aI]
        aii = self.transpose(aI, 1, "scale")
        aii7 = self.transpose(select(aii, 1), -1, "scale") + subset(aii, 2, 6)

        def triplet_bar(note_pair, bars=1):
            return self.triplets(self.notes(note_pair, 8) * int(6 * bars))

        def doublet_bar(note_pair, bars=1):
            return self.notes(note_pair, 8) * int(4 * bars)

        def A_motif(chord, bars, *tweaks):
            motif = {}

            if chord == aI:
                motif['treble'] = triplet_bar(pattern(chord, [6, 5]), bars=bars)
            elif chord == aii and 'low triplets' in tweaks:
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

        sections['A1'] = merge(A_motif(aI, 2, 'no treble'), A_motif(aiii, 2, 'no treble', 'low first'))
        sections['A1']['treble'] = self.tempo_change('4/4') + sections['A1']['treble']
        sections['A2'] = merge(A_motif(aI, 2), A_motif(aiii, 2))
        sections['A3'] = merge(A_motif(aI, 1), A_motif(aiii7, 0.5, 'crotchet bass'), A_motif(aI, 0.5, 'crotchet bass'), A_motif(aiii, 2))
        sections['A4'] = merge(A_motif(aii, 1, 'low triplets', 'extend tie'), A_motif(aii, 1), A_motif(aI, 2))
        sections['A5'] = merge(A_motif(aii, 1, 'low triplets'), A_motif(aii7, 0.5, 'crotchet bass'), A_motif(aii, 0.5, 'crotchet bass'), A_motif(aI, 2))

        A = ['A1', 'A2', 'A2', 'A3', 'A3', 'A4', 'A4', 'A5']

        bI7 = self.arpeggio(self.transpose(self.key.root, -1), 4) + self.arpeggio7(self.transpose(self.key.root, 9, 'scale'), 4)
        biii = self.arpeggio(self.transpose(self.key.root, -8, 'scale'), 4, key=self.IIIt)
        biii += self.arpeggio(self.transpose(self.key.root, 9, 'scale'), 4, key=self.IIIt)
        biii7 = [self.transpose(t, i, 'scale') for t, i in zip(bI7, [1, 0, 0, 1, -1, 0, 0, 0])]
        bii7 = self.transpose(subset(bI7, 1, 4), 1, 'scale') + self.transpose(subset(bI7, 5, 7), -1, 'scale') + select(bI7, 8)
        bii7d5 = [self.transpose(t, i, 'semitone') for t, i in zip(bii7, [0, 0, -1, 0, 0, 0, -1, 0])]

        def arpeggio_bar(arp, bars):
            return self.notes(pattern(arp, [1, 2, 3, 4, 3, 2]), 16) * int(4 * bars)

        def altpeggio_bar(arp, bars):
            return self.tempo_change("14/8") + pattern(arp, [1, 2, 3, 4, 3, 4, 3, 2, 1, 2, 3, 4, 3, 2]) * 2

        def B_motif(chord, bars, *tweaks):
            motif = {}

            if 'alt' not in tweaks:
                motif['treble'] = arpeggio_bar(subset(chord, 5, 8), bars=bars)
                motif['bass'] = arpeggio_bar(subset(chord, 4, 1), bars=bars)
            else:
                motif['treble'] = altpeggio_bar(subset(chord, 5, 8), bars=bars)
                motif['bass'] = altpeggio_bar(subset(chord, 4, 1), bars=bars)

            if 'tempo' in tweaks:
                motif['treble'] = self.tempo_change("12/8") + motif['treble']

            return motif

        sections['B1'] = merge(B_motif(bI7, 2, 'tempo'), B_motif(biii, 1), B_motif(biii, 1, 'alt'))
        sections['B2'] = merge(B_motif(bI7, 1, 'tempo'), B_motif(biii7, 0.5), B_motif(bI7, 0.5), B_motif(biii, 1), B_motif(biii, 1, 'alt'))
        sections['B3'] = merge(B_motif(bii7, 2, 'tempo'), B_motif(bI7, 1), B_motif(bI7, 1, 'alt'))
        sections['B4'] = merge(B_motif(bii7, 1, 'tempo'), B_motif(bii7d5, 1), B_motif(bI7, 1), B_motif(bI7, 1, 'alt'))

        B = ['B1', 'B1', 'B2', 'B2', 'B2', 'B3', 'B3', 'B4']

        def combine(lh, rh):
            return {
                'treble': self.triplets(subset(sections[rh]['treble'], 2, 7) * 8 + subset(sections[rh]['treble'], 56, 61) * 8),
                'bass1': sections[lh]['bass1'],
                'bass2': sections[lh]['bass2'],
            }

        sections['C1'] = combine('A2', 'B1')
        sections['C1']['treble'] = self.tempo_change('4/4') + sections['C1']['treble']
        sections['C2'] = combine('A3', 'B2')
        sections['C3'] = combine('A4', 'B3')
        sections['C4'] = combine('A5', 'B4')

        C = ['C1', 'C1', 'C2', 'C2', 'C3', 'C3', 'C4']

        def D_motif(chord, section):
            motif = {}
            motif['bass1'] = sections[section]['bass1']
            motif['bass2'] = sections[section]['bass2']
            if len(chord) == 3:
                motif['treble'] = self.harmonize(self.notes(pattern(chord, [1, 1, 2, 3, 3]), [1, 2, 2, 1, 1], '~   ~ '), 1)
            else:
                motif['treble'] = self.harmonize(self.notes(pattern(chord, [1, 1, 2, 2]), 1, '~ '), 1)
            return motif

        diii = self.transpose(self.transpose(self.arpeggio(self.key.root, 3), 2, "scale"), 1)
        dI = [self.transpose(self.key.root, 2)]
        dii = self.transpose([self.key.root, self.transpose(self.IIt.v, -1, "semitone")], 2) + [self.transpose(self.key.v, 2)]

        sections['D1'] = D_motif(diii, 'A2')
        sections['D2'] = D_motif(diii, 'A3')
        sections['D3'] = D_motif(dI * 2, 'A4')
        sections['D4'] = D_motif(dii, 'A5')

        D = ['D1', 'D1', 'D2', 'D2', 'D3', 'D3', 'D4']

        for section in sections:
            self.name(sections[section]['treble'], section)

        structure = [A, A, 'A1', B, 'A1', C, 'A1', C, 'A1', B, A, A, 'A1', B, 'A1', D, D, 'A1']

        self.score["treble"] = []
        self.score["bass"] = []

        if self.summary:
            sections_to_print = sections
        else:
            sections_to_print = flatten(structure)

        for section in sections_to_print:
            self.score["treble"] += sections[section]['treble'] + ["\\break\n"]
            if 'B' not in section:
                self.score['bass'] += self.voices(sections[section]['bass1'], sections[section]['bass2'])
            else:
                self.score['bass'] += sections[section]['bass']

    def end_score(self):
        return ('>>\n  \\layout {\n \\context {\n \\Score\n \\override SpacingSpanner.common-shortest-duration =\n #(ly:make-moment 1/8)\n }\n }\n }')


if __name__ == "__main__":
    MadRushKeyless()
