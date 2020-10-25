from piece import Piece
from util import pattern, select, remove


class PreludeInC(Piece):

    def details(self):
        self.title = "Prelude in C"
        self.composer = "J. S. Bach"
        self.opus = "BVW 846"

    def write_score(self):
        notes, tones, chord, rests, voices = self.notes, self.tones, self.chord, self.rests, self.voices
        scale, arpeggio, arpeggio7, dominant7, diminished7 = self.scale, self.arpeggio, self.arpeggio7, self.dominant7, self.diminished7
        transpose = self.transpose
        self.score["treble"], self.score["bass"] = [], []

        def motif(tones):
            self.score["bass"] += 2 * voices(rests(16) + notes(select(tones, 2), ['8.', 4], "~ "), notes(select(tones, 1), 2))
            self.score["treble"] += 2 * (rests(8) + notes(pattern(tones, 2 * [3, 4, 5]), 16))

        bar = [''] * 40

        bar[1] = arpeggio('c`', 'e``')
        bar[2] = remove(dominant7('c`', 'f``', key='D Minor'), 3, 5)
        bar[3] = remove(dominant7('b', 'f``', key='G Major'), 3, 5)
        bar[4] = bar[1]

        bar[5] = remove(arpeggio('c`', 'a``', key='A Minor'), 4)
        bar[6] = tones('c`') + arpeggio('d`', 'd``', key='D Major')
        bar[7] = transpose(bar[5], -1, 'scale')
        bar[8] = tones('b') + arpeggio('c`', 'c``')

        bar[9] = remove(arpeggio7('a', 'c``', key='A Minor'), 5)
        bar[10] = select(dominant7('d', 8, key='D Major'), 1, 3, 5, 6, 8)
        bar[11] = arpeggio('g', 5, key='G Major')
        bar[12] = select(diminished7('g', 7, key='G Minor'), 1, 2, 4, 5, 7)

        bar[13] = remove(arpeggio('f', 'd``', key='D Minor'), 4)
        bar[14] = remove(diminished7('f', 'b`', key='F Minor'), 3, 6)
        bar[15] = transpose(bar[13], -1, 'scale')
        bar[16] = remove(arpeggio7('e', 'f`', key='F Major'), 5)

        bar[17] = remove(arpeggio7('d', 'f`', key='D Minor'), 5)
        bar[18] = remove(dominant7('g,', 'f`', key='G Major'), 2, 4, 7)
        bar[19] = arpeggio('c', 'e`')
        bar[20] = remove(dominant7('c', 'e`'), 2)

        bar[21] = remove(arpeggio7('f,', 'e`', key='F Major'), 2, 3, 4)
        bar[22] = remove(diminished7('fs,', 'ds`'), 2, 4, 5)
        bar[23] = tones('af, f b c` d`')
        bar[24] = remove(arpeggio7('g,', 'd`', key='G Major'), 2, 3)

        bar[25] = remove(arpeggio('g,', 'e`'), 2)
        bar[26] = tones('g, d g c` f`')
        bar[27] = remove(dominant7('g,', 'f`', key='G Major'), 2, 4, 7)
        bar[28] = tones('g,') + remove(diminished7('ds', 'fs`'), 2, 5)

        bar[29] = remove(arpeggio('g,', 'g`'), 2, 6)
        bar[30] = bar[26]
        bar[31] = bar[27]
        bar[32] = remove(dominant7('c,', 'e`'), 2, 3, 4, 6, 9)

        for c in bar:
            if c:
                motif(c)

        self.score['treble'] += rests(8) + pattern(notes('d', 16) + arpeggio('f', 'f`', 16, key='F Major'), [2, 3, 4, 5, 4, 3, 4, 3, 2, 3, 2, 1, 2, 1])
        self.score['treble'] += rests(8) + pattern(dominant7('g`', 'f``', 16, key='G Major'), [1, 2, 3, 4, 3, 2, 3, 2, 1, 2]) + pattern(scale('d`', 'f`', 16), [1, 3, 2, 1])
        self.score["bass"] += 2 * voices(rests(16) + notes('b,', ['8.', 4, 2], "~ ~ "), notes('c,', 1))

        self.score['treble'] += [chord(arpeggio('e`', 'c``'), 1)]
        self.score['bass'] += [chord('c, c', 1)]

    def end_score(self):
        return ('>>\n  \\layout {\n \\context {\n \\Score\n \\override SpacingSpanner.common-shortest-duration =\n #(ly:make-moment 1/8)\n }\n }\n }')


if __name__ == "__main__":
    PreludeInC()
