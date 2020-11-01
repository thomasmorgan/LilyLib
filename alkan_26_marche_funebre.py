from piece import Piece
from util import merge, select


class MarcheFunebre(Piece):

    def details(self):
        self.title = "Marche Funebre"
        self.composer = "Charles Valentin Alkan"
        self.opus = "Op. 26"
        self.key = "Ef Minor"

    def subtext(self):
        return '''
            \\layout {
              \\context {
                \\Staff
                \\RemoveEmptyStaves
              }
            }
        '''

    def write_score(self):

        grace, notes, transpose, harmonize, rests, tones, scale, chord, arpeggio = self.grace, self.notes, self.transpose, self.harmonize, self.rests, self.tones, self.scale, self.chord, self.arpeggio

        """ Intro """

        def rise(tone):
            return grace(notes([transpose(transpose(tone, -1), -1, 'semitone'), transpose(tone, -1), tone], 32))

        def fall(tone):
            return harmonize(notes(tone, 8, ornamentation='\\staccato'), -1)

        def fall2(tone):
            return notes(transpose(tone, -1), 8, ornamentation='\\staccato')

        def plink(tone):
            return rise(tone) + fall(tone) + rests(8)

        def plonk(tone):
            return rise(tone) + 3 * fall(tone) + rests(8)

        def plonk2(tone):
            return rise(tone) + 3 * fall2(tone) + rests(8)

        def plod(tones):
            tones = self.tones(tones) * 2
            return 2 * plink(tones[0]) + plonk(tones[1])

        plodding = [plod(x) for x in 4 * ['ef,'] + ['ef, f,', 'f, gf,', 'ef, f,']] + plonk('f,') + plonk2('bf,')
        plodding[0].insert(5, '\\stemDown')

        def drone1(tone):
            note = notes(tone, 2)
            chord1 = harmonize(note, -2, 'scale')
            chord2 = transpose(chord1, -1, 'scale')
            chord3 = transpose(chord2, -1, 'semitone')
            return [chord1, chord2, chord3, chord2]

        def drone2(tone):
            return harmonize(scale(tone, -4, 2), -2, 'scale')

        def drone3(tone):
            return harmonize(scale(tone, -4, 2), [-2, -2, -2, 0], 'scale')

        drone_a = drone1('ef') + drone1('cf')
        self.set_key('bf minor')
        drone_b = drone2('gf') + drone3('ef')

        intro = {
            'treble': self.repeat(['\\grace s16.'] + rests(1) * 8),
            'bass': transpose(self.voices(drone_a + drone_b, plodding), 1)
        }

        """ Bold Chords """

        self.set_key('ef minor')

        melody = notes('cf`` af` f` f` f`', ['4.', 8, 4, '8.', 16])
        chords1_rh = [chord(self.diminished7('d`', note, key='Cf Major'), note.dur) for note in melody]
        chords1_lh = transpose(chords1_rh, -1)
        for c in chords1_lh:
            c.tones.extend(tones('bf,'))

        melody = scale('af`', 'ef`')
        durs = [8, 8, '8.', 16]
        # chords2_rh = [chord([tone, transpose(tone, -1)], dur) for tone, dur in zip(melody, durs)]

        chords2_rh = [
            chord(arpeggio(select(melody, 1)[0], -4, key='Af Major'), dur=durs[0]),
            chord(arpeggio(select(melody, 2)[0], -2, step=3), dur=durs[1]),
            chord(arpeggio(select(melody, 3)[0], -4, key='F Major'), dur=durs[2]),
            chord(arpeggio(select(melody, 4)[0], -2, step=3), dur=durs[3])
        ]

        bold_chords = {
            'treble': chords1_rh + chords2_rh,
            'bass': chords1_lh
        }

        self.name(intro['treble'], 'A: Play first repeat one octave below.')

        self.score = merge(intro, bold_chords)


if __name__ == "__main__":
    MarcheFunebre()
