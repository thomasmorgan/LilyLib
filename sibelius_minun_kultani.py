from piece import Piece
from points import chord, rests, tied_note, notes, tied_chord, chords
from markup import slur, voices, clef, italic, diminuendo
from util import rep, subset, select
from staves import Treble, Bass, Dynamics


class MinunKultani(Piece):

    def details(self):
        self.title = "Minun Kultani"
        self.composer = "Jean Sibelius"
        self.date = "1903"
        self.mutopiacomposer = "SibeliusJ"
        self.mutopiainstrument = "piano"
        self.source = "Breitkopf und Härtel, 1906"
        self.style = "Romantic"
        self.license = "Creative Commons Attribution-ShareAlike 4.0"
        self.maintainer = "Thomas Morgan"
        self.mantainer_email = "thomas.j.h.morgan@gmail.com"
        self.opus = "JS 81, No. 1"
        self.auto_add_bars = True
        self.key = 'fs minor'
        self.tempo_name = "Allegretto"
        self.staves = [
            Treble(),
            Dynamics(),
            Bass(
                _with=(
                    '\\override Beam.breakable = ##t\n'
                    '\\consists "Span_arpeggio_engraver"'),
                extra_text=(
                    '\\set Staff.connectArpeggios = ##t\n'
                    '\\override Staff.Arpeggio.stencil = '
                    '#ly:arpeggio::brew-chord-slur\n'
                    '\\override Staff.Arpeggio.X-extent = '
                    '#ly:grob::stencil-width\n'
                    '\\revert Staff.Arpeggio.dash-definition\n'))]

    def write_score(self):

        ###########
        # part 1
        ###########

        def split_note(note):
            notes = chords([note], [8, 8])
            select(notes, 1).phrasing += '_~['
            select(notes, 2).phrasing += ']'
            return notes

        def chord_motif(*args):
            split_notes = split_note('fs')
            motif = slur(self.harmonize(
                notes('gs fs e', 4) + split_notes, -2))
            if "short" in args:
                motif = subset(motif, 1, 4)
                select(motif, 4).phrasing = ')'
            return motif

        treble_1 = (
            rests(8) + rep(chord_motif(), 2) + chord_motif("short") +
            rests(4) + tied_chord('b, d', ['2.', 1, 1]))
        bass_1 = rep(chord('e, b,', 1), 3) + tied_chord('b,, fs,', [1, 1, 1])
        select(bass_1, 6).prefix = '\\afterGrace 15/16 {'
        select(bass_1, 6).suffix = '} { s32 \\sustainOff } '

        for i in [1, 7, 11, 16]:
            select(treble_1, i).suffix += '\\sustainOn'
        for i in [4, 9, 14]:
            select(treble_1, i).suffix += '\\sustainOff'

        dynamics_1 = rep(rests(1, prefix='%{ spacer %}'), 5)
        select(dynamics_1, 1).dynamics = 'mp'

        ###########
        # part 2
        ###########

        mini_motif = (
            slur(notes('fs e', ['4.', 8])) +
            notes('cs e', 4, articulation='-'))
        treble_2 = (
            clef('bass', rep(notes('fs', 4, articulation='-'), 4)) +
            mini_motif + self.transpose(mini_motif, -1) +
            notes('d', 2, articulation='-') +
            tied_note('cs', [2, 1], articulation='-')
            )
        select(treble_2, 2).dynamics = '<'
        for i in [4, 7, 11, 14]:
            select(treble_2, i).dynamics = '!'
        for i in [5, 9, 13]:
            select(treble_2, i).dynamics = '>'
        bass_2 = rep(rests(1), 4)
        dynamics_2 = rep(rests(1, prefix='%{ spacer %}'), 5)
        select(dynamics_2, 1).dynamics = 'mf'

        select(treble_2, 1).markup = italic('semplice')

        ###########
        # part 3
        ###########

        shift = '\\once \\override NoteColumn.force-hshift = #0.7 '

        mini_motif_2 = (
            notes('fs cs d b, cs fs, b, d', 4, articulation='-') +
            slur(diminuendo(notes('fs e', ['4.', 8]))) +
            notes('d cs', 4, articulation='-') + notes('b,', 2) +
            tied_note('b,', [2, 1]))

        high_treble_3 = (
            clef('treble', rep(rests(1, prefix='%{ spacer %}'), 5)) +
            self.transpose(treble_2, 1, 'octave') +
            self.transpose(mini_motif_2, 1, 'octave') +
            rep(rests(1, prefix='%{ spacer %}'), 3))
        select(high_treble_3, 6).prefix = ''
        select(high_treble_3, 6).markup = ''
        for i in [16, 18, 19, 25, 26, 27, 28]:
            select(high_treble_3, i).articulation = ''
        select(high_treble_3, 18).dynamics = ''
        select(high_treble_3, 19).dynamics = ''

        treble_3 = (
            rests(8) + rep(chord('gs b', 4), 3) +
            split_note('gs b') + rep(chord('as cs`', 4), 2) +
            [chord('gs d`', 4)] +
            rep(split_note('gs d`') +
                rep(chord('gs d`', 4), 3), 4) +
            split_note('gs d`') + [chord('g cs`', 4)] +
            chords(['g as'], [4, 4]) + split_note('g as') +
            chords(['f b'], [4, 4]) + [chord('d f', 4)] +
            split_note('f b') +
            rep(chords(['e as'], [4, 4, 4]) + split_note('e as'), 2) +
            chords(['e as'], [4, 4]) + [chord('e gs', 4)] +
            split_note('e gs') + chords(['e as'], [4, 4]) +
            chords(['e gs'], [4, 8]) +
            rests(8) + chords(['g cs`'], [4, 8]) +
            rests(8) + chords(['e as'], [4, 8]) +
            rests(8) + rep(chord_motif(), 2) + chord_motif("short") +
            rests(4) + tied_chord('b, d', ['2.', 1]))
        select(treble_3, 16).dynamics = '>'
        select(treble_3, 17).dynamics = '!'
        select(treble_3, 19).markup = italic('dim.')

        bass_3 = (
            mini_motif_2 +
            self.transpose(
                subset(high_treble_3, 6, len(high_treble_3)), -1, 'octave'))
        for note in subset(bass_3, 15, len(bass_3)):
            note.dynamics = ''
            if note.articulation == '-':
                note.articulation = ''
        select(bass_3, 1).prefix += '\\voiceFour '
        select(bass_3, 14).dynamics = '>'
        select(bass_3, 15).dynamics = '!'
        select(bass_3, 16).prefix += shift
        select(bass_3, 16).suffix = '\\arpeggio '
        select(bass_3, 16).markup = ''
        select(bass_3, 31).prefix += shift
        select(bass_3, 31).suffix = '\\arpeggio '

        low_bass_3 = (
            rep(rests(1, prefix='%{ spacer %}'), 5) +
            notes('e,', 1) + tied_note('e,', [1, 2]) +
            notes('e,', 2) + tied_note('e,', [1, 1]) +
            tied_note('e,', [1, 2]) + notes('e,', 2) +
            tied_note('e,', [1, 2]) + tied_chord('e, b,', [2, 1, 1]) +
            tied_chord('b,, fs,', [1, 1]))
        select(low_bass_3, 6).prefix += shift
        select(low_bass_3, 6).suffix = '\\arpeggio \\omit \\sustainOn'
        select(low_bass_3, 7).suffix = '\\sustainOff \\sustainOn'
        select(low_bass_3, 8).suffix = '\\sustainOff \\sustainOn'
        select(low_bass_3, 10).suffix = '\\sustainOff \\sustainOn'
        select(low_bass_3, 11).suffix = '\\sustainOn'
        select(low_bass_3, 12).prefix += (
            "\\once \\override Staff.Arpeggio.positions = #'(-3 . 0) " +
            '\\once \\override Staff.Arpeggio.X-offset = #0.9 ' + shift)
        select(low_bass_3, 12).suffix = '\\arpeggio '
        select(low_bass_3, 16).add('b,')

        dynamics_3 = (
            rep(rests(1), 4) + rests(2, 4, 4) + rests(1, 1, 1) +
            rests('16.', 32, 8, 4, 2) + rests(1))
        select(dynamics_3, 7).dynamics = 'mf'
        select(dynamics_3, 11).dynamics = '>'
        select(dynamics_3, 12).dynamics = '!'
        select(dynamics_3, 15).dynamics = '>'
        select(dynamics_3, 16).dynamics = '!'

        ###########
        # combine
        ###########

        self.score = {
            'treble': (
                rep(rests(1, prefix='%{ spacer %}'), 4) + rests(1) +
                treble_2 + high_treble_3),
            'dynamics': dynamics_1 + dynamics_2 + dynamics_3,
            'bass': (
                voices(treble_1, bass_1) + bass_2 +
                voices(treble_3, low_bass_3, bass_3))
        }


if __name__ == "__main__":
    MinunKultani()
