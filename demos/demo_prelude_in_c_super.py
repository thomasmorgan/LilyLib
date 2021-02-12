from staves import Super
from markup import voices
from tones import tonify
from points import note, notes, rests
from demos.demo_prelude_in_c import PreludeInC


class PreludeInCSuper(PreludeInC):

    def details(self):
        super().details()
        self.staves = [Super()]

    def motif(self, c):
        passage = super().motif(c)
        new_passage = {
            'treble': voices(passage['treble'], notes(tonify(c)[0:2], 16) + rests(8, 4))
        }
        new_passage['treble'][0].prefix += ' \\override Rest.transparent = ##t '
        new_passage['treble'][14].prefix += ' \\override Rest.transparent = ##t '
        new_passage['treble'][14].ornamentation = 'laissezVibrer'
        new_passage['treble'][15].ornamentation = 'laissezVibrer'
        return new_passage

    @property
    def outro(self):
        passage = super().outro
        new_passage = {'treble': voices(passage['treble'], passage['bass'])}
        new_passage['treble'][0].prefix += ' \\override Rest.transparent = ##t '
        return new_passage

    def held_bass(self, tones):
        tones = tonify(tones)
        return note(tones[0], 16, ornamentation='laissezVibrer', prefix=' \\override Rest.transparent = ##t ') + note(tones[1], 16, ornamentation='laissezVibrer') + rests(8, 4, 2)


if __name__ == "__main__":
    PreludeInCSuper()
