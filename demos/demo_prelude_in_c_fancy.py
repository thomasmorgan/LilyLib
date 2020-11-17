from piece import Piece
from util import pattern, select, omit, subset
from tones import tonify
from points import note, notes, chord, rest, dominant7, arpeggio, arpeggio7, diminished7
from markup import voices, name


class PreludeInCFancy(Piece):

    def details(self):
        self.title = "Prelude in C"
        self.composer = "J. S. Bach"
        self.opus = "BVW 846"
        self.summary = True
        self.annotate = True

    def write_score(self):
        self.score["treble"], self.score["bass"] = [], []

        def motif(c):
            tones = tonify(c[0])
            if self.summary:
                bass = chord(subset(tones, 1, 2), 4)
                treble = chord(subset(tones, 3, 5), 4)
            else:
                bass = 2 * voices(rest(16) + notes(select(tones, 2), ['8.', 4], "~ "), note(select(tones, 1), 2))
                treble = 2 * (rest(8) + notes(pattern(tones, [3, 4, 5, 3, 4, 5]), 16)) + ["\n"]
            if self.annotate:
                name(treble, c[1])
            self.score["bass"] += bass
            self.score["treble"] += treble

        bar = [''] * 40

        bar[1] = (self.arpeggio('c`', 'e``'), 'I')
        bar[2] = (omit(arpeggio7('c`', 'f``', 'D Minor'), 3, 5), 'ii D7')
        bar[3] = (omit(dominant7('b', 'f``', 'G Major'), 3, 5), 'V D7')
        bar[4] = bar[1]

        bar[5] = (omit(arpeggio('c`', 'a``', 'A Minor'), 4), 'vi')
        bar[6] = (['c`'] + arpeggio('d`', 'd``', 'D Major'), 'II D7')
        bar[7] = (self.transpose(bar[5][0], -1), 'V')
        bar[8] = (['b'] + self.arpeggio('c`', 'c``'), 'I7')

        bar[9] = (omit(arpeggio7('a', 'c``', 'A Minor'), 5), 'vi7')
        bar[10] = (select(dominant7('d', 8, 'D Major'), 1, 3, 5, 6, 8), 'II D7')
        bar[11] = (arpeggio('g', 5, 'G Major'), 'V')
        bar[12] = (select(diminished7('g', 7, 'G Minor'), 1, 2, 4, 5, 7), 'V d7')

        bar[13] = (omit(arpeggio('f', 'd``', 'D Minor'), 4), 'ii')
        bar[14] = (omit(diminished7('f', 'b`', 'D Minor'), 3, 6), 'ii d7')
        bar[15] = (self.transpose(bar[13][0], -1), 'I')
        bar[16] = (omit(arpeggio7('e', 'f`', 'F Major'), 5), 'IV7')

        bar[17] = (omit(arpeggio7('d', 'f`', 'D Minor'), 5), 'ii7')
        bar[18] = (omit(dominant7('g,', 'f`', 'G Major'), 2, 4, 7), 'V D7')
        bar[19] = (self.arpeggio('c', 'e`'), 'I')
        bar[20] = (omit(self.dominant7('c', 'e`'), 2), 'I D7')

        bar[21] = (omit(arpeggio7('f,', 'e`', 'F Major'), 2, 3, 4), 'IV7')
        bar[22] = (omit(diminished7('fs,', 'ef`', 'A Major'), 2, 4, 5), 'VI d7')
        bar[23] = ('af, f b c` d`', 'IV ?')
        bar[24] = (omit(dominant7('g,', 'd`', 'G Major'), 2, 3), 'V D7')

        bar[25] = (omit(self.arpeggio('g,', 'e`'), 2), 'I')
        bar[26] = ('g, d g c` f`', 'V 4/7')
        bar[27] = (omit(dominant7('g,', 'f`', 'G Major'), 2, 4, 7), 'V D7')
        bar[28] = (['g,'] + omit(diminished7('ef', 'fs`', 'A Major'), 2, 5), 'V/VI d7')

        bar[29] = (omit(self.arpeggio('g,', 'g`'), 2, 6), 'I')
        bar[30] = bar[26]
        bar[31] = bar[27]
        bar[32] = (omit(self.dominant7('c,', 'e`'), 2, 3, 4, 6, 9), 'I D7')

        for c in bar:
            if c:
                motif(c)

        self.score['treble'] += rest(8) + pattern(note('d', 16) + arpeggio('f', 'f`', 'F Major', 16), 2, 3, 4, 5, 4, 3, 4, 3, 2, 3, 2, 1, 2, 1)
        self.score['treble'] += rest(8) + pattern(dominant7('g`', 'f``', 'G Major', 16), 1, 2, 3, 4, 3, 2, 3, 2, 1, 2) + pattern(self.scale('d`', 'f`', 16), 1, 3, 2, 1)
        self.score["bass"] += voices(rest(16) + notes('c', ['8.', 4, 2], "~ ~ "), note('c,', 1)) + voices(rest(16) + notes('b,', ['8.', 4, 2], "~ ~ "), note('c,', 1))

        self.score['treble'] += [chord(self.arpeggio('e`', 'c``'), 1)]
        self.score['bass'] += [chord('c, c', 1)]

    def end_score(self):
        return ('>>\n  \\layout {\n \\context {\n \\Score\n \\override SpacingSpanner.common-shortest-duration =\n #(ly:make-moment 1/16)\n }\n }\n }')


if __name__ == "__main__":
    PreludeInCFancy()
