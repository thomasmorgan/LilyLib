from util import select, omit, assign
from points import dominant7, arpeggio, arpeggio7, diminished7
from demos.demo_prelude_in_c_simple import PreludeInCSimple
from copy import deepcopy


class PreludeInC(PreludeInCSimple):

    @property
    def chords(self):
        bars = [''] * 32

        assign(bars, 1, self.arpeggio('c`', 'e``'))
        assign(bars, 2, omit(arpeggio7('c`', 'f``', 'D Minor'), 3, 5))
        assign(bars, 3, omit(dominant7('b', 'f``', 'G Major'), 3, 5))
        assign(bars, 4, deepcopy(select(bars, 1)))

        assign(bars, 5, omit(arpeggio('c`', 'a``', 'A Minor'), 4))
        assign(bars, 6, ['c`'] + arpeggio('d`', 'd``', 'D Major'))
        assign(bars, 7, self.transpose(select(bars, 5), -1))
        assign(bars, 8, ['b'] + self.arpeggio('c`', 'c``'))

        assign(bars, 9, omit(arpeggio7('a', 'c``', 'A Minor'), 5))
        assign(bars, 10, select(dominant7('d', 8, 'D Major'), 1, 3, 5, 6, 8))
        assign(bars, 11, arpeggio('g', 5, 'G Major'))
        assign(bars, 12, select(diminished7('g', 7, 'Cs Minor'), 1, 2, 4, 5, 7))

        assign(bars, 13, omit(arpeggio('f', 'd``', 'D Minor'), 4))
        assign(bars, 14, omit(diminished7('f', 'b``', 'B Minor'), 3, 6))
        assign(bars, 15, self.transpose(select(bars, 13), -1))
        assign(bars, 16, omit(arpeggio7('e', 'f`', 'F Major'), 5))

        assign(bars, 17, omit(arpeggio7('d', 'f`', 'D Minor'), 5))
        assign(bars, 18, omit(dominant7('g,', 'f`', 'G Major'), 2, 4, 7))
        assign(bars, 19, self.arpeggio('c', 'e`'))
        assign(bars, 20, omit(self.dominant7('c', 'e`'), 2))

        assign(bars, 21, omit(arpeggio7('f,', 'e`', 'F Major'), 2, 3, 4))
        assign(bars, 22, omit(diminished7('fs,', 'ef`', 'Fs Major'), 2, 4, 5))
        assign(bars, 23, 'af, f b c` d`')
        assign(bars, 24, omit(dominant7('g,', 'd`', 'G Major'), 2, 3))

        assign(bars, 25, omit(self.arpeggio('g,', 'e`'), 2))
        assign(bars, 26, 'g, d g c` f`')
        assign(bars, 27, omit(dominant7('g,', 'f`', 'G Major'), 2, 4, 7))
        assign(bars, 28, ['g,'] + omit(diminished7('ef', 'fs`', 'Fs Major'), 2, 5))

        assign(bars, 29, omit(self.arpeggio('g,', 'g`'), 2, 6))
        assign(bars, 30, deepcopy(select(bars, 26)))
        assign(bars, 31, deepcopy(select(bars, 27)))
        assign(bars, 32, omit(self.dominant7('c,', 'e`'), 2, 3, 4, 6, 9))

        return bars


if __name__ == "__main__":
    PreludeInC()
