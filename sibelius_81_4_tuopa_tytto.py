from piece import Piece
from staves import Bass, Dynamics
from points import chord, tied_chord, notes, rests, chords
from markup import slur, voices, triplets, clef, italic
from util import rep, select, flatten, subset
from tones import tonify
from copy import deepcopy


class TuopaTytto(Piece):

    def details(self):
        self.title = "Tuopa tyttö, kaunis tyttö, kanteletta soittaa"
        self.composer = "Jean Sibelius"
        self.date = "1903"
        self.mutopiacomposer = "SibeliusJ"
        self.mutopiainstrument = "piano"
        self.source = "Breitkopf und Härtel, 1906"
        self.style = "Romantic"
        self.license = "Creative Commons Attribution-ShareAlike 4.0"
        self.maintainer = "Thomas Morgan"
        self.mantainer_email = "thomas.j.h.morgan@gmail.com"
        self.opus = "JS 81, No. 4"
        self.auto_add_bars = True
        self.key = 'd minor'
        self.tempo = ("2/4")
        self.beaming = ('\\set Timing.baseMoment = #(ly:make-moment 1/8)\n'
                        '\\set Timing.beatStructure = 1, 1, 1, 1')
        self.tempo_name = 'Moderato'
        self.staves = [
            Bass(name='treble'),
            Dynamics(),
            Bass(),
            Dynamics('pedal')]

    def subtext(self):
        return '\\paper { #(set-paper-size "letter")}\n'

    def write_score(self):

        #########
        # part 1
        #########

        treble_1 = [chord('c, g,', 2)] + tied_chord('c, g,', [2, 2, 2])
        select(treble_1, 2).phrasing = '^~'
        select(treble_1, 3).phrasing = '^~'

        bass_1 = (
            slur(rep(notes('e, e c e', 32), 5) +
                 rep(notes('e` g e g', 32), 3)) +
            slur(rep(notes('e e` c` e`', 32), 5) +
                 rep(notes('e`` g` e` g`', 32), 2) +
                 notes('d`` e` d` e`', 32)))
        select(bass_1, 1).phrasing = '_('
        select(bass_1, 21).prefix += '\\stemUp '
        select(bass_1, 33).phrasing = '_('
        select(bass_1, 33).prefix = '\\stemNeutral '
        select(bass_1, 53).prefix += (
            '\\change Staff = "treble" \\clef "treble" ')

        #########
        # part 2
        #########

        treble_2 = (
            rep(notes('c`` e` c` e`', 32), 12) +
            rep(notes('c`` fs` c` fs`', 32), 8))

        bass_2 = (
            rep(slur(notes('bf a g', 8)) + notes('a', 8), 2) +
            slur(notes('bf a', 8)) + slur(notes('bf d`', 8)) +
            notes('a', 4, articulation='-') +
            tied_chord('c, a, fs a', [4, 2], suffix='^>'))
        select(bass_2, 1).prefix += (
            '\\change Staff = "bass"\n'
            '\\set Staff.baseMoment = #(ly:make-moment 1/4)\n'
            '\\set Staff.beatStructure = 1, 1\n')

        #########
        # part 3
        #########

        melody = tonify('bf a d` c` bf a g a bf a bf d`')

        def blend(melody, backing):
            melody = self.transpose(notes(melody, 32), 1, 'octave')
            return flatten([[note] + notes(backing, 32) for note in melody])

        treble_3 = (
            blend(subset(melody, 1, 4), 'fs` c` fs`') +
            blend(subset(melody, 5, 8), 'e` c` e`') +
            blend(subset(melody, 9, 12), 'fs` c` fs`'))

        bass_3 = notes(melody, 8)
        for i in [1, 3, 5, 9, 11]:
            select(bass_3, i).phrasing += '('
        for i in [2, 4, 7, 10, 12]:
            select(bass_3, i).phrasing += ')'

        #########
        # part 4
        #########

        def fast_chords(chord_list, alt=False):
            output = []
            for c in chord_list:
                if alt:
                    output += rests(32, prefix='%{ spacer %}')
                output += (
                    [chord(c, 32, phrasing='[')] +
                    rests(32, prefix='%{ spacer %}') +
                    [chord(c, 32, phrasing=']')])
                if not alt:
                    output += rests(32, prefix='%{ spacer %}')
            return output

        def trio(tones, *args):
            melody = triplets(notes(tones, 32), omit_number=True)
            select(melody, 1).phrasing = '['
            select(melody, 3).phrasing = ']'
            if "up" in args:
                select(melody, 1).prefix = (
                    '\\stemUp ' + select(melody, 1).prefix)
            else:
                select(melody, 1).prefix = (
                    '\\stemDown ' + select(melody, 1).prefix)
            return melody

        treble_4 = (
            voices(
                rests(8) + fast_chords(
                    ['e`` g``', 'c`` e``', 'g` c``', 'e` g`', 'c` e`',
                     'g c`', 'e g', 'c e'], alt=True),
                [chord('c` g`', 2)] + rests(2, 8, prefix='%{ spacer %}'),
                rests(8, prefix='%{ spacer %} \\stemDown ') +
                fast_chords(
                    ['c`` fs``', 'g` ds``', 'e` b`', 'c` fs`', 'g ds`',
                     'e b', 'c fs', 'g, ds'])) +
            slur(trio('c, g, c', 32, "down") + trio('e g c`', 32, "up") +
                 trio('g, c e', 32, "down") + trio('g c` e`', 32, "up") +
                 trio('c e g', 32, "down") + trio('c` e` g`', 32, "up")))
        select(treble_4, 18).prefix += '\\change Staff = "bass"\n'
        select(treble_4, 54).prefix += '\\change Staff = "bass"\n'
        select(treble_4, 70).prefix += '\\change Staff = "bass"\n'
        select(treble_4, 85).prefix += '\\change Staff = "treble"\n'

        bass_4 = (
            [chord('c, g, c g', 2, suffix='^>')] +
            rests(2, 2, prefix='%{ spacer %}'))

        #########
        # part 5
        #########

        melody = tonify('af g f g af g f g af g af c`')

        treble_5 = blend(melody, 'd` c` d`')

        bass_5 = notes(melody, 8)
        for i in [1, 5, 9, 11]:
            select(bass_5, i).phrasing += '('
        for i in [3, 7, 10, 12]:
            select(bass_5, i).phrasing += ')'

        #########
        # part 6
        #########

        treble_6 = deepcopy(treble_4)
        bass_6 = deepcopy(bass_4)
        select(treble_6, 18).prefix = '%{ spacer %} '
        select(treble_6, 54).prefix = ''
        select(treble_6, 22).prefix += '\\change Staff = "bass"\n'
        select(treble_6, 58).prefix += '\\change Staff = "bass"\n'

        #########
        # part 7
        #########

        melody = tonify('bf a d` c` bf a')

        treble_7 = (
            blend(melody, 'fs` c` fs`') + [chord('c` g`', 8)] +
            rests(8, prefix=' %{ spacer %} '))
        bass_7 = (
            notes(melody, 8, articulation='.') +
            notes('g', 8, articulation='>') +
            slur(notes('c, g, c e g c` e` g`', 64)))
        for i in [1, 3, 5]:
            select(bass_7, i).phrasing += '('
            select(bass_7, i+1).phrasing += ')'
        select(bass_7, 8).prefix += '\\stemDown '
        select(bass_7, 8).phrasing += '['
        select(bass_7, 11).phrasing += ']'
        select(bass_7, 12).phrasing += '['
        select(bass_7, 12).prefix += '\\stemUp '
        select(bass_7, 13).prefix += '\\change Staff = "treble" '
        select(bass_7, 15).phrasing += ']'
        select(bass_7, 15).suffix += ' \\change Staff = "bass" \\stemNeutral '

        treble_7 = rep(treble_7, 2)
        bass_7 = rep(bass_7, 2)

        for i in [16, 17, 18, 19, 20]:
            select(bass_7, i).articulation = ''
        select(bass_7, 22).add('c')

        #########
        # part 8
        #########

        melody = tonify('bf a d` c` bf a g a bf a bf d`')

        treble_8 = (
            blend(subset(melody, 1, 4), 'fs` c` fs`') +
            blend(subset(melody, 5, 8), 'e` c` e`') +
            notes('bf` fs` c` fs` c`` fs` c` fs`', 32) +
            notes('d`` bf` d` bf` f`` bf` f` bf`', 32))

        bass_8 = notes(melody, 8, articulation='-')

        #########
        # part 9
        #########

        treble_9 = (
            [chord('a` c`` f`` a``', 8)] +
            voices(
                fast_chords(['c`` f``', 'a` c``', 'f` a`', 'c` f`',
                             'a c`', 'f a', 'c f'], alt=True),
                fast_chords(['a` e``', 'f` b`', 'c` gs`', 'a e`',
                             'f b', 'c gs', 'a, e'])))
        select(treble_9, 18).prefix += '\\change Staff = "bass" '
        select(treble_9, 46).prefix += '\\change Staff = "bass" '
        bass_9 = [chord('c a c`', 8)] + rests(8, 4, 2, prefix='%{ spacer %}')

        #########
        # part 10
        #########

        treble_10 = (
            rests(2, prefix='%{ spacer %}') +
            clef('bass', [chord('f,, c,', 2, articulation='>')]) +
            tied_chord('f,, c,', [2, 2]))
        bass_10 = (
            voices(notes('c', 2),
                   rep(notes('a,, a, f, a,', 32), 4)) +
            rep(notes('a,, a, f, a,', 32), 10) +
            notes('a,,', 4))

        #########
        # dynamics
        #########

        dynamics = (
            rests(2, dynamics='mp') +
            rests(4) + rests(4, markup=italic('cresc.')) +
            rests(2, 2) + rests(2, markup='\\dynamic{f} \\italic{ marcato}') +
            rests(2, 2, 2, 2, 2, 2, 2) + rests(2, dynamics='f') +
            rests(4) + rests(4, dynamics='>') + rests(8, dynamics='!') +
            rests(8, 4) + rests(2, dynamics='mf') + rests(2, 2) +
            rests(2, dynamics='f') + rests(2, 2) + rests(2, dynamics='mf') +
            rests(4, 8, 16, 64) + rests('32.', dynamics='<') +
            rests(2, dynamics='f') + rests(2, dynamics='f') +
            rests(2, markup='\\italic{più } \\dynamic{f}') +
            rests(32) + rests('16.', markup=italic('cresc.')) + rests(8, 4) +
            rests(2) + rests(2, dynamics='ff') + rests(4) +
            rests(4, markup=italic('dim. molto')) + rests(2, 2) +
            rests('4.', dynamics='p') + rests(8, markup=italic('dim.')) +
            rests(2)
        )

        #########
        # pedal
        #########

        on = '\\sustainOn '
        off = '\\sustainOff '

        pedal = (
            rests(2, suffix=on) + rests(2, 2, '4.') + rests(8, suffix=off) +
            rests(2, 2, 2, 4) + rests(4, suffix=on) +
            rests(4, 8, 16, 32, 64, 128) + rests(128, suffix=off) +
            rests(2, 2, 2) + rests(2, suffix=on) +
            rests(2, 2, 2, 2, 2, 2, 2, 2, 2, 4) + rests(4, suffix=on) +
            rests(2, 4) + rests(4, 4, 4, suffix=on) +
            rep(rests(8, suffix=on) + rests(8, suffix=off), 4) +
            rests(2, suffix=on) + rests(2) +
            rests(4, 8, 16, 32, 64, 128) + rests(128, suffix=off) +
            rests(2, suffix=on) + rests(2) +
            rests(4, 8, 16, 32, 64, 128) + rests(128, suffix=off)
        )

        #########
        # markup
        #########

        select(treble_4, 71).phrasing = '^\\<'
        select(treble_4, 85).dynamics = '!'

        #########
        # combine
        #########

        self.score = {
            'treble': (
                treble_1 + treble_2 + treble_3 + treble_4 + treble_5 +
                treble_6 + treble_7 + treble_8 + treble_9 + treble_10),
            'dynamics': dynamics,
            'bass': (
                bass_1 + bass_2 + bass_3 + bass_4 + bass_5 + bass_6 +
                bass_7 + bass_8 + bass_9 + bass_10),
            'pedal': pedal
        }


if __name__ == "__main__":
    TuopaTytto()
