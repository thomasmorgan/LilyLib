from util import subset, join
from tones import tonify
from points import chord
from demos.demo_prelude_in_c import PreludeInC


class PreludeInCFancy(PreludeInC):

    @property
    def chord_names(self):
        return ['I', 'ii D7', 'V D7', 'I',
                'vi', 'II D7', 'V', 'I7',
                'vi7', 'II D7', 'V', 'V d7',
                'ii', 'ii d7', 'I', 'IV7',
                'ii7', 'V D7', 'I', 'I D7',
                'IV7', 'VI d7', 'IV ?', 'V D7',
                'I', 'V 4/7', 'V D7', 'V/VI d7',
                'I', 'V 4/7', 'V D7', 'I D7']

    def write_score(self):
        self.score = join([self.motif(chord, name) for chord, name in zip(self.chords, self.chord_names)])
        self.score = join(self.score, self.outro)

    def motif(self, c, n):
        summary = True
        annotate = True
        if summary:
            tones = tonify(c)
            passage = {
                'treble': [chord(subset(tones, 3, 5), 4)],
                'bass': [chord(subset(tones, 1, 2), 4)]
            }
        else:
            passage = super().motif(c)

        if annotate:
            select(passage['treble'], 1).markup = n

        return passage

    def end_score(self):
        return ('>>\n  \\layout {\n \\context {\n \\Score\n \\override SpacingSpanner.common-shortest-duration =\n #(ly:make-moment 1/16)\n }\n }\n }')


if __name__ == "__main__":
    PreludeInCFancy()
