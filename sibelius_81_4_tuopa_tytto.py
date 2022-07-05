from piece import Piece
from staves import Bass, Dynamics
from points import chord, tied_chord, notes, rests, chords
from markup import slur, voices, triplets
from util import rep, select, flatten, subset
from tones import tonify


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

    def write_score(self):

        #########
        # part 1
        #########

        treble_1 = [chord('c, g,', 2)] + tied_chord('c, g,', [2, 2, 2])
        bass_1 = (
            slur(rep(notes('e, e c e', 32), 5) +
                 rep(notes('e` g e g', 32), 3)) +
            slur(rep(notes('e e` c` e`', 32), 5) +
                 rep(notes('e`` g` e` g`', 32), 2) +
                 notes('d`` e` d` e`', 32)))
        select(bass_1, 1).phrasing = '_('
        select(bass_1, 33).phrasing = '_('
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

        treble_3 = (
            blend(subset(melody, 1, 4), 'fs` c` fs`') +
            blend(subset(melody, 5, 8), 'e` c` e`') +
            blend(subset(melody, 9, 12), 'fs` c` fs`') +
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
        select(treble_3, 66).prefix += '\\change Staff = "bass"\n'
        select(treble_3, 102).prefix += '\\change Staff = "bass"\n'
        select(treble_3, 118).prefix += '\\change Staff = "bass"\n'
        select(treble_3, 133).prefix += '\\change Staff = "treble"\n'

        bass_3 = (
            notes(melody, 8) + [chord('c, g, c g', 2, suffix='^>')] +
            rests(2, 2, prefix='%{ spacer %}'))
        for i in [1, 3, 5, 9, 11]:
            select(bass_3, i).phrasing += '('
        for i in [2, 4, 7, 10, 12]:
            select(bass_3, i).phrasing += ')'

        #########
        # combine
        #########

        self.score = {
            'treble': treble_1 + treble_2 + treble_3,
            'dynamics': [],
            'bass': bass_1 + bass_2 + bass_3,
            'pedal': []
        }


if __name__ == "__main__":
    TuopaTytto()
