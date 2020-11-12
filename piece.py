from keys import key_dictionary, keyify
from staves import Treble, Bass
from util import flatten
from tones import equivalent_letters
from lilylib import Point, scale, arpeggio, arpeggio7, dominant7, diminished7, chromatic, scale_subset, transpose

from itertools import cycle


class Piece:

    def __init__(self):
        self.title = ""
        self.subtitle = ""
        self.composer = ""
        self.opus = ""
        self.staves = [Treble(), Bass()]
        self.tempo = "4/4"
        self.key = "C Major"
        self.score = {}

        self.details()

        self.set_key(self.key)
        print(self)

    def details():
        raise NotImplementedError("You must overwrite details to create a piece")

    def set_key(self, key):
        self.key = keyify(key)

    @property
    def key_signature(self):
        return [str(self.key)]

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
            + '    mutopiacomposer = ""\n'
            + '    mutopiainstrument = "piano"\n'
            + '    source = ""\n'
            + '    style = "Romatic"\n'
            + '    license = "Creative Commons Attribution-ShareAlike 4.0"\n'
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
            stave = [str(item) for item in flatten(stave)]
            return(" ".join(stave))
        else:
            raise TypeError("stave with value {} cannot be printed".format(stave))

    def scale(self, start, stop_or_length, dur=None, key=None, step=1):
        key = self.key if key is None else key
        return scale(start, stop_or_length, key, dur, step)

    def arpeggio(self, start, stop_or_length, dur=None, key=None, step=1):
        key = self.key if key is None else key
        return arpeggio(start, stop_or_length, key, dur, step)

    def arpeggio7(self, start, stop_or_length, dur=None, key=None, step=1):
        key = self.key if key is None else key
        return arpeggio7(start, stop_or_length, key, dur, step)

    def dominant7(self, start, stop_or_length, dur=None, key=None, step=1):
        key = self.key if key is None else key
        return dominant7(start, stop_or_length, key, dur, step)

    def diminished7(self, start, stop_or_length, dur=None, key=None, step=1):
        key = self.key if key is None else key
        return diminished7(start, stop_or_length, key, dur, step)

    def chromatic(self, start, stop_or_length, dur=None, key=None, step=1):
        key = self.key if key is None else key
        return chromatic(start, stop_or_length, key, dur, step)

    def scale_subset(self, positions, start, stop_or_length, dur=None, key=None, step=1):
        key = self.key if key is None else key
        return scale_subset(positions, start, stop_or_length, key, dur, step)

    def transpose(self, item, shift, mode="scale", key=None):
        key = self.key if key is None else key
        return transpose(item, shift, key, mode)

    def harmonize(self, chords, intervals, mode="octave", key=None):
        key = self.key if key is None else keyify(key)
        chords = [chords] if not isinstance(chords, list) else chords
        intervals = [intervals] if not isinstance(intervals, list) else intervals
        mode = [mode] if not isinstance(mode, list) else mode

        max_length = max([len(chords), len(intervals), len(mode)])
        zip_list = zip(range(max_length), cycle(chords), cycle(intervals), cycle(mode))

        for i, chord, interval, mode in zip_list:
            root_tone = chord.tones[0]
            interval = [interval] if not isinstance(interval, list) else interval

            for intrvl in interval:
                if intrvl != 0:
                    new_tone = self.transpose(root_tone, intrvl, mode, key)
                    if new_tone not in chord.tones:
                        chord.tones.append(new_tone)
        return chords

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
