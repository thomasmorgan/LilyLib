from staves import Super
from markup import voices
from tones import tonify
from points import note, notes, rests
from util import subset, select, rep
from demos.demo_prelude_in_c import PreludeInC


class PreludeInCSuper(PreludeInC):

    def details(self):
        super().details()
        self.staves = [Super()]

    def motif(self, c):
        passage = super().motif(c)
        new_passage = {
            'treble': voices(passage['treble'], rep(notes(subset(tonify(c), 1, 2), 16) + rests(8, 4), 2))
        }
        select(new_passage['treble'], 1).prefix += ' \\override Rest.transparent = ##t '
        select(new_passage['treble'], 15).prefix += ' \\override Rest.transparent = ##t '
        select(new_passage['treble'], 15).ornamentation = 'laissezVibrer'
        select(new_passage['treble'], 16).ornamentation = 'laissezVibrer'
        select(new_passage['treble'], 19).ornamentation = 'laissezVibrer'
        select(new_passage['treble'], 20).ornamentation = 'laissezVibrer'
        return new_passage

    @property
    def outro(self):
        passage = super().outro
        new_passage = {'treble': voices(passage['treble'], passage['bass'])}
        select(new_passage['treble'], 1).prefix += ' \\override Rest.transparent = ##t '
        return new_passage

    def held_bass(self, tones):
        tones = tonify(tones)
        return [note(select(tones, 1), 16, ornamentation='laissezVibrer', prefix=' \\override Rest.transparent = ##t '), note(select(tones, 2), 16, ornamentation='laissezVibrer')] + rests(8, 4, 2)


if __name__ == "__main__":
    PreludeInCSuper()
