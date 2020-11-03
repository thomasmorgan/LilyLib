from piece import Piece
from util import merge, subset, select, duplicate


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

        grace, notes, transpose, harmonize, rests, tones, scale, chord, arpeggio, diminished7, voices, add, name, remove = self.grace, self.notes, self.transpose, self.harmonize, self.rests, self.tones, self.scale, self.chord, self.arpeggio, self.diminished7, self.voices, self.add, self.name, self.remove

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

        def plod(tone):
            tone = tones(tone) * 2
            return 2 * plink(tone[0]) + plonk(tone[1])

        plodding = [plod(x) for x in 4 * ['ef'] + ['ef f', 'f gf', 'ef f']] + [plonk('f') + plonk2('bf')]
        plodding[0].insert(5, '\\stemDown')

        def drone1(tone, interval=-2):
            note = notes(tone, 2)
            chord1 = harmonize(note, interval, 'scale')
            chord2 = transpose(chord1, -1, 'scale')
            chord3 = transpose(chord2, -1, 'semitone')
            return chord1 + chord2 + chord3 + chord2

        def drone2(tone, interval=-2):
            return harmonize(scale(tone, -4, 2), interval, 'scale')

        drone_a = drone1('ef`') + drone1('cf`')
        self.set_key('bf minor')
        drone_b = drone2('gf`') + subset(drone1('ef`'), 1, 3) + notes('bf', 2)

        intro = {
            'treble': self.repeat(['\\grace s16.'] + rests(1) * 8),
            'bass': self.voices(drone_a + drone_b, plodding)
        }

        self.name(intro['treble'], 'Play first repeat one octave lower')

        """ Bold Chords """

        self.set_key('ef minor')

        rh_melody = [''] * 9
        rh_melody[1] = scale('cf``', 'f`', ['4.', 8, 4], step=2) + notes('f` f`', ['8.', 16])
        rh_melody[2] = scale('af`', 'ef`', [8, 8, '8.', 16]) + notes('f`', 2)
        rh_melody[3] = scale('gf`', 'cf``', [4, '8.', 16, '4.']) + notes('af`', 8)
        rh_melody[4] = scale('f`', 'ef``', [8, 8, '8.', 16], step=2) + notes('df``', 2)
        rh_melody[5] = scale('bf`', 'ef``', [4, '8.', 16, '4.']) + notes('cf``', 8)
        rh_melody[6] = notes('bf` af` bf`', [4, 4, 2])
        rh_melody[7] = duplicate(rh_melody[5])
        rh_melody[8] = scale('bf`', 'gf`', [4, 4, 2])

        lh_melody = transpose(rh_melody, -1)
        lh_melody[3] = rests(2) + scale('af,', 'ef', [4, '8.', 16], step=2)
        lh_melody[4] = rests(2) + scale('bf,', 'f', [4, '8.', 16], step=2)
        lh_melody[5] = rests(['2..']) + notes('cf`', 8)
        lh_melody[7] = subset(lh_melody[7], 1, 3) + rests(2)
        lh_melody[8] = transpose(lh_melody[8], 2, 'scale')

        rh_harmony = [''] * 9
        rh_harmony[1] = [chord(diminished7('d`', note, key='cf major'), note.dur) for note in rh_melody[1]]
        rh_harmony[2] = [chord('c` ef`', 4), chord('a c`', '8.'), chord('a c`', 16), chord('bf d`', 2)]
        rh_harmony[3] = [chord(arpeggio('bf', 'gf`'), note.dur) for note in subset(rh_melody[3], 1, 3)] + [chord(arpeggio('cf`', 'gf`', key='cf major'), 2)]
        rh_harmony[4] = [chord('df` f`', 4)] + [chord('df` f` af`', d) for d in ['8.', 16, 2]]
        rh_harmony[5] = [chord(arpeggio('ef`', 'bf`'), note.dur) for note in rh_melody[5]]
        remove(select(rh_harmony[5], 5), 'bf`')
        rh_harmony[6] = [chord('df` gf`', 4), chord('df` f`', 4), chord('d` f` af`', 2)]
        rh_harmony[7] = subset(rh_harmony[5], 1, 4) + [chord('ef` af`', 8)]
        rh_harmony[8] = notes('gf`', 4) + [chord('df` f`', 4)] + notes('df`', 2)

        lh_harmony = [''] * 9
        lh_harmony[1] = transpose(rh_harmony[1], -1)
        add(subset(lh_harmony[1], 1, 4), 'bf,')
        lh_harmony[2] = transpose(rh_harmony[2], -1)
        add(lh_harmony[2], 'bf,')
        remove(lh_harmony[2], 'a,')
        lh_harmony[3] = [chord('ef gf', dur=c.dur) for c in rh_harmony[3]]
        lh_harmony[4] = transpose(rh_harmony[4], -1)
        lh_harmony[5] = transpose(rh_harmony[5], -1)
        add(subset(lh_harmony[5], 1, 3), 'df`')
        add(subset(lh_harmony[5], 4, 5), 'cf')
        lh_harmony[6] = transpose(rh_harmony[6], -1)
        lh_harmony[7] = duplicate(subset(lh_harmony[5], 1, 4)) + [chord('cf ef af', 8)]
        remove(lh_harmony[7], 'df`')
        lh_harmony[8] = [chord('df gf', 4), chord('df f', 4), chord('gf, df', 2)]

        name(rh_melody[1], "Bf/d7, Bf")
        name(rh_melody[2], "Af, FD7, Bf")
        name(rh_melody[3], "Efm, Cf")
        name(rh_melody[4], "d7, Df")
        name(rh_melody[5], "EfD7, Cf7")
        name(rh_melody[6], "Gf, Df, d7")
        name(rh_melody[7], "Ef, Ef6, Af")
        name(rh_melody[8], "Gf, DfD7, Gf")

        bold_chords = {
            'treble': voices(rh_melody, rh_harmony),
            'bass': voices(lh_melody, lh_harmony)
        }

        """ Intro again """

        self.set_key('fs minor')
        shifted_bass = self.key_signature + transpose(subset(plodding, 1, 7), 3, 'semitone') + self.tempo_change('2/4') + plonk('gs') + self.tempo_change('4/4')

        drone_c = drone1('fs`', 5) + drone1('d`', 5)
        add(drone_c, 'fs`')
        drone_c = self.key_signature + drone_c

        self.set_key('cs minor')
        drone_d = drone2('a`', 5) + subset(drone1('fs`', 5), 1, 3)
        add(subset(drone_d, 1, 2), 'cs``')

        intro2 = {
            'treble': drone_c + drone_d,
            'bass': shifted_bass
        }

        self.score = merge(intro, bold_chords, intro2)

    def end_score(self):
        return ('>>\n  \\layout {\n \\context {\n \\Score\n \\override SpacingSpanner.common-shortest-duration =\n #(ly:make-moment 1/15)\n }\n }\n }')


if __name__ == "__main__":
    MarcheFunebre()
