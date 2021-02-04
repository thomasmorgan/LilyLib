from piece import Piece
from util import join, subset, select, flatten
from markup import linebreak, clef, grace, after_grace, repeat, voices, name, tempo_change
from tones import tonify, letter
from copy import deepcopy
from points import note, notes, rests, chord, chords, dominant7, diminished7, arpeggio, remove, add, merge, replace, transpose


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

        """ Intro """

        def rise(tone):
            return grace(notes([self.transpose(self.transpose(tone, -1, 'octave'), -1, 'semitone'), self.transpose(tone, -1, 'octave'), tone], 32))

        def fall(tone):
            return self.harmonize(note(tone, 8, ornamentation='\\staccato'), -1, 'octave')

        def fall2(tone):
            return note(self.transpose(tone, -1, 'octave'), 8, ornamentation='\\staccato')

        def plink(tone):
            return rise(tone) + fall(tone) + rests(8)

        def plonk(tone):
            return rise(tone) + 3 * fall(tone) + rests(8)

        def plonk2(tone):
            return rise(tone) + 3 * fall2(tone) + rests(8)

        def plod(tones):
            tones = tonify(tones)
            return 2 * plink(tones[0]) + plonk(tones[1])

        plodding = [plod(x) for x in 4 * ['ef ef'] + ['ef f', 'f gf', 'ef f']] + [plonk('f') + plonk2('bf')]
        plodding[0].insert(5, '\\stemDown')

        def drone1(tone, interval=-2):
            note = notes(tone, 2)
            chord1 = self.harmonize(note, interval, 'scale')
            chord2 = self.transpose(chord1, -1, 'scale')
            chord3 = self.transpose(chord2, -1, 'semitone')
            return chord1 + chord2 + chord3 + chord2

        def drone2(tone, interval=-2):
            return self.harmonize(self.scale(tone, -4, 2), interval, 'scale')

        drone_a = drone1('ef`') + drone1('cf`')
        self.set_key('bf minor')
        drone_b = drone2('gf`') + subset(drone1('ef`'), 1, 3) + notes('bf', 2)

        intro = {
            'treble': repeat(['\\grace s16.'] + rests(1) * 8),
            'bass': voices(drone_a + drone_b, plodding) + linebreak
        }

        name(intro['treble'], 'Play first repeat one octave lower')

        """ Bold Chords """

        self.set_key('ef minor')

        rh_melody = [''] * 9
        rh_melody[1] = self.scale('cf``', 'f`', ['4.', 8, 4], step=2) + notes('f` f`', ['8.', 16])
        rh_melody[2] = self.scale('af`', 'ef`', [8, 8, '8.', 16]) + notes('f`', 2)
        rh_melody[3] = self.scale('gf`', 'cf``', [4, '8.', 16, '4.']) + notes('af`', 8)
        rh_melody[4] = self.scale('f`', 'ef``', [8, 8, '8.', 16], step=2) + notes('df``', 2)
        rh_melody[5] = self.scale('bf`', 'ef``', [4, '8.', 16, '4.']) + notes('cf``', 8)
        rh_melody[6] = notes('bf` af` bf`', [4, 4, 2])
        rh_melody[7] = deepcopy(rh_melody[5])
        rh_melody[8] = self.scale('bf`', 'gf`', [4, 4, 2])

        lh_melody = self.transpose(rh_melody, -1, 'octave')
        lh_melody[3] = rests(2) + self.scale('af,', 'ef', [4, '8.', 16], step=2)
        lh_melody[4] = rests(2) + self.scale('bf,', 'f', [4, '8.', 16], step=2)
        lh_melody[5] = rests(['2..']) + notes('cf`', 8)
        lh_melody[7] = subset(lh_melody[7], 1, 3) + rests(2)
        lh_melody[8] = self.transpose(lh_melody[8], 2)

        rh_harmony = [''] * 9
        rh_harmony[1] = [chord(diminished7('d`', note.tone, key='d minor'), note.dur) for note in rh_melody[1]]
        rh_harmony[2] = [chord('c` ef`', 4), chord('a c`', '8.'), chord('a c`', 16), chord('bf d`', 2)]
        rh_harmony[3] = [chord(self.arpeggio('bf', 'gf`'), note.dur) for note in subset(rh_melody[3], 1, 3)] + [chord(arpeggio('cf`', 'gf`', key='cf major'), 2)]
        rh_harmony[4] = [chord('df` f`', 4)] + [chord('df` f` af`', d) for d in ['8.', 16, 2]]
        rh_harmony[5] = [chord(self.arpeggio('ef`', 'bf`'), note.dur) for note in rh_melody[5]]
        remove(select(rh_harmony[5], 5), 'bf`')
        rh_harmony[6] = [chord('df` gf`', 4), chord('df` f`', 4), chord('d` f` af`', 2)]
        rh_harmony[7] = subset(rh_harmony[5], 1, 4) + [chord('ef` af`', 8)]
        rh_harmony[8] = notes('gf`', 4) + [chord('df` f`', 4)] + notes('df`', 2)

        lh_harmony = self.transpose(rh_harmony, -1, 'octave')
        add(subset(lh_harmony[1], 1, 4), 'bf,')
        add(lh_harmony[2], 'bf,')
        remove(lh_harmony[2], 'a,')
        lh_harmony[3] = [chord('ef gf', dur=c.dur) for c in flatten(rh_harmony[3])]
        add(subset(lh_harmony[4], 1, 3), 'af cf`')
        remove(select(lh_harmony[4], 4), 'df')
        add(subset(lh_harmony[5], 1, 3), 'df`')
        add(subset(lh_harmony[5], 4, 5), 'cf')
        lh_harmony[7] = deepcopy(subset(lh_harmony[5], 1, 4)) + [chord('cf ef af', 8)]
        remove(lh_harmony[7], 'df`')
        lh_harmony[8] = [chord('df gf', 4), chord('df f', 4), chord('gf, df', 2)]

        bold_chords = {
            'treble': voices(rh_melody, rh_harmony),
            'bass': voices(lh_melody, lh_harmony)
        }

        """ Intro again """

        self.set_key('fs minor')
        shifted_bass = self.key_signature + self.transpose(subset(plodding, 1, 7), 3, 'semitone') + tempo_change('2/4') + plonk('gs') + tempo_change('4/4')

        drone_c = self.key_signature + drone1('fs`', 5) + drone1('d`', 5)
        add(drone_c, 'fs`')

        self.set_key('cs minor')
        drone_d = merge(drone2('a`', 5) + subset(drone1('fs`', 5), 1, 3), notes('cs`` cs`` bs` a` a` gs` fs`', 2))

        intro2 = {
            'treble': drone_c + drone_d,
            'bass': shifted_bass
        }

        """ Bold Chords again """

        self.set_key('fs minor')

        rh_melody2 = self.transpose(subset(rh_melody, 1, 7), 3, 'semitone')
        rh_melody2[4] = notes('gs`', 8) + self.scale('b`', 'e``', [8, '8.', 16, 2])
        rh_melody2[6] = self.scale('b`', 'a``', [8, 8, '8.', 16], step=2) + notes('gs``', 2)

        lh_melody2 = self.transpose(subset(lh_melody, 1, 7), 3, 'semitone')
        lh_melody2[5] = rests(2) + self.scale('d', 'a', [4, '8.', 16], step=2)
        lh_melody2[6] = rests(2) + self.scale('e', 'd`', [8, 8, '8.', 16], step=2)

        self.set_key('cs major')

        rh_harmony2 = self.transpose(subset(rh_harmony, 1, 7), 3, 'semitone')
        add(subset(rh_harmony2[1], 3, 5), 'cs`')
        rh_harmony2[2] = chord('d` fs`', 4) + chord('b d`', '8.') + chord('b d`', 16) + chord(self.arpeggio('cs`', 3), 2)
        add(subset(rh_harmony2[4], 1, 3), 'd`')
        rh_harmony2[5] = subset(rh_harmony2[5], 1, 4)
        remove(subset(rh_harmony2[5], 1, 3), 'fs`')
        add(subset(rh_harmony2[5], 1, 3), 'e`')
        select(rh_harmony2[5], 4)[0][0].dur = 2
        rh_harmony2[6] = chord('gs` b`', 4) + chord('gs` b` cs``', '8.') + chord('b` cs`` fs``', 16) + chord(select(diminished7('gs`', 5, key='gs minor'), 1, 2, 3, 5), 2)

        lh_harmony2 = self.transpose(subset(lh_harmony, 1, 7), 3, 'semitone')
        replace(lh_harmony2[2], 'ds', 'd')
        add(subset(lh_harmony2[3], 1, 3), 'cs')
        add(select(lh_harmony2[3], 1), 'fs,')
        add(select(lh_harmony2[4], 1), 'b')
        remove(select(lh_harmony2[4], 4), 'e')
        lh_harmony2[5] = subset(lh_harmony2[5], 1, 4)
        remove(lh_harmony2[5], 'e`')
        add(select(lh_harmony2[5], 1), 'a,')
        remove(select(lh_harmony2[5], 4), 'fs')
        select(lh_harmony2[5], 4)[0][0].dur = 2
        lh_harmony2[6] = chord('gs b d` fs`', 4) + chord('gs b d` fs`', '8.') + chord('gs b d` fs`', 16) + chord('e gs b d`', 2)

        bold_chords2 = {
            'treble': voices(rh_melody2, rh_harmony2),
            'bass': voices(lh_melody2, lh_harmony2)
        }

        """ bridge """

        bridge_rhythm = [4, '8.', 16]

        def bridge_chords(tone):
            self.set_key(letter(tone) + ' major')
            tones = self.arpeggio(tone, -8)
            return {
                'treble': chords([subset(tones, 1, 4)], bridge_rhythm),
                'bass': chords([subset(tones, 5, 8)], bridge_rhythm)
            }

        def tremble(tone):
            bass_tone = self.transpose(tone, -2, 'octave')
            start_grace = grace(notes([self.transpose(bass_tone, -1, 'semitone'), bass_tone, self.transpose(bass_tone, 2, 'semitone')], 32))
            stop_grace = notes([self.transpose(bass_tone, -1, 'semitone'), bass_tone], 32)

            treble_chord = chord(arpeggio(tone, -4, key=letter(tone) + ' major'), 2)
            if tone == 'b`':
                add(treble_chord, 'a')
            return {
                'treble': treble_chord,
                'bass': start_grace + after_grace(notes(bass_tone, 2, '\\trill'), stop_grace)
            }

        def bridge_motif(tone):
            return join(bridge_chords(tone), tremble(self.transpose(tone, -3)))

        bridge_part_1 = join(bridge_motif('af``'), bridge_motif('gf``'), bridge_motif('e``'))

        key_change = {'treble': self.key_signature, 'bass': self.key_signature}

        bridge_part_2_melody = {
            'treble': 2 * (notes('e`', bridge_rhythm) + self.scale('e`', -4, 8) + self.scale('e`', 4, bridge_rhythm + [2])) + 2 * rests(1),
            'bass': rests(1, 2) + self.scale('e,', -2, 8) + grace(note('ds,', 8)) + self.scale('cs,', -2, 8) + notes(['b,,'] + self.scale('e,', 3), 8) + notes('a,', 2) + self.scale('a,', -4, 8) + self.scale('e,', -4, [8, 8, '8.', 16]) + self.scale('b,,', -4, 8) + notes('e,, ds,, d,,', [4, 4, 1])
        }

        bridge_part_2_harmony = {'treble': [''] * 6, 'bass': [''] * 9}
        bridge_part_2_harmony['treble'][1] = bridge_chords('e`')['treble'] + chords(['fs a b', 'e a', 'ds a'], [4, 8, 8])
        bridge_part_2_harmony['treble'][2] = chords([self.arpeggio('e', 4), 'fs b e`', self.arpeggio('gs', 4)], bridge_rhythm) + chord(select(dominant7('a', 5, key='b major'), 1, 2, 4, 5), 2)
        bridge_part_2_harmony['treble'][3] = remove(deepcopy(bridge_part_2_harmony['treble'][1]), 'a')
        bridge_part_2_harmony['treble'][4] = bridge_part_2_harmony['treble'][2]

        bridge_part_2_harmony['bass'][1] = chords(['b,, b,'], bridge_rhythm)
        bridge_part_2_harmony['bass'][2] = tremble('b`')['bass']
        bridge_part_2_harmony['bass'][3] = chords(['e, b,'], bridge_rhythm)
        bridge_part_2_harmony['bass'][4] = note('b,', 2)
        bridge_part_2_harmony['bass'][5] = notes('b,', bridge_rhythm)
        bridge_part_2_harmony['bass'][6] = tremble('b`')['bass']
        bridge_part_2_harmony['bass'][7] = notes('b,', bridge_rhythm)
        bridge_part_2_harmony['bass'][8] = note('b,', 2)

        bridge_part_2 = {
            'treble': clef('bass') + voices(bridge_part_2_melody['treble'], bridge_part_2_harmony['treble']),
            'bass': voices(bridge_part_2_harmony['bass'], bridge_part_2_melody['bass'])
        }

        bridge = join(bridge_part_1, key_change, bridge_part_2)

        """ decorations """

        name(rh_melody[1], "Bf/d7, Bf")
        name(rh_melody[2], "Af, FD7, Bf")
        name(rh_melody[3], "Efm, Cf")
        name(rh_melody[4], "d7, Df")
        name(rh_melody[5], "EfD7, Cf7")
        name(rh_melody[6], "Gf, Df, d7")
        name(rh_melody[7], "Ef, Ef6, Af")
        name(rh_melody[8], "Gf, DfD7, Gf")

        self.score = join(intro, bold_chords, intro2, bold_chords2, bridge)

    def end_score(self):
        return ('>>\n  \\layout {\n \\context {\n \\Score\n \\override SpacingSpanner.common-shortest-duration =\n #(ly:make-moment 1/15)\n }\n }\n }')


if __name__ == "__main__":
    MarcheFunebre()
