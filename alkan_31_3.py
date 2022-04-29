from piece import Piece
from points import (notes, tied_note, chords, rests, add, merge, scale,
                    transpose)
from staves import Treble, Super, Bass
from markup import voices, signe, italic, linebreak
from util import select, omit, flatten, subset, join, pattern


pushNC = """pushNC =
\\once \\override NoteColumn.X-offset =
  #(lambda (grob)
    (let* ((p-c (ly:grob-parent grob X))
           (p-c-elts (ly:grob-object p-c 'elements))
           (stems
             (if (ly:grob-array? p-c-elts)
                 (filter
                   (lambda (elt)(grob::has-interface elt 'stem-interface))
                   (ly:grob-array->list p-c-elts))
                 #f))
           (stems-x-exts
             (if stems
                 (map
                   (lambda (stem)
                     (ly:grob-extent
                       stem
                       (ly:grob-common-refpoint grob stem X)
                       X))
                   stems)
                 '()))
           (sane-ext
             (filter interval-sane? stems-x-exts))
           (cars (map car sane-ext)))
    (if (pair? cars)
        (abs (- (apply max cars)  (apply min cars)))
        0)))\n"""


class GenreAncien(Piece):

    def details(self):
        self.title = "No. 3"
        self.subtitle = "Dans le genre ancien"
        self.composer = "Charles-Valentin Alkan"
        self.date = "1847"
        self.mutopiacomposer = "AlkanCV"
        self.mutopiainstrument = "piano"
        self.source = "Bardus, 1847"
        self.style = "Romantic"
        self.license = "Creative Commons Attribution-ShareAlike 4.0"
        self.maintainer = "Thomas Morgan"
        self.mantainer_email = "thomas.j.h.morgan@gmail.com"
        self.opus = "Op. 31, No. 3"
        self.auto_add_bars = True
        self.key = 'bf minor'
        self.improvements = False
        if self.improvements:
            self.staves = [
                Treble("treble"),
                Super("middle"),
                Bass("bass")]

    def subtext(self):
        text = (
          pushNC +
          '#(set-default-paper-size "letter")\n'
          "\\layout{\\context{\\PianoStaff \\consists #Span_stem_engraver }}\n"
          '\\layout { \\context { \\Voice '
          '\\consists "Horizontal_bracket_engraver" } }\n'
          "\\layout { \\context { \\Score \\override "
          "SpacingSpanner.base-shortest-duration = #(ly:make-moment 1/25)}}\n")
        if not self.improvements:
            text += (
              "\\paper { system-system-spacing = #'((basic-distance . 12) "
              "(minimum-distance . 8) (padding . 12) (stretchability . 60))}\n"
              "\\layout { \\context { \\PianoStaff \\override "
              "StaffGrouper.staff-staff-spacing.basic-distance = #12 } }\n")
        return text

    def write_score(self):

        ####################
        # Section 1 voices #
        ####################

        upper_melody = [
            [],
            notes('af` df`` f``', [2, 4, 4]),
            notes('f`` ef`` gf``', [2, 4, 4]),
            notes('gf`` ef`` df`` c``', 4),
            notes('af`` f`` ef`` d``', 4),
            notes('bf`` gf`` ef``', [2, 4, 4]),
            notes('ef```', '4.') + self.scale('df```', -5, 8),
            notes('f`` ef`` df`` ef`` c`` df``', [8, 8, 8, 8, '4.', 8]),
            notes('df`` ', ['2.', 4])
        ]
        select(upper_melody[1], 1).prefix += (
            '\\tempo "Très lentement" ' + signe +
            '\\repeat volta 1 { ')
        select(upper_melody[1], 1).markdown = 'Plaintivement'

        lower_melody = [
            [],
            rests(1),
            rests(1),
            rests(1),
            rests(1),
            notes('gf bf ef`', [2, 4, 4]),
            tied_note('c`', [2, 8]) + rests(8, 4),
            rests(2) + notes('af', 2),
            notes('df', 4) + rests(4, 2)
        ]
        select(lower_melody[5], 1).suffix += '\\startGroup '
        select(lower_melody[5], 1).markdown += 'mains ou pieds'
        select(lower_melody[5], 3).suffix += '\\stopGroup '
        select(lower_melody[7], 2).suffix += '\\startGroup '
        select(lower_melody[7], 2).markdown += 'mains ou pieds'
        select(lower_melody[8], 1).suffix += '\\stopGroup '

        upper_harmony = [
            [],
            rests(1),
            self.scale('bf`', -4, 8) + self.scale('gf`', -4, 8),
            omit(self.scale('c`', 7, 8), 2) + self.scale('af`', -2, 8),
            (omit(scale('d`', 7, dur=8, key='ef minor harmonic'), 2) +
             self.scale('bf`', -2, 8)),
            (notes('af`', 8) + self.scale('f`', 3, 8) +
             self.scale('gf`', 3, 8) + notes('bf`', 8)),
            (self.scale('bf`', -3, 8) + self.scale('af`', -2, 8) +
             self.scale('c`', 3, 8)),
            (self.scale('f`', 4, 8) + self.scale('af`', -3, 8) +
             notes('gf`', 8)),
            (self.scale('f`', -3, 8) + self.scale('ef`', -2, 8) +
             self.scale('af', -3, 8, step=2))
        ]
        select(upper_harmony[4], 8).articulation = '~'
        select(upper_harmony[5], 8).articulation = '~'

        lower_harmony = [
            [],
            self.scale('f`', -8, 8),
            tied_note('gf', [2, 8]) + self.scale('ef', 3, 8),
            self.transpose(upper_harmony[3], -2),
            transpose(upper_harmony[4], -2, key='ef minor harmonic'),
            transpose(upper_harmony[5], -2, key='ef minor harmonic'),
            self.transpose(upper_harmony[6], -2),
            (self.transpose(subset(upper_harmony[7], 1, 4), -2) +
             transpose(subset(upper_harmony[7], 5, 8), -2,
                       key='ef harmonic minor')),
            (notes('df`', 8) +
             self.transpose(subset(upper_harmony[8], 2, 5), -5) +
             rests(8, 8, 8, prefix='\\omit '))
        ]
        select(upper_harmony[8], 5).markup = '    Fin.'
        select(upper_harmony[8], 5).suffix += '\\bar "||" '
        select(upper_harmony[8], 5).articulation = '['
        select(upper_harmony[8], 8).articulation = ']'
        select(upper_harmony[8], 8).suffix += linebreak

        #########################
        # Section 1 compilation #
        #########################

        if not self.improvements:
            for i in [1, 2, 3, 4]:
                upper_harmony[8][i].prefix += "\\pushNC "
            upper_harmony[8][0].add('df`')
            lower_harmony[8][0].remove('df`')
            lower_harmony[8][0].prefix += '\\omit '
            lower_harmony[8][1].prefix += '\\autoBeamOff \\crossStaff { '
            lower_harmony[8][3].suffix += ' } '
            upper_harmony[8][5].prefix += '\\change Staff = "bass" \\stemUp '
            lower_harmony[8][4].prefix += '\\crossStaff { '
            lower_harmony[8][4].suffix += ' } '
            select(lower_melody[8], 2).prefix += '\\omit '
            select(lower_melody[8], 3).prefix += '\\omit '
            bar3e = (
                rests(8, prefix='\\omit ') +
                notes('ef`', 8,
                      prefix=(
                        '\\voiceOne \\autoBeamOff \\stemDown \\crossStaff {'),
                      suffix='} \\autoBeamOn \\stemNeutral ') +
                rests(2, 4, prefix='\\omit '))
            bar7f = (
                notes('f`', 8, prefix='\\stemDown \\crossStaff { ',
                      suffix='} \\stemNeutral') +
                rests(8, 4, 2, prefix='\\omit '))

            score1 = {
                'treble': [
                    [],
                    upper_melody[1],
                    voices(upper_melody[2], upper_harmony[2]),
                    voices(upper_melody[3], bar3e),
                    voices(upper_melody[4], merge(upper_harmony[4],
                                                  lower_harmony[4])),
                    voices(upper_melody[5], merge(upper_harmony[5],
                                                  lower_harmony[5])),
                    voices(upper_melody[6],
                           merge(upper_harmony[6][0:5],
                                 lower_harmony[6][0:5]) +
                           rests(8, 8, 8, prefix='\\omit ')),
                    voices(upper_melody[7], bar7f),
                    voices(upper_melody[8], upper_harmony[8])],
                'bass': [
                    [],
                    lower_harmony[1],
                    lower_harmony[2],
                    merge(upper_harmony[3], lower_harmony[3]),
                    lower_melody[4],
                    lower_melody[5],
                    lower_melody[6][0:2] + merge(upper_harmony[6][5:8],
                                                 lower_harmony[6][5:8]),
                    voices(merge(upper_harmony[7], lower_harmony[7]),
                           lower_melody[7]),
                    voices(lower_harmony[8],
                           lower_melody[8])]
            }

            select(score1['bass'][3], 1).prefix = (
                '\\override Beam.auto-knee-gap = #10 ')
            select(score1['bass'][3], 2).remove('ef`')
            select(score1['bass'][3], 3).prefix = (
                '\\change Staff = "treble" \\voiceTwo ')
            select(score1['bass'][3], 5).prefix = (
                '\\override Beam.auto-knee-gap = #5.5 ')
            select(score1['bass'][4], 1).prefix = (
                '\\change Staff = "bass" \\omit ')
            select(score1['treble'][6], 11).prefix += '\\crossStaff { '
            select(score1['treble'][6], 11).suffix += ' } '
            select(score1['bass'][7], 1).remove('f`')
            select(score1['bass'][7], 1).prefix += '\\stemDown '
            select(score1['bass'][7], 2).prefix += (
                '\\change Staff = "treble" ')
            select(score1['bass'][7], 9).prefix += '\\omit '
            select(score1['bass'][7], 5).prefix += '\\omit '
            select(score1['treble'][8], 10).suffix += ' } '

        else:
            select(upper_melody[8], 2).suffix += ' } '
            score1 = {
                'treble': upper_melody,
                'middle': self.merge_harmonies(upper_harmony, lower_harmony),
                'bass': lower_melody
            }

        ####################
        # Section 2 voices #
        ####################

        upper_melody2 = [
            [],
            notes('f` bf` df``', [2, 4, 4]),
            notes('df`` c`` ef``', [2, 4, 4]),
            notes('ef`` c`` bf` a`', 4),
            notes('af`` f`` ef`` d``', 4),
            notes('bf`` gf`` ef``', [2, 4, 4]),
            notes('gf`` ef`` d`` ', ['4.', 8, 4, 4]),
            notes('ff`` df`` c`` ', ['4.', 8, 4, 4]),
            notes('af` df`` ff``', [2, 4, 4]),
            notes('ff`` ef`` gf``', [2, 4, 4]),
            notes('gf`` ef`` df`` c``', 4),
            notes('af`` f`` ef`` d``', 4),
            notes('ef``` bf`` gf``', [2, 4, 4]),
            (notes('ef```', '4.') +
             scale('cf```', -5, dur=8, key='ef minor harmonic')),
            (scale('gf``', -3, dur=8, key='ef minor harmonic') +
             notes('cf`` d`` ef``', [8, '4.', 8])),
            notes('ef`` ', ['2.', 4])
        ]

        select(upper_melody2[1], 1).prefix += '\\repeat volta 1 { '

        lower_melody2 = [
            [],
            rests(1),
            rests(1),
            rests(1),
            rests(1),
            notes('bf, ef gf', [2, 4, 4]),
            notes('f bf ', [2, 4, 4]),
            notes('ef af ', [2, 4, 4]),
            rests(1),
            tied_note('gf', [2, 8]) + notes('ef ff gf', 8),
            notes('bff af ', [2, 4, 4]),
            notes('cf` bf ', [2, 4, 4]),
            notes('gf bf ef`', [2, 4, 4]),
            tied_note('cf`', [2, 8]) + notes('cf` bf af', 8),
            notes('bf bf,', 2),
            notes('ef  ', [4, 4, 2])
        ]

        select(lower_melody2[5], 1).suffix += '\\startGroup '
        select(lower_melody2[5], 1).markdown += 'mains ou pieds'
        select(lower_melody2[5], 3).suffix += '\\stopGroup '
        select(lower_melody2[9], 1).suffix += '\\startGroup '
        select(lower_melody2[9], 1).markdown += 'mains ou pieds'
        select(lower_melody2[9], 5).suffix += '\\stopGroup '
        select(lower_melody2[12], 1).suffix += '\\startGroup '
        select(lower_melody2[12], 1).markdown += 'mains ou pieds'
        select(lower_melody2[12], 3).suffix += '\\stopGroup '

        def mini_motif(n):
            n = notes(n, 8)
            return pattern(n, 3, 1, 2, 3)

        upper_harmony2 = [
            [],
            rests(1),
            notes('gf`', 8) + self.scale('af`', -7, 8),
            (omit(scale('a', 7, 'bf minor harmonic', 8), 2) +
             notes('f` ef`', 8)),
            (omit(scale('d`', 7, 'ef minor harmonic', 8), 2) +
             notes('bf` af`', 8)),
            scale('gf``', -8, 'ef minor', 8),
            mini_motif('a` bf` c``') + mini_motif('af` bf` cf``'),
            mini_motif('g` af` bf`') + mini_motif('gf` af` bff`'),
            scale('af`', -8, 'df minor', 8),
            (scale('df``', -4, 'df minor', 8) +
             scale('bff`', -4, 'df minor', 8)),
            pattern(scale('ef`', 5, 'df minor', 8), 1, 2, 3, 1, 4, 5, 4, 3),
            pattern(scale('f`', 5, 'ef minor harmonic', 8),
                    1, 2, 3, 1, 4, 5, 4, 3),
            pattern(scale('f`', 4, 'ef minor harmonic', 8),
                    3, 1, 2, 3, 2, 3, 4, 4),
            pattern(scale('f`', 4, 'ef minor harmonic', 8),
                    4, 4, 3, 2, 3, 1, 2, 3),
            notes('gf` af` bf` cf`` bf` af` g` af`', 8),
            notes('gf` f` ef` f` ef` bf gf ef', 8)
        ]
        select(upper_harmony2[11], 8).articulation = '~'
        select(upper_harmony2[12], 8).articulation = '~'

        lower_harmony2 = [
            [],
            self.scale('df`', -8, 8),
            tied_note('ef', [2, 8]) + self.scale('c', 3, 8),
            transpose(upper_harmony2[3], -2, key='bf minor harmonic'),
            transpose(upper_harmony2[4], -2, key='ef minor harmonic'),
            transpose(upper_harmony2[5], -5, key='ef minor'),
            mini_motif('c` df` ef`') + mini_motif('f` gf` af`'),
            mini_motif('bf cf` df`') + mini_motif('ef` ff` gf`'),
            transpose(upper_harmony2[8], -2, key='df minor'),
            transpose(upper_harmony2[9], -2, key='df minor'),
            transpose(upper_harmony2[10], -2, key='df minor harmonic'),
            transpose(upper_harmony2[11], -2, key='ef minor harmonic'),
            transpose(upper_harmony2[12], -2, key='ef minor harmonic'),
            transpose(upper_harmony2[13], -2, key='ef minor harmonic'),
            notes('ef` f` gf` af` gf` f` e` f`', 8),
            notes('ef` af gf af gf', 8) + rests(8, 8, 8, prefix='\\omit ')
            ]

        #########################
        # Section 2 compilation #
        #########################

        if not self.improvements:
            select(upper_melody2[1], 1).prefix = (
                select(upper_melody2[1], 1).prefix + '\\stemUp ')
            score2 = {
                'treble': [
                    [],
                    upper_melody2[1],
                    voices(upper_melody2[2], upper_harmony2[2]),
                    upper_melody2[3],
                    voices(upper_melody2[4],
                           merge(upper_harmony2[4], lower_harmony2[4])),
                    voices(upper_melody2[5],
                           merge(upper_harmony2[5], lower_harmony2[5])),
                    voices(upper_melody2[6], upper_harmony2[6]),
                    voices(upper_melody2[7],
                           subset(upper_harmony2[7], 1, 4) +
                           merge(subset(upper_harmony2[7], 5, 8),
                                 subset(lower_harmony2[7], 5, 8))),
                    voices(upper_melody2[8], upper_harmony2[8]),
                    voices(upper_melody2[9],
                           merge(upper_harmony2[9], lower_harmony2[9])),
                    voices(upper_melody2[10],
                           merge(upper_harmony2[10], lower_harmony2[10])),
                    voices(upper_melody2[11],
                           merge(upper_harmony2[11], lower_harmony2[11])),
                    voices(upper_melody2[12],
                           merge(upper_harmony2[12], lower_harmony2[12])),
                    voices(upper_melody2[13],
                           merge(upper_harmony2[13], lower_harmony2[13])),
                    voices(upper_melody2[14],
                           merge(upper_harmony2[14], lower_harmony2[14])),
                    voices(upper_melody2[15],
                           subset(upper_harmony2[15], 1, 5) +
                           notes('bf gf ef', 8))
                ],
                'bass': [
                    [],
                    lower_harmony2[1],
                    lower_harmony2[2],
                    merge(upper_harmony2[3], lower_harmony2[3]),
                    rests(1, prefix='\\omit '),
                    lower_melody2[5],
                    voices(lower_harmony2[6], lower_melody2[6]),
                    voices(subset(lower_harmony2[7], 1, 4) +
                           rests(2, prefix='\\omit '),
                           lower_melody2[7]),
                    lower_harmony2[8],
                    lower_melody2[9],
                    lower_melody2[10],
                    lower_melody2[11],
                    lower_melody2[12],
                    lower_melody2[13],
                    lower_melody2[14],
                    voices(lower_harmony2[15], lower_melody2[15])
                ]
            }
            select(score2['bass'][3], 5).prefix += (
                '\\stemDown \\change Staff = "treble" ')
            select(score2['bass'][3], 8).suffix += (
                ' \\stemNeutral \\change Staff = "bass" ')
            select(score2['treble'][10], 5).tones[0] = (
                select(score2['treble'][10], 5).tones[0] + "!")
            select(score2['treble'][11], 5).tones[1] = (
                select(score2['treble'][11], 5).tones[1] + "!")
            select(score2['treble'][6], 4).prefix += '\\omit '
            select(score2['treble'][15], 3).add('ef`')
            select(score2['bass'][15], 1).remove('ef`')
            select(score2['bass'][15], 1).prefix += '\\omit '
            select(score2['treble'][15], 8).prefix += (
                '\\change Staff = "bass" \\stemUp ')
            for i in [4, 5, 6, 7]:
                select(score2['treble'][15], i).prefix += '\\pushNC '
            select(score2['bass'][15], 2).prefix += (
                '\\autoBeamOff \\crossStaff { ')
            select(score2['bass'][15], 5).suffix += ' } '
            select(score2['bass'][15], 10).prefix += '\\omit '
            select(score2['bass'][15], 11).prefix += '\\omit '
            select(score2['treble'][15], 10).suffix += ' } ' + signe

        else:
            score2 = {
                'treble': upper_melody2,
                'middle': self.merge_harmonies2(upper_harmony2,
                                                lower_harmony2),
                'bass': lower_melody2
            }
            select(score2['treble'][15], 2).suffix += ' } ' + signe

        #####################
        # Score compilation #
        #####################

        self.score = join(score1, score2)

    def merge_harmonies(self, upper_harmony, lower_harmony):
        return([
            [],
            lower_harmony[1],
            voices(upper_harmony[2], lower_harmony[2]),
            merge(upper_harmony[3], lower_harmony[3]),
            merge(upper_harmony[4], lower_harmony[4]),
            merge(upper_harmony[5], lower_harmony[5]),
            merge(upper_harmony[6], lower_harmony[6]),
            merge(upper_harmony[7], lower_harmony[7]),
            merge(upper_harmony[8], lower_harmony[8]),
        ])

    def merge_harmonies2(self, upper_harmony2, lower_harmony2):
        return([
            [],
            lower_harmony2[1],
            voices(upper_harmony2[2], lower_harmony2[2]),
            merge(upper_harmony2[3], lower_harmony2[3]),
            merge(upper_harmony2[4], lower_harmony2[4]),
            merge(upper_harmony2[5], lower_harmony2[5]),
            merge(upper_harmony2[6], lower_harmony2[6]),
            merge(upper_harmony2[7], lower_harmony2[7]),
            merge(upper_harmony2[8], lower_harmony2[8]),
            merge(upper_harmony2[9], lower_harmony2[9]),
            merge(upper_harmony2[10], lower_harmony2[10]),
            merge(upper_harmony2[11], lower_harmony2[11]),
            merge(upper_harmony2[12], lower_harmony2[12]),
            merge(upper_harmony2[13], lower_harmony2[13]),
            merge(upper_harmony2[14], lower_harmony2[14]),
            merge(upper_harmony2[15], lower_harmony2[15])
        ])


if __name__ == "__main__":
    GenreAncien()
