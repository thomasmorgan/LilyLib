from piece import Piece
from util import pattern, select, omit
from tones import tonify
from points import note, notes, chord, rest, rests, dominant7, arpeggio, arpeggio7, diminished7
from markup import voices


class PreludeInC(Piece):

    def details(self):
        self.title = "Prelude in C"
        self.composer = "J. S. Bach"
        self.opus = "BVW 846"

    def write_score(self):
        self.score["treble"], self.score["bass"] = [], []

        def motif(tones):
            tones = tonify(tones)
            self.score["bass"] += 2 * voices(rest(16) + notes(select(tones, 2), ['8.', 4], "~ "), note(select(tones, 1), 2))
            self.score["treble"] += 2 * (rest(8) + notes(pattern(tones, 2 * [3, 4, 5]), 16))

        bar = [''] * 40

        bar[1] = self.arpeggio('c`', 'e``')
        bar[2] = omit(arpeggio7('c`', 'f``', 'D Minor'), 3, 5)
        bar[3] = omit(dominant7('b', 'f``', 'G Major'), 3, 5)
        bar[4] = bar[1]

        bar[5] = omit(arpeggio('c`', 'a``', 'A Minor'), 4)
        bar[6] = ['c`'] + arpeggio('d`', 'd``', 'D Major')
        bar[7] = self.transpose(bar[5], -1)
        bar[8] = ['b'] + self.arpeggio('c`', 'c``')

        bar[9] = omit(arpeggio7('a', 'c``', 'A Minor'), 5)
        bar[10] = select(dominant7('d', 8, 'D Major'), 1, 3, 5, 6, 8)
        bar[11] = arpeggio('g', 5, 'G Major')
        bar[12] = select(diminished7('g', 7, 'G Minor'), 1, 2, 4, 5, 7)

        bar[13] = omit(arpeggio('f', 'd``', 'D Minor'), 4)
        bar[14] = omit(diminished7('f', 'b`', 'D Minor'), 3, 6)
        bar[15] = self.transpose(bar[13], -1)
        bar[16] = omit(arpeggio7('e', 'f`', 'F Major'), 5)

        bar[17] = omit(arpeggio7('d', 'f`', 'D Minor'), 5)
        bar[18] = omit(dominant7('g,', 'f`', 'G Major'), 2, 4, 7)
        bar[19] = self.arpeggio('c', 'e`')
        bar[20] = omit(self.dominant7('c', 'e`'), 2)

        bar[21] = omit(arpeggio7('f,', 'e`', 'F Major'), 2, 3, 4)
        bar[22] = omit(diminished7('fs,', 'ef`', 'A Major'), 2, 4, 5)
        bar[23] = 'af, f b c` d`'
        bar[24] = omit(arpeggio7('g,', 'd`', 'G Major'), 2, 3)

        bar[25] = omit(self.arpeggio('g,', 'e`'), 2)
        bar[26] = 'g, d g c` f`'
        bar[27] = omit(dominant7('g,', 'f`', 'G Major'), 2, 4, 7)
        bar[28] = ['g,'] + omit(diminished7('ef', 'fs`', 'A Major'), 2, 5)

        bar[29] = omit(self.arpeggio('g,', 'g`'), 2, 6)
        bar[30] = bar[26]
        bar[31] = bar[27]
        bar[32] = omit(self.dominant7('c,', 'e`'), 2, 3, 4, 6, 9)

        for c in bar:
            if c:
                motif(c)

        self.score['treble'] += rests(8) + pattern(notes('d', 16) + arpeggio('f', 'f`', 'F Major', 16), [2, 3, 4, 5, 4, 3, 4, 3, 2, 3, 2, 1, 2, 1])
        self.score['treble'] += rests(8) + pattern(dominant7('g`', 'f``', 'G Major', 16), [1, 2, 3, 4, 3, 2, 3, 2, 1, 2]) + pattern(self.scale('d`', 'f`', 16), [1, 3, 2, 1])
        self.score["bass"] += 2 * voices(rest(16) + notes('b,', ['8.', 4, 2], "~ ~ "), note('c,', 1))

        self.score['treble'] += [chord(self.arpeggio('e`', 'c``'), 1)]
        self.score['bass'] += [chord('c, c', 1)]

    def end_score(self):
        return ('>>\n  \\layout {\n \\context {\n \\Score\n \\override SpacingSpanner.common-shortest-duration =\n #(ly:make-moment 1/8)\n }\n }\n }')


if __name__ == "__main__":
    PreludeInC()
