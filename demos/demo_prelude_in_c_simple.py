from piece import Piece
from util import pattern, select, rep, join
from tones import tonify
from points import note, notes, chord, rest, tied_note
from markup import voices


class PreludeInCSimple(Piece):

    def details(self):
        self.title = "Prelude in C"
        self.composer = "J. S. Bach"
        self.opus = "BVW 846"

    def motif(self, c):
        tones = tonify(c)
        return {
            'treble': rep([rest(8)] + notes(pattern(tones, 2 * [3, 4, 5]), 16), 2),
            'bass': rep(voices([rest(16)] + tied_note(select(tones, 2), ['8.', 4]), [note(select(tones, 1), 2)]), 2)
        }

    @property
    def chords(self):
        bars = [
            'c` e` g` c`` e``',
            'c` d` a` d`` f``',
            'b d` g` d`` f``',
            'c` e` g` c`` e``',

            'c` e` a` e`` a``',
            'c` d` fs` a` d``',
            'b d` g` d`` g``',
            'b c` e` g` c``',

            'a c` e` g` c``',
            'd a d` fs` c``',
            'g b d` g` b`',
            'g bf e` g` cs``',

            'f a d` a` d``',
            'f af d` f` b`',
            'e g c` g` c``',
            'e f a c` f`',

            'd f a c` f`',
            'g, d g b f`',
            'c e g c` e`',
            'c g bf c` e`',

            'f, f a c` e`',
            'fs, c a c` ef`',
            'af, f b c` d`',
            'g, f g b d`',

            'g, e g c` e`',
            'g, d g c` f`',
            'g, d g b f`',
            'g, ef a c` fs`',

            'g, e g c` g`',
            'g, d g c` f`',
            'g, d g b f`',
            'c, c g bf e`'
        ]

        return bars

    def held_bass(self, tones):
        tones = tonify(tones)
        return voices([rest(16)] + tied_note(select(tones, 2), ['8.', 4, 2]), [note(select(tones, 1), 1)])

    def long_melody(self, tones):
        tones = tonify(tones)
        return [rest(8)] + notes(pattern(tones, 1, 2, 3, 4, 3, 2, 3, 2, 1, 2), 16)

    @property
    def outro(self):
        return {
            'treble': self.long_melody('f a c` f`') + rep(notes('f d', 16), 2) + self.long_melody('g` b` d`` f``') + pattern(self.scale('d`', 'f`', 16), 1, 3, 2, 1) + [chord('e` g` c`', 1)],
            'bass': self.held_bass('c, c') + self.held_bass('c, b,') + [chord('c, c', 1)]
        }

    def write_score(self):
        self.score = join([self.motif(chord) for chord in self.chords])
        self.score = join(self.score, self.outro)


if __name__ == "__main__":
    PreludeInCSimple()
