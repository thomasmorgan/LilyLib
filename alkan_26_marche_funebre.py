from piece import Piece
from util import join, subset, select, flatten, rep
from markup import linebreak, pagebreak, clef, grace, after_grace, repeat, voices, time_signature, key_signature
from tones import tonify, letter
from copy import deepcopy
from points import note, notes, rest, rests, chord, chords, dominant7, diminished7, arpeggio, remove, add, merge, replace


class MarcheFunebre(Piece):

    def details(self):
        self.title = "Marche Funebre"
        self.composer = "Charles Valentin Alkan"
        self.opus = "Op. 26"
        self.key = "Ef Minor"
        self.staves[0].extra_text = '\\set Score.connectArpeggios = ##t'

    def subtext(self):
        return '''
            \\layout {
              \\context {
                \\Staff
                \\RemoveEmptyStaves
              }
            }
            \\layout {
              \\context {
                \\Score
                \\consists "Span_arpeggio_engraver"
              }
            }
        '''

    def write_score(self):

        """ Intro """

        def rise(tone):
            return grace(notes([self.transpose(tone, -13, 'semitone'), self.transpose(tone, -1, 'octave'), tone], 32))

        def fall(tone):
            return self.harmonize(note(tone, 8, articulation='.'), -1, 'octave')

        def fall2(tone):
            return note(self.transpose(tone, -1, 'octave'), 8, articulation='.')

        def plink(tone):
            return rise(tone) + fall(tone) + rests(8)

        def plonk(tone):
            return rise(tone) + rep(fall(tone), 3) + rests(8)

        def plonk2(tone):
            return rise(tone) + rep(fall2(tone), 3) + rests(8)

        def plonk3(tone):
            return rise(tone) + rep(fall(tone), 2) + rest(4)

        def plod(tones):
            tones = tonify(tones)
            return rep(plink(tones[0]), 2) + plonk(tones[1])

        plodding = flatten([plod(x) for x in 4 * ['ef ef'] + ['ef f', 'f gf', 'ef f']] + [plonk('f') + plonk2('bf')])
        plodding[3].prefix += '\\stemDown'

        def drone1(tone, interval=-2):
            note = notes(tone, 2)
            chord1 = self.harmonize(note, interval, 'scale')
            chord2 = self.transpose(chord1, -1, 'scale')
            chord3 = self.transpose(chord2, -1, 'semitone')
            return chord1 + chord2 + chord3 + deepcopy(chord2)

        def drone2(tone, interval=-2):
            return self.harmonize(self.scale(tone, -4, 2), interval, 'scale')

        drone_a = drone1('ef`') + drone1('cf`')
        self.set_key('bf minor')
        drone_b = drone2('gf`') + subset(drone1('ef`'), 1, 3) + notes('bf', 2)
        drone_b[0].articulation = ">"

        intro = {
            'treble': repeat(rests(1, 1, 1, 1, 1, 1, 1, 1)),
            'bass': voices(drone_a + drone_b, plodding)
        }

        intro['bass'][0].markup = "Play first repeat one octave lower and \\bold {\\italic {pp}}, second as written and \\bold {\\italic {p}}"
        intro['treble'][0].prefix = '\\grace s16. ' + intro['treble'][0].prefix
        intro['bass'][-1].suffix += linebreak

        # """ Bold Chords """

        self.set_key('ef minor')

        rh_melody = [[]] * 9
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

        rh_harmony = [[]] * 9
        rh_harmony[1] = flatten([chord(diminished7('d`', note.tone, key='d minor'), note.dur) for note in rh_melody[1]])
        rh_harmony[2] = chord('c` ef`', 4) + chord('a c`', '8.') + chord('a c`', 16) + chord('bf d`', 2)
        rh_harmony[3] = flatten([chord(self.arpeggio('bf', 'gf`'), note.dur) for note in subset(rh_melody[3], 1, 3)]) + chord(arpeggio('cf`', 'gf`', key='cf major'), 2)
        rh_harmony[4] = chord('df` f`', 4) + flatten([chord('df` f` af`', d) for d in ['8.', 16, 2]])
        rh_harmony[5] = flatten([chord(self.arpeggio('ef`', 'bf`'), note.dur) for note in rh_melody[5]])
        remove(select(rh_harmony[5], 5), 'bf`')
        rh_harmony[6] = chord('df` gf`', 4) + chord('df` f`', 4) + chord('d` f` af`', 2)
        rh_harmony[7] = deepcopy(subset(rh_harmony[5], 1, 4)) + chord('ef` af`', 8)
        rh_harmony[8] = notes('gf`', 4) + chord('df` f`', 4) + notes('df`', 2)

        lh_harmony = self.transpose(rh_harmony, -1, 'octave')
        add(subset(lh_harmony[1], 1, 4), 'bf,')
        add(lh_harmony[2], 'bf,')
        remove(lh_harmony[2], 'a,')
        lh_harmony[3] = flatten([chord('ef gf', dur=c.dur) for c in rh_harmony[3]])
        add(subset(lh_harmony[4], 1, 3), 'af cf`')
        remove(select(lh_harmony[4], 4), 'df')
        add(subset(lh_harmony[5], 1, 3), 'df`')
        add(subset(lh_harmony[5], 4, 5), 'cf')
        lh_harmony[7] = deepcopy(subset(lh_harmony[5], 1, 4)) + chord('cf ef af', 8)
        remove(lh_harmony[7], 'df`')
        lh_harmony[8] = chord('df gf', 4) + chord('df f', 4) + chord('gf, df', 2)

        rh_harmony[1][0].dynamics = "rfz"
        rh_harmony[3][0].dynamics = "f"
        rh_harmony[6][2].articulation = ">"
        lh_harmony[6][2].articulation = ">"
        rh_harmony[7][0].dynamics = "p"

        bold_chords = {
            'treble': voices(rh_melody, rh_harmony),
            'bass': voices(lh_melody, lh_harmony)
        }

        # """ Intro again """

        self.set_key('fs minor')
        shifted_bass = self.transpose(plodding[0:119], 3, 'semitone') + time_signature('2/4', plonk('gs'), '4/4')
        shifted_bass[0].prefix = self.key_signature + shifted_bass[0].prefix

        drone_c = drone1('fs`', 5) + drone1('d`', 5)
        add(drone_c, 'fs`')
        drone_c[0].prefix = self.key_signature + '\\grace s16.'
        drone_c[0].dynamics = "p"

        self.set_key('cs minor')
        drone_d = merge(drone2('a`', 5) + drone1('fs`', 5)[0:3], notes('cs`` cs`` bs` a` a` gs` fs`', 2))
        drone_d[0].articulation = ">"
        drone_d[-1].suffix += linebreak

        intro2 = {
            'treble': drone_c + drone_d,
            'bass': shifted_bass
        }

        # """ Bold Chords again """

        self.set_key('fs minor')

        rh_melody2 = self.transpose(rh_melody[0:7], 3, 'semitone')
        rh_melody2[4] = note('gs`', 8) + self.scale('b`', 'e``', [8, '8.', 16, 2])
        rh_melody2[6] = self.scale('b`', 'a``', [8, 8, '8.', 16], step=2) + note('gs``', 2)

        lh_melody2 = self.transpose(lh_melody[0:7], 3, 'semitone')
        lh_melody2[5] = rest(2) + self.scale('d', 'a', [4, '8.', 16], step=2)
        lh_melody2[6] = rest(2) + self.scale('e', 'd`', [8, 8, '8.', 16], step=2)

        self.set_key('cs major')

        rh_harmony2 = self.transpose(rh_harmony[0:7], 3, 'semitone')
        add(subset(rh_harmony2[1], 3, 5), 'cs`')
        rh_harmony2[2] = chord('d` fs`', 4) + chord('b d`', '8.') + chord('b d`', 16) + chord(self.arpeggio('cs`', 3), 2)
        rh_harmony2[5] = subset(rh_harmony2[5], 1, 4)
        remove(subset(rh_harmony2[5], 1, 3), 'fs`')
        add(subset(rh_harmony2[5], 1, 3), 'e`')
        rh_harmony2[5][3].dur = 2
        rh_harmony2[6] = chord('gs` b`', 4) + chord('gs` b` cs``', '8.') + chord('b` cs`` fs``', 16) + chord(select(diminished7('gs`', 5, key='gs minor'), 1, 2, 3, 5), 2)

        lh_harmony2 = self.transpose(lh_harmony[0:7], 3, 'semitone')
        replace(lh_harmony2[2], 'ds', 'd')
        add(subset(lh_harmony2[3], 1, 3), 'cs')
        add(select(lh_harmony2[3], 1), 'fs,')
        add(select(lh_harmony2[4], 1), 'b')
        remove(select(lh_harmony2[4], 4), 'e')
        lh_harmony2[5] = subset(lh_harmony2[5], 1, 3) + chord('a cs`', 2)
        remove(lh_harmony2[5], 'e`')
        add(select(lh_harmony2[5], 1), 'a,')
        lh_harmony2[6] = chord('gs b d` fs`', 4) + chord('gs b d` fs`', '8.') + chord('gs b d` fs`', 16) + chord('e gs b d`', 2)

        rh_harmony2[5][0].dynamics = "cresc"
        rh_harmony2[5][1].dynamics = "!"
        lh_melody2[6][1].suffix = "^\\>"
        lh_melody2[6][4].suffix = "\\!"

        bold_chords2 = {
            'treble': voices(rh_melody2, rh_harmony2),
            'bass': voices(lh_melody2, lh_harmony2)
        }

        # """ bridge """

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
                'bass': start_grace + after_grace(note(bass_tone, 2, ornamentation='trill'), stop_grace)
            }

        def bridge_motif(tone):
            return join(bridge_chords(tone), tremble(self.transpose(tone, -3)))

        bridge_part_1 = join(bridge_motif('af``'), bridge_motif('gf``'), bridge_motif('e``'))

        def bridge_grace(passage):
            return subset(passage, 1, 2) + grace(note(passage[1].tone, 16)) + subset(passage, 3, len(passage))

        bridge_rhythm4 = [8, 8, '8.', 16]

        bridge_part_2_melody = {
            'treble': rep(notes('e`', bridge_rhythm) + self.scale('e`', -4, 8) + self.scale('e`', 4, bridge_rhythm + [2]), 2) + rep(rests(1), 2),
            'bass': rests(1, 2) + bridge_grace(self.scale('e,', -4, 8)) + notes(['b,,'] + self.scale('e,', 3), 8) + note('a,', 2) + self.scale('a,', -4, 8) + self.scale('e,', -4, bridge_rhythm4) + self.scale('b,,', -4, 8) + notes('e,, ds,, d,,', [4, 4, 1])
        }

        bridge_part_2_harmony = {'treble': [[]] * 6, 'bass': [[]] * 9}
        bridge_part_2_harmony['treble'][1] = bridge_chords('e`')['treble'] + chords(['fs a b', 'e a', 'ds a'], [4, 8, 8])
        bridge_part_2_harmony['treble'][2] = chords([self.arpeggio('e', 4), 'fs b e`', self.arpeggio('gs', 4)], bridge_rhythm) + chord(select(dominant7('a', 5, key='b major'), 1, 2, 4, 5), 2)
        bridge_part_2_harmony['treble'][3] = replace(deepcopy(bridge_part_2_harmony['treble'][1]), 'a', 'b')
        bridge_part_2_harmony['treble'][4] = deepcopy(bridge_part_2_harmony['treble'][2])

        bridge_part_2_harmony['bass'][1] = chords(['b,, b,'], bridge_rhythm)
        bridge_part_2_harmony['bass'][2] = tremble('b`')['bass']
        bridge_part_2_harmony['bass'][3] = chords(['e, b,'], bridge_rhythm)
        bridge_part_2_harmony['bass'][4] = note('b,', 2)
        bridge_part_2_harmony['bass'][5] = notes('b,', bridge_rhythm)
        bridge_part_2_harmony['bass'][6] = tremble('b`')['bass']
        bridge_part_2_harmony['bass'][7] = notes('b,', bridge_rhythm)
        bridge_part_2_harmony['bass'][8] = note('b,', 2)

        bridge_part_2 = {
            'treble': clef('bass', voices(bridge_part_2_melody['treble'], bridge_part_2_harmony['treble'])),
            'bass': voices(bridge_part_2_harmony['bass'], bridge_part_2_melody['bass'])
        }
        bridge_part_2_melody['bass'][-1].suffix += linebreak

        bridge_part_1['treble'][0].dynamics = "p"
        bridge_part_2_harmony['treble'][1][0].dynamics = "p"

        bridge_part_2_melody['treble'][0].prefix = self.key_signature + bridge_part_2_melody['treble'][0].prefix
        bridge_part_2_harmony['bass'][1][0].prefix = self.key_signature + bridge_part_2_harmony['bass'][1][0].prefix

        bridge_part_2['bass'][-1].suffix += linebreak

        bridge = join(bridge_part_1, bridge_part_2)

        # """ Intro again again """

        self.set_key('Ef Minor')
        intro3_treble = drone1('ef') + drone1('cf')
        intro3_bass = rep(plod('ef, ef,'), 4)

        self.set_key('ef harmonic')
        mini_motif = self.harmonize(notes('bf', ['4.', 8]) + self.scale('bf', -4, 4), -2)
        intro3_treble += (self.harmonize(notes('gf ef af', 2) + grace(note('gf', 16)) + note('f', 2), -2)
                          + mini_motif + chord('d cf', 2) + deepcopy(mini_motif) + note('ef', 2) + rep(chord('d af cf`', 2, articulation='>') + note('ef', 2), 2) + chord('d af cf`', 1, articulation='>'))
        intro3_bass += (plod('ef, af,') + plod('f, bf,') + plod('gf, cf') + plod('bf, af,')
                        + rep(plink('gf,'), 2) + plonk3('cf') + plonk3('bf,') + plonk('ef,')
                        + rest(2) + rep(plink('ef,'), 2) + rest(2) + plonk('ef,') + rest(1))

        intro3_treble[0].suffix += "^\\pp"
        intro3_treble[8].articulation = '>'
        intro3_bass[68].markup = '\\italic{poco cresc.}'
        intro3_treble[10].articulation = '>'
        intro3_treble[13].articulation = '>'
        intro3_treble[19].articulation = '>'
        intro3_treble[20].markup = '\\italic {dim.}'
        intro3_treble[22].suffix += '^\\>'
        intro3_treble[26].dynamics = 'pp'
        intro3_bass[-1].suffix += linebreak + pagebreak

        intro3 = {
            'treble': clef('treble', rest(1, prefix=self.key_signature + ' \\grace s16.')) + rest(1) * 12,
            'bass': key_signature(self.key, voices(intro3_treble, intro3_bass))
        }

        # """ Cascade """

        self.set_key('ef major')

        def set_cascade_melody(melody, bars=8, is_repeated=False, end=False, key=False):
            section = {
                'treble': voices(melody, rep(self.scale('ef`', -4, 8), bars)),
                'bass': voices(rep(self.scale('g', -4, 8), bars), rep(note('ef,', 2, articulation='>'), bars))
            }
            if key:
                section['treble'] = key_signature(self.key, section['treble'])
                section['bass'] = key_signature(self.key, section['bass'])
            if is_repeated:
                section['bass'] = repeat(section['bass'])
            if end:
                section['bass'][-1].suffix += pagebreak
            else:
                section['bass'][-1].suffix += linebreak
            return section

        cascade_melody_1a = notes('g` af` g` af` bf` g` af`', [4, 4, 4, 8, 8, 4, 4])
        cascade_melody_1 = cascade_melody_1a + notes('g` f`', 4) + deepcopy(cascade_melody_1a) + note('g`', 2)
        cascade_meldody_2a = self.arpeggio('g`', 3, 4)
        cascade_meldody_2b = deepcopy(cascade_meldody_2a) + notes('bf` af`', 8)
        cascade_melody_2 = cascade_meldody_2b + cascade_meldody_2a + note('bf`', 4) + deepcopy(cascade_meldody_2b) + notes('g` af` bf` g`', [4, 8, 8, '4.']) + rest(8)
        cascade_melody_3a = notes('ef`` c`` d`` c`` g` g`', [4, 8, 8, 4, 4, 2])
        cascade_melody_3 = notes('c`` g`', 4) + cascade_melody_3a + notes('g` c`` d``', [4, 8, 8]) + deepcopy(cascade_melody_3a)
        cascade_melody_4 = deepcopy(subset(cascade_melody_1, 1, 14)) + notes('g` f` ef` g`', [4, 8, 8, 2])
        cascade_melody_5 = self.arpeggio('g`', 3, 4) + note('c``', 8) + self.scale('d``', -5, [8, 4, 8, 8, 2]) + note('g`', 4) + 2 * self.scale('c``', 3, [8, 8, 4]) + notes('g` f` g`', [8, 8, 2])
        cascade_melody_6 = deepcopy(cascade_melody_4)

        cascade_melody_1[0].dynamics = "f"
        cascade_melody_2[0].dynamics = "f"
        cascade_melody_3[0].dynamics = "ff"
        cascade_melody_3[16].dynamics = ">"
        cascade_melody_4[0].dynamics = "p"
        cascade_melody_5[0].dynamics = "ff"
        cascade_melody_5[18].dynamics = ">"
        cascade_melody_6[0].dynamics = "pp"

        cascade = join(set_cascade_melody(cascade_melody_1, is_repeated=True, key=True),
                       set_cascade_melody(cascade_melody_2, is_repeated=True),
                       set_cascade_melody(cascade_melody_3),
                       set_cascade_melody(cascade_melody_4),
                       set_cascade_melody(cascade_melody_5),
                       set_cascade_melody(cascade_melody_6, end=True)
                       )

        # """ Intro 4 """

        self.set_key('ef minor')

        intro4 = {
            'treble': key_signature(self.key, rep(rest(1), 8)),
            'bass': key_signature(self.key, voices(
                deepcopy(drone_a + drone_b),
                plodding
            ))
        }

        intro4['bass'][-1].suffix += linebreak
        intro4['bass'][0].markup += "Play left hand one octave lower"
        intro4['bass'][16].suffix += "^\\p"

        # """ bold chords 3 """

        rh_melody3 = deepcopy(subset(rh_melody, 1, 5)) + self.transpose(subset(rh_melody, 4, 5), 2)

        rh_harmony3 = deepcopy(rh_harmony[0:7])
        add(rh_harmony3[1], 'bf')
        rh_harmony3[2] = chords(['bf cf` ef`', 'af cf`', 'af cf`', 'af bf d`'], [4, '8.', 16, 2])
        rh_harmony3[5] = subset(rh_harmony3[5], 1, 3) + chord('ef` gf` bf`', 2)
        rh_harmony3[6] = self.transpose(rh_harmony3[4], 2)
        add(select(rh_harmony3[6], 3), 'ef``')
        add(select(rh_harmony3[6], 4), 'df``')

        lh_melody3 = deepcopy(subset(lh_melody, 1, 4)) + [rest(2) + self.scale('bf,', 'af', [8, 8, '8.', 16], step=2)]
        lh_melody3 += [self.transpose(lh_melody3[3], 2), self.transpose(lh_melody3[4], 2)]

        lh_harmony3 = deepcopy(lh_harmony[0:7])
        add(lh_harmony3[1], 'bf,')
        add(subset(lh_harmony3[3], 1, 3), 'bf,')
        add(select(lh_harmony3[3], 1), 'ef,')
        add(select(lh_harmony3[4], 1), 'f,')
        add(select(lh_harmony3[4], 4), 'df')
        lh_harmony3[5] = subset(lh_harmony3[5], 1, 3) + chord('ef gf bf', 2)
        add(select(lh_harmony3[5], 1), 'gf,')
        lh_harmony3[6] = self.transpose(lh_harmony3[4], 2)
        add(select(lh_harmony3[6], 4), 'df`')

        rh_harmony3[5][0].dynamics = "cresc"
        rh_harmony3[5][1].dynamics = "!"
        lh_melody3[6][1].suffix += "^\\<"
        lh_melody3[6][4].dynamics = "!"

        bold_chords3 = {
            'treble': voices(rh_melody3, rh_harmony3),
            'bass': voices(lh_melody3, lh_harmony3)
        }

        # """ bridge 2 """

        bridge2_part_1 = join(bridge_motif('gf``'), bridge_motif('f``'), bridge_motif('e``'))

        bridge2_part_2_melody = {
            'treble': key_signature(self.key, subset(bridge_part_2_melody['treble'], 1, 14) + bridge_grace(self.scale('e`', -4, bridge_rhythm4)) + note('b', 8) + self.scale('e`', 3, 8) + note('a`', 2) + rests(1, 1)),
            'bass': key_signature(self.key, rests(1, 2) + bridge_grace(self.scale('e,', -4, bridge_rhythm4)) + notes(['b,,'] + self.scale('e,', 3), 8) + bridge_grace(self.scale('e', -8, bridge_rhythm4 + [8, 8, 8, 8])) + bridge_grace(self.scale('e,', -8, bridge_rhythm4 + [8, 8, 8, 8])) + notes('e,, ds,, d,,', [4, 4, 1]))
        }

        bridge2_part_2_harmony = deepcopy(bridge_part_2_harmony)
        bridge2_part_2_harmony['treble'][3] = bridge_chords('e`')['treble'] + chord('fs b', 2)
        bridge2_part_2_harmony['treble'][4] = chords(['e b', 'fs b e`', 'gs b e`', 'a b fs`'], [4, 8, 8, 2])
        bridge2_part_2_harmony['bass'][6] = note('a,', 2)

        bridge2_part_2 = {
            'treble': clef('bass', voices(bridge2_part_2_melody['treble'], bridge2_part_2_harmony['treble'])),
            'bass': voices(bridge2_part_2_harmony['bass'], bridge2_part_2_melody['bass'])
        }

        bridge2_part_1['treble'][0].dynamics = "p"
        bridge2_part_2['bass'][-1].suffix += linebreak

        bridge2 = join(bridge2_part_1, bridge2_part_2)

        # """ outro """

        self.set_key('ef minor')

        outro = {
            'treble': key_signature(self.key, rep(rest(1), 15)),
            'bass': key_signature(self.key, deepcopy(voices(intro3_treble[0:19] + chord('c ef', 2) + intro3_treble[13:17] + rest(2, ornamentation='fermata') + intro3_treble[17:19] + rest(2, ornamentation='fermata') + intro3_treble[26:31] + rep(chord('d af cf`', 2, articulation=">"), 2) + chord('d af cf`', 1, articulation=">"),
                                                            intro3_bass[0:151] + rest(4) + rest(2) + plonk3('bf,') + rest(2) + rep(plink('ef,'), 2) + rest(2) + plonk('ef,') + rest(2) + rep(plink('ef,'), 2) + rests(1, 1))))
        }

        outro['treble'][0].prefix += '\\grace s16.'
        outro['treble'][-1].suffix = linebreak

        outro['bass'][13] = chord(outro['bass'][13].tones, outro['bass'][13].dur, articulation='>')
        outro['bass'][17].dynamics = ''
        outro['bass'][20].suffix = '^\\pp'
        outro['bass'][20].articulation = ''
        outro['bass'][28].suffix = '^\\ppp'
        outro['bass'][28].dynamics = ''
        outro['bass'][34].markdown = '\\italic { dim. }'
        outro['bass'][35].markdown += '\\italic { dim. }'
        outro['bass'][104].markup = ''

        # """ outro 2 """

        self.set_key('ef major')

        outro2 = {
            'treble': key_signature(self.key, clef('bass', voices(chords(['ef g bf'], [2, 4]) + chord('ef af bf', 4) + chords(['ef g bf'], [2, 2]),
                                                                  rep(self.scale('g', -4, 8), 4)))) + chord('ef g bf', 1, ornamentation='arpeggio'),
            'bass': key_signature(self.key, rep(voices(self.scale('ef', -4, 8), chord('ef, bf,', 2)), 4)) + chord('ef,, bf,, ef, bf,', 1, ornamentation='arpeggio')
        }

        outro2['treble'][0].dynamics = 'mf'
        outro2['treble'][1].markdown = '\\italic { dim. }'
        outro2['treble'][3].markdown = '\\italic { rall. }'
        outro2['treble'][4].dynamics = 'pp'
        outro2['treble'][-1].dynamics = 'ppp'

        self.score = join(intro, bold_chords, intro2, bold_chords2, bridge, intro3, cascade, intro4, bold_chords3, bridge2, outro, outro2)

    def end_score(self):
        return ('>>\n  \\layout {\n \\context {\n \\Score\n \\override SpacingSpanner.common-shortest-duration =\n #(ly:make-moment 1/14)\n }\n }\n }')


if __name__ == "__main__":
    MarcheFunebre()
