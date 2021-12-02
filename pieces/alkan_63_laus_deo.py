from piece import Piece
from points import (
    notes, merge, rests, chord, tied_note, rest, note, add, chords,
    tied_chord, replace)
from util import rep, select, subset, pattern, join
from markup import (
    slur, thinthick_barbreak, ottava, quintuplets, clef, voices,
    doublethick_barbreak, double_barbreak, triplets, linebreak)
from tones import tonify
from copy import deepcopy


class LausDeo(Piece):

    def details(self):
        self.title = "Laus Deo"
        self.composer = "Charles-Valentin Alkan"
        self.date = "1861"
        self.mutopiacomposer = "AlkanCV"
        self.mutopiainstrument = "piano"
        self.source = "Simon Richault, 1861/Costallat & Cie., 1910"
        self.style = "Romantic"
        self.license = "Creative Commons Attribution-ShareAlike 4.0"
        self.maintainer = "Thomas Morgan"
        self.mantainer_email = "thomas.j.h.morgan@gmail.com"
        self.opus = "Op. 63"
        self.tempo = '4/4'
        self.auto_add_bars = True
        self.improvements = True

    def write_score(self):

        # intro #

        def intro_motif(dyn, long=False):
            passage = merge(notes('c`` d`` f`` e`` c``', 8,
                                  articulation='>'),
                            notes('g` af` c`` bf` g`', 8))
            select(passage, 1).dynamics = dyn
            select(passage, 2).suffix = '['
            if long:
                select(passage, 5).suffix = ']'
                return slur(passage)
            else:
                select(passage, 4).suffix = ']'
                return slur(subset(passage, 1, 4))

        intro_treble = (
            rests([4, 8], prefix='%{ spacer %} ') +
            rep(intro_motif('f') + intro_motif('mf'), 2) +
            intro_motif('f', long=True)
        )

        intro_bass = (
            rests([4, 8], prefix='%{ spacer %} ') + rests([8, 4]) +
            tied_note('c,,', [4, 4], articulation='^') +
            rep([rest(4), note('c,,', 2, articulation='^')], 2) + [rest(4)]
        )

        if self.improvements:
            intro_bass = (
                subset(intro_bass, 1, 4) +
                ottava(subset(intro_bass, 5, 10), -2) +
                [select(intro_bass, 11)])

        select(intro_treble, 1).prefix = (
            '\\tempo "Assez lentement" ' + select(intro_treble, 1).prefix)
        select(intro_treble, len(intro_treble)).suffix += thinthick_barbreak
        select(intro_bass, 3).suffix += '\\sustainOn '
        select(intro_bass, len(intro_bass)).suffix += (
            '\\tweak self-alignment-X #-5 \\sustainOff ')

        intro = {'treble': intro_treble, 'bass': intro_bass}

        select(intro['treble'], len(intro['treble'])).suffix += linebreak

        # walking #

        def walking_motif(tones):
            tones = tonify(tones)
            return quintuplets(notes(pattern(tones, 2, 1, 3, 2, 1), 4))

        walking_treble = (
            slur(
                walking_motif('bf c` df`') + walking_motif('g af bf') +
                clef('bass', walking_motif('e f g')) + walking_motif('c d e')
            ) + slur(quintuplets(notes('d c g e c', 4))) +
            slur(walking_motif('c d e')) +
            slur(quintuplets(self.scale('e', 5, 4)))
        )

        def walked_bass():
            return (clef('treble', (
                [chord('c`` e``', 1)] +
                add(merge(notes('d`` e`` f`` g``', 2),
                          notes('f`` g`` af`` bf``', 2)), 'c``') +
                voices(
                    rep(slur(chords(['f`` af`` b``', 'e`` g`` c```'], 2)), 3) +
                    rests(1, prefix='\\omit '),
                    notes('c``', [1, 1, 1], articulation='-') +
                    slur(chords(['b` g``', 'a` f``'], 2)))
            )))

        walking_bass = walked_bass()

        select(walking_treble, 1).prefix = (
            '\\tempo "Même mouvement" ' + select(walking_treble, 1).prefix)
        select(walking_treble, 30).dynamics = '!'
        select(walking_treble, 35).dynamics = '!'
        select(walking_treble, 35).suffix += doublethick_barbreak
        select(walking_bass, len(walking_bass)-1).prefix = (
            '\\set doubleSlurs = ##t ' +
            select(walking_bass, len(walking_bass)-1).prefix)

        if self.improvements:
            select(walking_bass, 1).markup = '\\italic{dolce}'
            select(walking_bass, 1).markdown = (
                   '\\dynamic{p} \\italic{e sostenuto}')
            select(walking_treble, 21).suffix = '^\\<'
            select(walking_treble, 31).suffix = '^\\>'
            select(walking_treble, 31).markup = '\\italic{poco cal.}'
            walking = {'treble': walking_bass, 'bass': walking_treble}
        else:
            select(walking_treble, 1).markup = '\\italic{Dolce}'
            select(walking_treble, 1).markdown = (
                   '\\dynamic{p} \\italic{e sostenuto}')
            select(walking_treble, 21).dynamics = '<'
            select(walking_treble, 31).dynamics = '>'
            select(walking_treble, 31).markdown = '\\italic{poco cal.}'
            walking = {'treble': walking_treble, 'bass': walking_bass}

        select(walking['treble'], len(walking['treble'])).suffix += linebreak

        # bridge 1 #

        v1 = (notes('e` f` d` e`', [2, 4]) +
              notes('d` c`', [8, 8, 2, '2.']))
        v2 = (notes('g a b', [2, 4]) +
              notes('c`', 4, phrasing='~') + [chord('a c`', 4)] +
              notes('b a b g', [8, 8, 4, '2.']))
        v3 = (rests(2, 4, prefix='\\omit ') + notes('g', '2.') +
              tied_note('f', ['2.', 4]) + notes('e d e', [8, 8, 4]))

        v4 = rests(1, 2, 4, 4) + notes('g, f, g,', [8, 8, '2.'])
        v5 = (rests(1, 2, prefix='\\omit ') + rests('2.') +
              notes('c, b,, c,', [8, 8, 2]))

        v6 = (notes('e` f` g` c`` a` b`', [2, 4]) +
              chords(['a`', 'd` g`'], '2.'))
        v8 = (chords(['c`', 'b d`', 'c` e`'], ['2.', 2, 4]) +
              notes('d` c`', 4) + [chord('b d`', 4)] + notes('c` b', 8) +
              [chord('c` d`', 2, phrasing='~')] +
              notes('c` b a b', [4, 8, 8, 4]))
        v7 = (rests(1, 2, prefix='\\omit ') + notes('fs`', 2) +
              notes('g`', 4, phrasing='~') + [chord('e` g`', 4)] +
              notes('fs` e` fs`', [8, 8, 4])) + rests(2, 4, prefix='\\omit ')

        v9 = rests('1', 2, 2, 4, 4, 4) + notes('d c d', [8, 8, '2.'])
        v10 = (
            rep(rests(2, prefix='\\omit '), 6) + notes('g, fs, g,', [8, 8, 2]))

        v11 = (notes('d` e`', [2, 4]) +
               chords(['a f`', 'g g`', 'g e`', 'f f`'], [2, 4]) +
               notes('e` d` e`', [8, 8, 2]) + [chord('a d`', '2.')])
        v12 = (notes('d` cs`', [2, 4]) +
               tied_note('d`', ['2.', 4]) + notes('c` b c`', [8, 8, 4]) +
               chords(['f bf', 'bf d`', 'a cs`'], 4) +
               notes('g e f', [8, 8, 2]))
        v13 = (merge(notes('g f e d c b, c b, a, bf,', 4),
                     notes('bf a g f e d e d c d', 4)) +
               notes('g, a, g,', [4, 8, 8]) + rests(4) +
               notes('d, cs, d,', [8, 8, 4]))
        v14 = (rests(2, 4, 2, 2, 2, 4, prefix='\\omit ') +
               notes('g a g', [8, 8, 4]) + [chord('a, d', '2.')])

        v15 = (notes('f` e` d` e` c` d`', [2, 4]) +
               [chord('c` d`', 8)] + notes('c` d`', [8, 2]))
        v16 = (rests(2, 4, prefix='\\omit ') + notes('a b', [2, 4]) +
               chords(['a c`', 'g b', 'fs a c`', 'af'], 4) +
               [chord('g b', 8)] + [chord('f a', 8, phrasing='~')] +
               [chord('f g b', 4)])
        v17 = (rests(2, 2, 2, prefix='\\omit ') + notes('a,', 2) +
               rests(4, prefix='\\omit ') + notes('f', 2) +
               notes('g, f,', 8))
        v18 = (rests('2.') + notes('fs gs', [2, 4]) +
               rests(2, prefix='\\omit ') + notes('d e f e', 8) +
               notes('f', 4) + rests(4, prefix='\\omit '))

        v15a = [chord('g c`', '2.')]
        v16a = notes('f d e', [8, 8, 2])
        v17a = notes('g,', '2.')
        v18a = rests(4) + notes('c, b,, c,', [8, 8, 4])

        v15b = (chords(['g c`', 'c`'], '2.', phrasing='~'))
        v16b = notes('f d e', [8, 8, 2]) + rests('2.')
        v17b = notes('g, ', '2.')
        v18b = rests(4) + notes('c, b,, c,', [8, 8, 4]) + rests('2.')

        for vv in ([v1, v2, v3, v4, v5, v6, v8, v9, v10, v11, v12, v13, v14,
                    v15a, v16a, v17a, v18a]):
            select(vv, len(vv)).ornamentation = 'fermata'

        select(v3, 4).phrasing = '_~'
        if not self.improvements:
            select(v4, 3).markup = '\\italic{dolce e legato}'
            select(v4, 6).markdown = '\\italic{dolce e legato}'
        select(v1, 8).markup = '\\italic{calando}'

        select(v6, 1).prefix = (
            '\\tempo "A tempo"') + select(v6, 1).prefix
        if not self.improvements:
            select(v6, 1).markdown = '\\italic{sempre}'
        select(v6, 1).dynamics = '<'
        select(v6, 4).dynamics = '!'
        select(v6, 6).phrasing = '('
        select(v6, 7).phrasing = ')'
        select(v6, len(v6)).markup = '\\italic{calando}'
        select(v8, len(v8)-3).dynamics = '>'
        select(v8, len(v8)).dynamics = '!'
        select(v11, 1).prefix += '\\tempo "A tempo" '
        select(v11, 1).markdown = '\\italic{sempre dolce}'
        select(v11, 7).markdown = '\\italic{poco cresc.}'
        select(v11, 9).ornamentation = 'tenuto'
        select(v12, 10).markup = '\\italic{calando}'
        select(v15, 1).prefix += '\\tempo "A tempo" '
        select(v15, 1).markdown = '\\italic{dim.}'
        select(v15, 5).ornamentation = 'tenuto'
        select(v15a, len(v15a)).markup = '\\italic{calando}'
        select(v15b, 1).markup = '\\italic{calando}'
        select(v15b, 1).suffix += '\\bar "||" '
        select(v18b, len(v18b)).suffix += (
            '\\tweak self-alignment-X #-5 \\sustainOff ' +
            '\\tweak self-alignment-X #-1 \\treCorde ')

        if self.improvements:
            select(v3, 1).prefix = ''
            select(v3, 2).prefix = ''
            select(v4, 1).prefix = '\\omit '
            select(v4, 2).prefix = '\\omit '
            select(v4, 3).prefix = '\\omit '
            select(v4, 4).prefix = '\\omit '
            select(v9, 1).prefix = '\\omit '
            select(v9, 2).prefix = '\\omit '
            select(v9, 3).prefix = '\\omit '
            select(v9, 4).prefix = '\\omit '
            select(v9, 5).prefix = '\\omit '
            select(v9, 6).prefix = '\\omit '
            select(v8, len(v8)-3).dynamics = ''
            select(v8, len(v8)-3).suffix = '^\\>'
            rh_voices = ottava(voices(v1, v2), -1)
            lh_voices = voices(v3, v5, v4)
            rh_voices2 = voices(v6, v7)
            lh_voices2 = voices(v8, v10, v9)
        else:
            rh_voices = voices(v1, v2, v3)
            lh_voices = voices(v4, v5)
            rh_voices2 = voices(v6, v8, v7)
            lh_voices2 = voices(v9, v10)

        rh_voices3 = voices(v11, v12)
        lh_voices3 = voices(v14, v13)
        rh_voices4 = voices(v15, v16)
        lh_voices4 = voices(v17, v18)
        rh_voices4a = voices(v15a, v16a)
        lh_voices4a = voices(v17a, v18a)
        rh_voices4b = voices(v15b, v16b)
        lh_voices4b = voices(v17b, v18b)

        if self.improvements:
            rh_voices3 = ottava(rh_voices3, -1)
            rh_voices4 = ottava(rh_voices4, -1)
            rh_voices4a = ottava(rh_voices4a, -1)
            rh_voices4b = ottava(rh_voices4b, -1)

        select(rh_voices2, len(rh_voices2)).suffix += linebreak
        select(rh_voices3, 1).prefix = (
            '\\repeat volta 2 { ' + select(rh_voices3, 1).prefix)
        select(rh_voices4, len(rh_voices4)).suffix += double_barbreak + ' }\n'
        select(rh_voices4a, 1).prefix = (
            '%{ start alternatives %} \\alternative { \n{ ' +
            select(rh_voices4a, 1).prefix)
        select(rh_voices4a, len(rh_voices4a)).suffix += ' } %{'
        select(rh_voices4b, 1).prefix = (
            '%{ switch alternative %} { ' + select(rh_voices4b, 1).prefix)
        select(rh_voices4b, len(rh_voices4b)).suffix += ' }\n }\n'
        select(lh_voices3, 1).prefix = (
            '\\repeat volta 2 { ' + select(lh_voices3, 1).prefix)
        select(lh_voices4, len(lh_voices4)).suffix += double_barbreak + ' }\n'
        select(lh_voices4a, 1).prefix = (
            '%{ start alternatives %} \\alternative { \n{ ' +
            select(lh_voices4a, 1).prefix)
        select(lh_voices4a, len(lh_voices4a)).suffix += ' } %{'
        select(lh_voices4b, 1).prefix = (
            '%{ switch alternative %} { ' + select(lh_voices4b, 1).prefix)
        select(lh_voices4b, len(lh_voices4b)).suffix += (
            doublethick_barbreak + ' }\n }\n' + linebreak)

        if self.improvements:
            b1_treble_intro = (
                rests(2, 4) +
                clef('treble', ottava(notes('c` d`', [2, 4]), -1)))
        else:
            b1_treble_intro = (
                rests(2, 4) + clef('treble', notes('c` d`', [2, 4])))

        b1_treble = (
            b1_treble_intro +
            rh_voices + rh_voices2 + rh_voices3 +
            rh_voices4 + rh_voices4a + rh_voices4b)

        b1_bass = (
            rests(2, 4) + clef('bass', rests(2, 4)) +
            lh_voices + lh_voices2 + lh_voices3 +
            lh_voices4 + lh_voices4a + lh_voices4b)

        select(b1_treble, 1).prefix = (
            '\\tempo "Un peu plus lentement" ' +
            '\\time 6/4 ' + select(b1_treble, 1).prefix)
        select(b1_bass, 1).prefix = (
            '\\time 6/4 ' + select(b1_bass, 1).prefix)
        select(b1_treble, 3).markup = '\\italic{dolce e legato}'
        if not self.improvements:
            select(b1_treble, 3).prefix += '\\bar "||" '
        select(b1_bass, 3).markup = '\\italic{sostenutissimo}'
        select(b1_bass, 3).suffix = '\\sustainOn \\unaCorda '

        b1 = {'treble': b1_treble, 'bass': b1_bass}

        # walking 2 #

        walking2_treble = (
            slur(
                walking_motif('bf c` df`') + walking_motif('g af bf') +
                clef('bass', walking_motif('e f g'))) +
            slur(
                walking_motif('c d e') +
                quintuplets(notes('d c g e c', 4)) +
                walking_motif('c d e') +
                quintuplets(self.scale('e', 5, 4))) +
            tied_note('c`', [2, '4.'])
        )
        walking2_bass = walked_bass() + voices(
            slur(triplets(
                notes('f``', 4) + notes('e``', 8, phrasing='[') +
                notes('d``', 8, phrasing=']') +
                notes('e``', 4, phrasing=')~'))) +
            notes('e``', '4.'),
            tied_chord('g` c``', [2, '4.']))

        replace(select(walking2_bass, 16), 'b`', 'bf`')

        select(walking2_treble, 1).prefix = (
            '\\time 4/4 \\tempo "Al primo tempo" ' +
            select(walking2_treble, 1).prefix)
        select(walking2_bass, 1).prefix = (
            '\\time 4/4 ' + select(walking2_bass, 1).prefix)
        select(walking2_treble, 35).dynamics = '!'
        select(walking2_treble, len(walking2_treble)).suffix += '\\bar "|." '
        select(walking2_bass, len(walking2_bass)-8).phrasing = '^('
        select(walking2_bass, len(walking2_bass)-7).phrasing = '^)'
        select(walking2_bass, len(walking2_bass)-9).ornamentation = '('
        select(walking2_bass, len(walking2_bass)-7).ornamentation = ')'

        if not self.improvements:
            select(walking2_treble, 1).markdown = '\\italic{dolce e sostenuto}'
            select(walking2_treble, 16).dynamics = '<'
            select(walking2_treble, 31).dynamics = '>'
            select(walking2_treble, 31).markdown = '\\italic{poco cal.}'
            select(walking2_treble, 36).markdown = '\\italic{rall.}'
            walking2 = {'treble': walking2_treble, 'bass': walking2_bass}
        else:
            select(walking2_treble, 1).markup = '\\italic{dolce e sostenuto}'
            select(walking2_treble, 16).suffix = (
                '^\\<' + select(walking2_treble, 16).suffix)
            select(walking2_treble, 31).suffix = (
                '^\\>' + select(walking2_treble, 31).suffix)
            select(walking2_treble, 31).markup = '\\italic{poco cal.}'
            select(walking2_treble, 36).markup = '\\italic{rall.}'
            walking2 = {'treble': walking2_bass, 'bass': walking2_treble}

        select(walking2['treble'], len(walking2['treble'])).suffix += linebreak

        # outro #

        outro_treble = (
            clef('treble', intro_motif('f') + intro_motif('mf') +
                 intro_motif('f') + intro_motif('mf', long=True)) +
            rests(8) + slur(merge(notes('bf` g`', [8, 4]),
                                  notes('e`` c``', [8, 4]))) +
            rests('8.') + slur(notes('bf` g`', [16, 4])) +
            rests(4) + notes('g`', 4, articulation='.') +
            rests(2, ornamentation='fermata'))

        outro_bass = (
            rests(8) + clef('bass', notes('c,,', 2, articulation='^')) +
            rests(4) + tied_note('c,,', [4, 4], articulation='^') +
            rests(4) + notes('c,,', 2, articulation='^') +
            rests(4) + notes('c,,', 4, articulation='^') +
            rests(2) + notes('c,,', 4, articulation='.') +
            rests(4) + rests(2, ornamentation='fermata'))

        select(outro_bass, 1).ornamentation = 'sustainOn'
        select(outro_treble, 18).markdown = '\\italic{dim. e rit.}'
        select(outro_treble, 24).dynamics = 'p'
        select(outro_treble, len(outro_treble)).ornamentation = 'fermata'
        select(outro_bass, len(outro_bass)).ornamentation = 'fermata'
        select(outro_treble, len(outro_treble)).suffix = doublethick_barbreak
        select(outro_bass, len(outro_bass)).suffix += (
            '\\tweak self-alignment-X #-5 \\sustainOff ')

        if self.improvements:
            outro_bass = (
                [select(outro_bass, 1)] +
                ottava(subset(outro_bass, 2, 11), -2) +
                subset(outro_bass, 12, 13))

        outro = {'treble': outro_treble, 'bass': outro_bass}

        self.score = join(intro, walking, b1, walking2, outro)


if __name__ == "__main__":
    LausDeo()
