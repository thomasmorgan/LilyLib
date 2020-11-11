from piece import Piece
from util import pattern, select, remove, subset, tonify


class PreludeInCFancy(Piece):

    def details(self):
        self.title = "Prelude in C"
        self.composer = "J. S. Bach"
        self.opus = "BVW 846"
        self.summary = True
        self.annotate = True

    def write_score(self):
        note, notes, chord, rest, rests, voices = self.note, self.notes, self.chord, self.rest, self.rests, self.voices
        scale, arpeggio, arpeggio7, dominant7, diminished7 = self.scale, self.arpeggio, self.arpeggio7, self.dominant7, self.diminished7
        transpose = self.transpose
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
                self.name(treble, c[1])
            self.score["bass"] += bass
            self.score["treble"] += treble

        bar = [''] * 40

        bar[1] = (arpeggio('c`', 'e``'), 'I')
        bar[2] = (remove(dominant7('c`', 'f``', key='D Minor'), 3, 5), 'ii D7')
        bar[3] = (remove(dominant7('b', 'f``', key='G Major'), 3, 5), 'V D7')
        bar[4] = bar[1]

        bar[5] = (remove(arpeggio('c`', 'a``', key='A Minor'), [4]), 'vi')
        bar[6] = (['c`'] + arpeggio('d`', 'd``', key='D Major'), 'II D7')
        bar[7] = (transpose(bar[5][0], -1, 'scale'), 'V')
        bar[8] = (['b'] + arpeggio('c`', 'c``'), 'I7')

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

        bar[21] = (remove(arpeggio7('f,', 'e`', key='F Major'), [2, 3, 4]), 'IV7')
        bar[22] = (remove(diminished7('fs,', 'ds`'), [2, 4, 5]), 'I d7')
        bar[23] = ('af, f b c` d`', 'IV ?')
        bar[24] = (remove(arpeggio7('g,', 'd`', key='G Major'), [2, 3]), 'V7')

        bar[25] = (remove(arpeggio('g,', 'e`'), [2]), 'I')
        bar[26] = ('g, d g c` f`', 'V 4/7')
        bar[27] = (remove(dominant7('g,', 'f`', key='G Major'), [2, 4, 7]), 'V D7')
        bar[28] = (['g,'] + remove(diminished7('ds', 'fs`'), [2, 5]), 'V/i d7')

        bar[29] = (remove(arpeggio('g,', 'g`'), [2, 6]), 'I')
        bar[30] = bar[26]
        bar[31] = bar[27]
        bar[32] = (remove(dominant7('c,', 'e`'), [2, 3, 4, 6, 9]), 'I D7')

        for c in bar:
            if c:
                motif(c)

        self.score['treble'] += rests(8) + pattern(notes('d', 16) + arpeggio('f', 'f`', 16, key='F Major'), [2, 3, 4, 5, 4, 3, 4, 3, 2, 3, 2, 1, 2, 1])
        self.score['treble'] += rests(8) + pattern(dominant7('g`', 'f``', 16, key='G Major'), [1, 2, 3, 4, 3, 2, 3, 2, 1, 2]) + pattern(scale('d`', 'f`', 16), [1, 3, 2, 1])
        self.score["bass"] += 2 * voices(rests(16) + notes('b,', ['8.', 4, 2], "~ ~ "), notes('c,', 1))

        self.score['treble'] += [chord(arpeggio('e`', 'c``'), 1)]
        self.score['bass'] += [chord('c, c', 1)]

    def end_score(self):
        return ('>>\n  \\layout {\n \\context {\n \\Score\n \\override SpacingSpanner.common-shortest-duration =\n #(ly:make-moment 1/16)\n }\n }\n }')


if __name__ == "__main__":
    PreludeInCFancy()
