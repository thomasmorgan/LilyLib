from piece import Piece
from util import pattern, select, remove, subset


class PreludeInC(Piece):

    def details(self):
        self.title = "Prelude in C"
        self.composer = "J. S. Bach"
        self.opus = "BVW 846"
        self.summary = True
        self.annotate = True

    def write_score(self):
        notes, tones, chord, rests, voices = self.notes, self.tones, self.chord, self.rests, self.voices
        arpeggio, arpeggio7, dominant7, diminished7 = self.arpeggio, self.arpeggio7, self.dominant7, self.diminished7
        transpose = self.transpose
        self.score["treble"], self.score["bass"] = [], []

        def motif(c):
            tones = c[0]
            if self.summary:
                bass = [chord(subset(tones, 1, 2), 4)]
                treble = [chord(subset(tones, 3, 5), 4)]
            else:
                bass = 2 * voices(rests(16) + notes(pattern(tones, [2, 2]), ['8.', 4], "~ "), notes(pattern(tones, [1]), 2))
                treble = 2 * (rests(8) + notes(pattern(tones, [3, 4, 5, 3, 4, 5]), 16)) + ["\n"]
            if self.annotate:
                self.name(treble, c[1])
            self.score["bass"] += bass
            self.score["treble"] += treble

        bar = [''] * 40

        bar[1] = (arpeggio('c`', 'e``'), 'I')
        bar[2] = (tones('c` d`') + arpeggio('a`', 'f``', key='D Minor'), 'ii D7')
        bar[3] = (select(dominant7('b', 'f``', key='G Major'), [1, 2, 4, 6, 7]), 'V D7')
        bar[4] = bar[1]

        bar[5] = (remove(arpeggio('c`', 'a``', key='A Minor'), [4]), 'vi')
        bar[6] = (tones('c`') + arpeggio('d`', 'd``', key='D Major'), 'II D7')
        bar[7] = (transpose(bar[5][0], -1, 'scale'), 'V')
        bar[8] = (tones('b') + arpeggio('c`', 'c``'), 'I7')

        bar[9] = (remove(arpeggio7('a', 'c``', key='A Minor'), [5]), 'vi7')
        bar[10] = (select(dominant7('d', 8, key='D Major'), [1, 3, 5, 6, 8]), 'II D7')
        bar[11] = (arpeggio('g', 5, key='G Major'), 'V')
        bar[12] = (select(diminished7('g', 7, key='G Minor'), [1, 2, 4, 5, 7]), 'V d7')

        bar[13] = (remove(arpeggio('f', 'd``', key='D Minor'), [4]), 'ii')
        bar[14] = (remove(diminished7('f', 'b`', key='F Minor'), [3, 6]), 'iv d7')
        bar[15] = (transpose(bar[13][0], -1, 'scale'), 'I')
        bar[16] = (remove(arpeggio7('e', 'f`', key='F Major'), [5]), 'IV7')

        bar[17] = (remove(arpeggio7('d', 'f`', key='D Minor'), [5]), 'ii7')
        bar[18] = (remove(dominant7('g,', 'f`', key='G Major'), [2, 4, 7]), 'V D7')
        bar[19] = (arpeggio('c', 'e`'), 'I')
        bar[20] = (remove(dominant7('c', 'e`'), [2]), 'I D7')

        for c in bar:
            if c:
                motif(c)

    def end_score(self):
        return ('>>\n  \\layout {\n \\context {\n \\Score\n \\override SpacingSpanner.common-shortest-duration =\n #(ly:make-moment 1/16)\n }\n }\n }')


if __name__ == "__main__":
    PreludeInC()
