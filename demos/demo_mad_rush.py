from piece import Piece
from util import flatten, pattern, subset, select, join
from points import note, notes, rest, arpeggio, arpeggio7
from markup import triplets, tempo_change, name, voices


class MadRush(Piece):

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
                        \\line { - }
                        \\line {\\bold {Overall:} \\bold{AA B CC B AA B DD}}
                        \\line { - }
                        \\line {Insert A0 between all elements, and at start and end of piece.}
                        \\line { - }
                        \\line { - }
                        \\line { - }
                        \\line {\\bold {Section A:} A1, A1, A2, A2, A2, A3, A3, A4}
                        \\line {\\bold {Section B:} B1, B1, B2, B2, B2, B3, B3, B4}
                        \\line {\\bold {Section C:} C1, C1, C2, C2, C2, C3, C3, C4}
                        \\line {\\bold {Section D:} D1, D1, D2, D2, D2, D3, D3, D4}
                        \\line { - }
                        \\line { - }
                        \\line { - }
                    }
                }"""
        else:
            return ""

    def write_score(self):
        self.score["treble"] = []
        self.score["bass"] = []
        sections = {}

        aI = self.arpeggio('f', 6)
        aiii = arpeggio('e', 6, 'A Minor')
        aiii7 = pattern(arpeggio7('g', 7, 'A Minor'), 1, 2, 3, 5, 6, 7)
        aii = arpeggio('g', 6, 'G Minor')
        aii7 = ['f'] + subset(aii, 2, 6)

        def triplet_bar(note_pair, bars=1):
            return triplets(notes(note_pair, 8) * int(6 * bars))

        def doublet_bar(note_pair, bars=1):
            return notes(note_pair, 8) * int(4 * bars)

        def A_motif(chord, bars, *tweaks):
            motif = {}

            if chord == aI:
                motif['treble'] = triplet_bar(pattern(chord, [6, 5]), bars=bars)
            elif chord == aii and 'low triplets' in tweaks:
                motif['treble'] = triplet_bar(pattern(chord, [5, 4]), bars=bars)
            else:
                motif['treble'] = triplet_bar(pattern(chord, [6, 4]), bars=bars)

            motif['bass1'] = doublet_bar(pattern(chord, 2, 3), bars=bars)

            if 'crotchet bass' in tweaks:
                motif['bass2'] = note(select(chord, 1), 4) * int(bars * 4)
            else:
                motif['bass2'] = notes(select(chord, 1) * bars, 1, "~")
                if 'extend tie' not in tweaks:
                    motif['bass2'][-1].ornamentation = ""

            if 'low first' in tweaks:
                motif['bass1'][0] = chord[0]
                motif['bass2'] = self.transpose(motif['bass2'], -9, "scale")

            if 'no treble' in tweaks:
                motif['treble'] = rest(1) * bars

            return motif

        sections['A0'] = join(A_motif(aI, 2, 'no treble'), A_motif(aiii, 2, 'no treble', 'low first'))
        sections['A0']['treble'] = tempo_change('4/4') + sections['A0']['treble']
        sections['A1'] = join(A_motif(aI, 2), A_motif(aiii, 2))
        sections['A2'] = join(A_motif(aI, 1), A_motif(aiii7, 0.5, 'crotchet bass'), A_motif(aI, 0.5, 'crotchet bass'), A_motif(aiii, 2))
        sections['A3'] = join(A_motif(aii, 1, 'low triplets', 'extend tie'), A_motif(aii, 1), A_motif(aI, 2))
        sections['A4'] = join(A_motif(aii, 1, 'low triplets'), A_motif(aii7, 0.5, 'crotchet bass'), A_motif(aii, 0.5, 'crotchet bass'), A_motif(aI, 2))

        A = ['A1', 'A1', 'A2', 'A2', 'A2', 'A3', 'A3', 'A4']

        bI7 = self.arpeggio('f,', 4) + self.arpeggio7('a`', 4)
        biii = arpeggio('e,', 4, 'A Minor') + arpeggio('a`', 4, 'A minor')
        biii7 = [self.transpose(t, i) for t, i in zip(bI7, [1, 0, 0, 1, -1, 0, 0, 0])]
        bii7 = arpeggio('g,', 4, 'G Minor') + arpeggio('g`', 4, 'G Minor')
        bii7d5 = [self.transpose(t, i, 'semitone') for t, i in zip(bii7, [0, 0, -1, 0, 0, 0, -1, 0])]

        def arpeggio_bar(arp, bars):
            return notes(pattern(arp, 1, 2, 3, 4, 3, 2), 16) * int(4 * bars)

        def altpeggio_bar(arp, bars):
            return tempo_change("14/8") + pattern(arp, 1, 2, 3, 4, 3, 4, 3, 2, 1, 2, 3, 4, 3, 2) * 2

        def B_motif(chord, bars, *tweaks):
            motif = {}

            if 'alt' not in tweaks:
                motif['treble'] = arpeggio_bar(subset(chord, 5, 8), bars=bars)
                motif['bass'] = arpeggio_bar(subset(chord, 4, 1), bars=bars)
            else:
                motif['treble'] = altpeggio_bar(subset(chord, 5, 8), bars=bars)
                motif['bass'] = altpeggio_bar(subset(chord, 4, 1), bars=bars)

            if 'tempo' in tweaks:
                motif['treble'] = tempo_change("12/8") + motif['treble']

            return motif

        sections['B1'] = join(B_motif(bI7, 2, 'tempo'), B_motif(biii, 1), B_motif(biii, 1, 'alt'))
        sections['B2'] = join(B_motif(bI7, 1, 'tempo'), B_motif(biii7, 0.5), B_motif(bI7, 0.5), B_motif(biii, 1), B_motif(biii, 1, 'alt'))
        sections['B3'] = join(B_motif(bii7, 2, 'tempo'), B_motif(bI7, 1), B_motif(bI7, 1, 'alt'))
        sections['B4'] = join(B_motif(bii7, 1, 'tempo'), B_motif(bii7d5, 1), B_motif(bI7, 1), B_motif(bI7, 1, 'alt'))

        B = ['B1', 'B1', 'B2', 'B2', 'B2', 'B3', 'B3', 'B4']

        def combine(lh, rh):
            return {
                'treble': triplets(subset(sections[rh]['treble'], 2, 7) * 8 + subset(sections[rh]['treble'], 56, 61) * 8),
                'bass1': sections[lh]['bass1'],
                'bass2': sections[lh]['bass2'],
            }

        sections['C1'] = combine('A1', 'B1')
        sections['C1']['treble'] = tempo_change('4/4') + sections['C1']['treble']
        sections['C2'] = combine('A2', 'B2')
        sections['C3'] = combine('A3', 'B3')
        sections['C4'] = combine('A4', 'B4')

        C = ['C1', 'C1', 'C2', 'C2', 'C2', 'C3', 'C3', 'C4']

        def D_motif(chord, section):
            motif = {}
            motif['bass1'] = sections[section]['bass1']
            motif['bass2'] = sections[section]['bass2']
            if len(chord) == 3:
                motif['treble'] = self.harmonize(notes(pattern(chord, 1, 1, 2, 3, 3), [1, 2, 2, 1, 1], '~   ~ '), 1, 'octave')
            else:
                motif['treble'] = self.harmonize(notes(pattern(chord, 1, 1, 2, 2), 1, '~ '), 1, 'octave')
            return motif

        diii = arpeggio('a`', 3, 'A Minor')
        dI = ['f``', 'f``']
        dii = ['f``', 'df``', 'c``']

        sections['D1'] = D_motif(diii, 'A1')
        sections['D2'] = D_motif(diii, 'A2')
        sections['D3'] = D_motif(dI * 2, 'A3')
        sections['D4'] = D_motif(dii, 'A4')

        D = ['D1', 'D1', 'D2', 'D2', 'D2', 'D3', 'D3', 'D4']

        for section in sections:
            name(sections[section]['treble'], section)

        order = [A, A, B, C, C, B, A, A, B, D, D]
        structure = ['A0']
        for item in order:
            structure += [item, 'A0']

        if self.summary:
            sections_to_print = sections
        else:
            sections_to_print = flatten(structure)

        for section in sections_to_print:
            self.score["treble"] += sections[section]['treble'] + ["\\break\n"]
            if 'B' not in section:
                self.score['bass'] += voices(sections[section]['bass1'], sections[section]['bass2'])
            else:
                self.score['bass'] += sections[section]['bass']

    def end_score(self):
        return ('>>\n  \\layout {\n \\context {\n \\Score\n \\override SpacingSpanner.common-shortest-duration =\n #(ly:make-moment 1/8)\n }\n }\n }')


if __name__ == "__main__":
    MadRush()
