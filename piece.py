import re

from keys import key_dictionary, keyify
from staves import Treble, Bass
from util import flatten
from tones import equivalent_letters
from points import Point, scale, arpeggio, arpeggio7, dominant7, diminished7, chromatic, scale_subset, transpose, harmonize
from markup import barbreak


class Piece:

    def __init__(self):
        self.title = ""
        self.subtitle = ""
        self.composer = ""
        self.date = ""
        self.mutopiacomposer = ""
        self.mutopiainstrument = "piano"
        self.source = ""
        self.style = ""
        self.license = "Creative Commons Attribution-ShareAlike 4.0"
        self.maintainer = ""
        self.mantainer_email = ""
        self.opus = ""
        self.staves = [Treble(), Bass()]
        self.tempo = "4/4"
        self.key = "C Major"
        self.score = {}
        self.auto_add_bars = False

        self.details()

        self.set_key(self.key)
        print(self)

    def details():
        raise NotImplementedError("You must overwrite details to create a piece")

    def set_key(self, key):
        self.key = keyify(key)

    @property
    def key_signature(self):
        return str(self.key)

    def write_score(self):
        raise NotImplementedError("You must overwrite write_score to create a piece")

    def __str__(self):
        printed_score = self.header() + self.subtext() + self.start_score()
        initial_key = str(self.key)
        self.write_score()
        for stave in self.staves:
            printed_score += stave.start
            printed_score += initial_key
            printed_score += "\\time {}\n".format(self.tempo)
            printed_score += self.print_stave(stave)
            printed_score += stave.end
        printed_score += self.end_score()
        printed_score = printed_score.replace("`", "'")
        return(printed_score)

    def header(self):
        return (
            '\\version "2.18.2"\n'
            + '\\language "english"\n'
            + '\\header {\n'
            + '    title = "{}"\n'.format(self.title)
            + '    subtitle = "{}"\n'.format(self.subtitle)
            + '    composer = "{}"\n'.format(self.composer)
            + '    date = "{}"\n'.format(self.date)
            + '    mutopiacomposer = "{}"\n'.format(self.mutopiacomposer)
            + '    mutopiainstrument = "{}"\n'.format(self.mutopiainstrument)
            + '    maintainer = "{}"\n'.format(self.maintainer)
            + '    maintainerEmail = "{}"\n'.format(self.mantainer_email)
            + '    source = "{}"\n'.format(self.source)
            + '    style = "{}"\n'.format(self.style)
            + '    license = "{}"\n'.format(self.license)
            + '    maintainer = "Anonymous"\n'
            + '    opus = "{}"\n'.format(self.opus)
            + '}\n'
        )

    def subtext(self):
        return ""

    def start_score(self):
        return('\\score { <<\n')

    def end_score(self):
        return('>> }\n')

    def print_stave(self, stave):
        if type(self.score[stave.name]) is dict:
            return " ".join([str(item) for item in flatten([self.score[stave.name]])])

        stave = self.score[stave.name]
        if isinstance(stave, Point):
            return(str(stave))
        elif isinstance(stave, list):
            if self.auto_add_bars:
                stave = self.add_barlines(stave)

            stave = [str(item) for item in flatten(stave)]
            stave = " ".join(stave)
            stave = re.sub('\n ', '\n', stave)
            return(stave)
        else:
            raise TypeError("stave with value {} cannot be printed".format(stave))

    def add_barlines(self, stave):
        num_bars = 0

        bar_length = 1

        bar_progress = 0.0

        progress_at_voice_start = 0.0
        bars_at_voice_start = 0

        mult = 1.0

        stave = flatten(stave)

        for point in stave:

            if "\n<<\n{ " in point.prefix:
                progress_at_voice_start = bar_progress
                bars_at_voice_start = num_bars

            if '\\tuplet 3/2 {' in point.prefix:
                mult *= 2.0/3.0

            if '\\grace {' in point.prefix or ' %{ start grace %}{' in point.prefix or '\\acciaccatura {' in point.prefix:
                old_mult = mult
                mult = 0.0

            if isinstance(point.dur, int):
                progress = 1 / float(point.dur)
            else:
                if point.dur == '\\longa':
                    progress = 4.0
                elif point.dur == '\\breve':
                    progress = 2.0
                elif '..' in point.dur:
                    progress = (1 / float(int(point.dur[:-2]))) * 1.75
                elif '.' in point.dur:
                    progress = (1 / float(int(point.dur[:-1]))) * 1.5
                else:
                    progress = 1 / float(int(point.dur))
            bar_progress += progress*mult


            if bar_progress > 1:
                raise ValueError("Duration of notes crosses a bar line: {} in bar {}".format(str(point), num_bars+1))

            if bar_progress == 1 and " }\n\\\\\n" not in point.suffix and progress*mult != 0.0:
                point.suffix += barbreak
                bar_progress = 0
                num_bars += 1

            if " }\n\\\\\n" in point.suffix:
                num_bars = bars_at_voice_start
                bar_progress = progress_at_voice_start

            if '} %{ end triplets %}' in point.suffix:
                mult /= 2.0/3.0

            if '} %{ end grace %}' in point.suffix or '} %{ end acciaccatura %}' in point.suffix:
                mult = old_mult


        return(stave)


    def scale(self, start, stop_or_length, dur=None, step=1):
        return scale(start, stop_or_length, self.key, dur, step)

    def arpeggio(self, start, stop_or_length, dur=None, step=1):
        return arpeggio(start, stop_or_length, self.key, dur, step)

    def arpeggio7(self, start, stop_or_length, dur=None, step=1):
        return arpeggio7(start, stop_or_length, self.key, dur, step)

    def dominant7(self, start, stop_or_length, dur=None, step=1):
        return dominant7(start, stop_or_length, self.key, dur, step)

    def diminished7(self, start, stop_or_length, dur=None, step=1):
        return diminished7(start, stop_or_length, self.key, dur, step)

    def chromatic(self, start, stop_or_length, dur=None, step=1):
        return chromatic(start, stop_or_length, self.key, dur, step)

    def scale_subset(self, positions, start, stop_or_length, dur=None, step=1):
        return scale_subset(positions, start, stop_or_length, self.key, dur, step)

    def transpose(self, item, shift, mode="scale", clean=False):
        return transpose(item, shift, self.key, mode, clean)

    def harmonize(self, points, intervals, mode="scale"):
        return harmonize(points, intervals, self.key, mode)

    def relative_key(self, mode, relationship):
        my_root = self.key.root
        index_of_my_root = self.key.letters.index(my_root)
        new_index = index_of_my_root + relationship
        new_root = (self.key.letters * 2)[new_index]

        try:
            return key_dictionary[mode][new_root]
        except KeyError:
            try:
                new_root2 = equivalent_letters[new_root]
                return key_dictionary[mode][new_root2]
            except KeyError:
                raise KeyError("Error: No {} key exists with root {} or {}".format(mode, new_root, new_root2))

    def relative_major_key(self, relationship):
        return self.relative_key("major", relationship)

    def relative_minor_key(self, relationship):
        return self.relative_key("minor", relationship)

    def relative_harmonic_key(self, relationship):
        return self.relative_key("harmonic", relationship)

    def relative_cis_key(self, relationship):
        if "major" in self.key.name:
            return self.relative_major_key(relationship)
        else:
            return self.relative_minor_key(relationship)

    def relative_trans_key(self, relationship):
        if "minor" in self.key.name:
            return self.relative_major_key(relationship)
        else:
            return self.relative_minor_key(relationship)

    @property
    def I(self):
        return self.relative_major_key(0)

    @property
    def II(self):
        return self.relative_major_key(1)

    @property
    def III(self):
        return self.relative_major_key(2)

    @property
    def IV(self):
        return self.relative_major_key(3)

    @property
    def V(self):
        return self.relative_major_key(4)

    @property
    def VI(self):
        return self.relative_major_key(5)

    @property
    def VII(self):
        return self.relative_major_key(6)

    @property
    def i(self):
        return self.relative_minor_key(0)

    @property
    def ii(self):
        return self.relative_minor_key(1)

    @property
    def iii(self):
        return self.relative_minor_key(2)

    @property
    def iv(self):
        return self.relative_minor_key(3)

    @property
    def v(self):
        return self.relative_minor_key(4)

    @property
    def vi(self):
        return self.relative_minor_key(5)

    @property
    def vii(self):
        return self.relative_minor_key(6)

    @property
    def ih(self):
        return self.relative_harmonic_key(0)

    @property
    def iih(self):
        return self.relative_harmonic_key(1)

    @property
    def iiih(self):
        return self.relative_harmonic_key(2)

    @property
    def ivh(self):
        return self.relative_harmonic_key(3)

    @property
    def vh(self):
        return self.relative_harmonic_key(4)

    @property
    def vih(self):
        return self.relative_harmonic_key(5)

    @property
    def viih(self):
        return self.relative_harmonic_key(6)

    @property
    def Ic(self):
        return self.relative_cis_key(0)

    @property
    def IIc(self):
        return self.relative_cis_key(1)

    @property
    def IIIc(self):
        return self.relative_cis_key(2)

    @property
    def IVc(self):
        return self.relative_cis_key(3)

    @property
    def Vc(self):
        return self.relative_cis_key(4)

    @property
    def VIc(self):
        return self.relative_cis_key(5)

    @property
    def VIIc(self):
        return self.relative_cis_key(6)

    @property
    def It(self):
        return self.relative_trans_key(0)

    @property
    def IIt(self):
        return self.relative_trans_key(1)

    @property
    def IIIt(self):
        return self.relative_trans_key(2)

    @property
    def IVt(self):
        return self.relative_trans_key(3)

    @property
    def Vt(self):
        return self.relative_trans_key(4)

    @property
    def VIt(self):
        return self.relative_trans_key(5)

    @property
    def VIIt(self):
        return self.relative_trans_key(6)
