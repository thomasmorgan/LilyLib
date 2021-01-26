from piece import Piece
from util import pattern, select
from tones import tonify
from points import note, notes, chord, rest
from markup import voices


class PreludeInCSimple(Piece):

    def details(self):
        self.title = "Prelude in C"
        self.composer = "J. S. Bach"
        self.opus = "BVW 846"

    def write_score(self):
        self.score["treble"], self.score["bass"] = [], []

        def motif(c):
            tones = tonify(c)
            self.score["bass"] += 2 * voices(rest(16) + notes(select(tones, 2), ['8.', 4], "~ "), note(select(tones, 1), 2))
            self.score["treble"] += 2 * (rest(8) + notes(pattern(tones, 2 * [3, 4, 5]), 16))

        bar = [''] * 40

        bar[1] = 'c` e` g` c`` e``'
        bar[2] = 'c` d` g` c`` e``'
        bar[3] = 'b d` g` d`` f``'
        bar[4] = 'c` e` g` c`` e``'

        bar[5] = 'c` e` a` e`` a``'
        bar[6] = 'c` d` df` a` d``'
        bar[7] = 'b d` g` d`` g``'
        bar[8] = 'b c` e` g` c``'

        bar[9] = 'a c` e` g` c``'
        bar[10] = 'd a d` fs` c``'
        bar[11] = 'g b d` g` b`'
        bar[12] = 'g bf e` g` cs``'

        bar[13] = 'f a d` a` d``'
        bar[14] = 'f af d` f` b`'
        bar[15] = 'e g c` g` c``'
        bar[16] = 'e f a c` f`'

        bar[17] = 'd f a c` f`'
        bar[18] = 'g, d g b f`'
        bar[19] = 'c e g c` e`'
        bar[20] = 'c g bf c` e`'

        bar[21] = 'f, f a c` e`'
        bar[22] = 'fs, c a c` ef`'
        bar[23] = 'af, f b c` d`'
        bar[24] = 'g, f g b d`'

        bar[25] = 'g, e g c` e`'
        bar[26] = 'g, d g c` f`'
        bar[27] = 'g, d g b f`'
        bar[28] = 'g, ef a c` fs`'

        bar[29] = 'g, e g c` g`'
        bar[30] = 'g, d g c` f`'
        bar[31] = 'g, d g b f`'
        bar[32] = 'c, c g bf e`'

        for c in bar:
            if c:
                motif(c)

        def held_bass(tones):
            tones = tonify(tones)
            return voices(rest(16) + notes(tones[1], ['8.', 4, 2], "~ ~ "), note(tones[0], 1))

        def long_melody(tones):
            tones = tonify(tones)
            return rest(8) + notes(pattern(tones, 1, 2, 3, 4, 3, 2, 3, 2, 1, 2), 16)

        self.score['treble'] += long_melody('f a c` f`') + notes('f d', 16) * 2
        self.score['treble'] += long_melody('g` b` d`` f``') + pattern(self.scale('d`', 'f`', 16), 1, 3, 2, 1)
        self.score["bass"] += held_bass('c, c') + held_bass('c, b,')

        self.score['treble'] += [chord('e` g` c`', 1)]
        self.score['bass'] += [chord('c, c', 1)]


if __name__ == "__main__":
    PreludeInCSimple()
