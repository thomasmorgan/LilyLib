from models import Tone, ToneSpace, Note, Chord, Key
from staves import Treble, Bass
from util import flatten

import keys

from itertools import cycle
from copy import deepcopy
from inspect import isclass


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
        self.tonespace = ToneSpace()
        self.create_key_dictionary()

        self.details()

        self.set_key(self.key)
        print(self)

    def details():
        raise NotImplementedError("You must overwrite details to create a piece")

    def keyify(self, key):
        if key is None:
            return self.key
        elif isinstance(key, Key):
            return key
        elif isclass(key) and issubclass(key, Key):
            return key(self.tonespace)
        elif isinstance(key, str):
            try:
                key = key.split(" ")
                letter = key[0].lower()
                mode = " ".join(key[1:]).lower()
                if 'harmonic' in mode:
                    mode = 'harmonic'
                return self.key_dictionary[mode][letter]
            except Exception:
                raise ValueError("{} is not a valid string format for a key".format(key))
        else:
            raise ValueError("{} is not a valid key".format(key))

    def set_key(self, key):
        self.key = self.keyify(key)

    @property
    def key_signature(self):
        return [str(self.key)]

    def clef(self, clef):
        return ['\\clef {}'.format(clef)]

    def create_key_dictionary(self):
        self.key_dictionary = {
            "major": {
                "cf": keys.CFlatMajor(self.tonespace),
                "c": keys.CMajor(self.tonespace),
                "cs": keys.CSharpMajor(self.tonespace),
                "df": keys.DFlatMajor(self.tonespace),
                "d": keys.DMajor(self.tonespace),
                "ef": keys.EFlatMajor(self.tonespace),
                "e": keys.EMajor(self.tonespace),
                "f": keys.FMajor(self.tonespace),
                "fs": keys.FSharpMajor(self.tonespace),
                "gf": keys.GFlatMajor(self.tonespace),
                "g": keys.GMajor(self.tonespace),
                "af": keys.AFlatMajor(self.tonespace),
                "a": keys.AMajor(self.tonespace),
                "bf": keys.BFlatMajor(self.tonespace),
                "b": keys.BMajor(self.tonespace)
            },
            "minor": {
                "c": keys.CMinor(self.tonespace),
                "cs": keys.CSharpMinor(self.tonespace),
                "d": keys.DMinor(self.tonespace),
                "ds": keys.DSharpMinor(self.tonespace),
                "ef": keys.EFlatMinor(self.tonespace),
                "e": keys.EMinor(self.tonespace),
                "f": keys.FMinor(self.tonespace),
                "fs": keys.FSharpMinor(self.tonespace),
                "g": keys.GMinor(self.tonespace),
                "gs": keys.GSharpMinor(self.tonespace),
                "af": keys.AFlatMinor(self.tonespace),
                "a": keys.AMinor(self.tonespace),
                "as": keys.ASharpMinor(self.tonespace),
                "bf": keys.BFlatMinor(self.tonespace),
                "b": keys.BMinor(self.tonespace)
            },
            "harmonic": {
                "c": keys.CMinorH(self.tonespace),
                "cs": keys.CSharpMinorH(self.tonespace),
                "d": keys.DMinorH(self.tonespace),
                "ds": keys.DSharpMinorH(self.tonespace),
                "ef": keys.EFlatMinorH(self.tonespace),
                "e": keys.EMinorH(self.tonespace),
                "f": keys.FMinorH(self.tonespace),
                "fs": keys.FSharpMinorH(self.tonespace),
                "g": keys.GMinorH(self.tonespace),
                "gs": keys.GSharpMinorH(self.tonespace),
                "af": keys.AFlatMinorH(self.tonespace),
                "a": keys.AMinorH(self.tonespace),
                "as": keys.ASharpMinorH(self.tonespace),
                "bf": keys.BFlatMinorH(self.tonespace),
                "b": keys.BMinorH(self.tonespace)
            }
        }

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
            return " ".join([str(note) for note in flatten([self.score[stave.name]])])

        stave = self.score[stave.name]
        if isinstance(stave, Note) or isinstance(stave, Chord):
            return(str(stave))
        elif isinstance(stave, list):
            stave = [str(s) for s in flatten(stave)]
            return(" ".join(stave))
        else:
            raise TypeError("stave with value {} cannot be printed".format(stave))

    def tones(self, tones):
        tones = flatten([tones])
        tones = flatten([t.split(' ') for t in tones if isinstance(t, str)])
        return [self.key.tonespace.tone_with_string(t) for t in tones]

    def notes(self, tones, dur, ornamentation=""):
        tones = flatten([tones])
        tones = flatten([self.tones(n) if isinstance(n, str) else n for n in tones])
        dur = flatten([dur])
        dur = flatten([d.split(" ") if isinstance(d, str) else d for d in dur])
        orn = flatten([ornamentation])
        orn = flatten([o.split(" ") if isinstance(o, str) and '"' not in o else o for o in orn])

        max_length = max([len(tones), len(dur), len(orn)])

        zip_list = zip(range(max_length), cycle(tones), cycle(dur), cycle(orn))
        return [Note(n, d, o) for i, n, d, o in zip_list]

    def chord(self, tones, dur, ornamentation=""):
        tones = flatten([tones])
        tones = flatten([self.tones(t) if isinstance(t, str) else t for t in tones])
        return Chord(tones, dur, ornamentation)

    def rests(self, dur):
        return self.notes('r', dur)

    def series(self, tones, start, stop_or_length, dur=None, step=1):
        start, stop_or_length = self.validate_series_args(tones, start, stop_or_length, dur, step)

        start_index = tones.index(start)

        if isinstance(stop_or_length, Tone):
            stop_index = tones.index(stop_or_length)
        else:
            if stop_or_length > 0:
                stop_index = start_index + (stop_or_length - 1) * step
            else:
                stop_index = start_index + (stop_or_length + 1) * step

        stop_index = self.make_stop_inclusive(start_index, stop_index)
        if stop_index < start_index:
            step = -step

        series = tones[start_index:stop_index:step]
        if not dur:
            return series
        return self.notes(series, dur)

    def validate_series_args(self, tones, start, stop_or_length, dur, step):
        if not isinstance(tones, list):
            raise ValueError("series arg tones cannot be {}, it must be a list".format(tones))

        for t in tones:
            if not isinstance(t, Tone):
                raise ValueError("series arg tones cannot contain {}, it must be a list of tones".format(t))

        start = self.tonify(start)
        if start not in tones:
            raise ValueError("Cannot start series on {} as it it not in tones: {}.".format(start, [str(t) for t in tones]))

        if not isinstance(stop_or_length, int):
            stop_or_length = self.tonify(stop_or_length)
            if stop_or_length not in tones:
                raise ValueError("Cannot stop series on {} as it it not in tones: {}.".format(stop_or_length, [str(t) for t in tones]))

        if not isinstance(step, int):
            raise ValueError("series step must be an int, not {}".format(step))

        return start, stop_or_length

    def tonify(self, item):
        if isinstance(item, Note):
            return item.tone
        if isinstance(item, Tone):
            return item
        if isinstance(item, str):
            return self.tonespace.tone_with_string(item)
        raise ValueError("Cannot tonify {}, can only tonify Notes, Tones and strings".format(item))

    def make_stop_inclusive(self, start, stop):
        if stop >= start:
            return stop + 1
        else:
            return stop - 1

    def scale(self, start, stop_or_length, dur=None, key=None, step=1):
        key = self.keyify(key)
        return self.series(key.tones, start, stop_or_length, dur, step)

    def arpeggio(self, start, stop_or_length, dur=None, key=None, step=1):
        key = self.keyify(key)
        return self.series(key.arpeggio_tones, start, stop_or_length, dur, step)

    def arpeggio7(self, start, stop_or_length, dur=None, key=None, step=1):
        key = self.keyify(key)
        arpeggio7_tones = key.scale_subset([1, 3, 5, 7])
        return self.series(arpeggio7_tones, start, stop_or_length, dur, step)

    def dominant7(self, start, stop_or_length, dur=None, key=None, step=1):
        key = self.keyify(key)
        dominant7_letters = key.arpeggio_letters + [key.relative_chromatic_letter(10)]
        dominant7_tones = [t for t in key.all_tones if t.letter in dominant7_letters]
        return self.series(dominant7_tones, start, stop_or_length, dur, step)

    def diminished7(self, start, stop_or_length, dur=None, key=None, step=1):
        key = self.keyify(key)
        diminished7_letters = [key.relative_chromatic_letter(i) for i in [0, 3, 6, 9]]
        diminished7_tones = [t for t in key.all_tones if t.letter in diminished7_letters]
        return self.series(diminished7_tones, start, stop_or_length, dur, step)

    def chromatic(self, start, stop_or_length, dur=None, key=None, step=1):
        key = self.keyify(key)
        return self.series(key.all_tones, start, stop_or_length, dur, step)

    def scale_subset(self, positions, start, stop_or_length, dur=None, key=None, step=1):
        key = self.keyify(key)
        custom_tones = key.scale_subset(positions)
        return self.series(custom_tones, start, stop_or_length, dur, step)

    def transpose(self, item, shift, mode="octave"):
        self.validate_transpose_args(shift, mode)

        if isinstance(item, Tone):
            if item.letter == 'r':
                return item

            if mode == "octave":
                new_pitch = self.key.tonespace.all_pitches[self.key.tonespace.all_pitches.index(item.pitch) + shift]
                new_tone_string = item.letter + new_pitch
                item = self.key.tonespace.tone_with_string(new_tone_string)
            elif mode == "scale":
                current_index = self.key.tones.index(item)
                item = self.key.tones[current_index + shift]
            elif mode == "semitone":
                item = self.key.all_tones[self.key.all_tones.index(item) + shift]
            return item

        elif isinstance(item, Note):
            return Note(self.transpose(item.tone, shift, mode), item.dur, item.ornamentation)

        elif isinstance(item, Chord):
            return Chord(self.transpose(item.tones, shift, mode), item.dur, item.ornamentation)

        elif isinstance(item, list):
            return [self.transpose(subitem, shift, mode) for subitem in item]

        elif isinstance(item, dict):
            new_dict = {}
            for key in item:
                new_dict[key] = self.transpose(item[key], shift, mode)
            return new_dict

        elif isinstance(item, str):
            try:
                return " ".join([str(t) for t in self.transpose(self.tones(item), shift, mode)])
            except Exception:
                return item

        else:
            raise ValueError("Cannot transpose {} as it is a {}".format(item, type(item)))

    def validate_transpose_args(self, shift, mode):
        if not isinstance(shift, int):
            raise ValueError("{} is not a valid shift for piece.transpose(), it must be an int".format(shift))
        if mode not in ["octave", "scale", "semitone"]:
            raise ValueError("{} is not a valid mode for piece.transpose()".format(mode))

    def harmonize(self, notes, intervals, mode="octave"):
        chords = []
        if not isinstance(notes, list):
            notes = [notes]
        if not isinstance(intervals, list):
            intervals = [intervals]
        if not isinstance(mode, list):
            mode = [mode]
        max_length = max([len(notes), len(intervals), len(mode)])
        zip_list = zip(range(max_length), cycle(notes), cycle(intervals), cycle(mode))
        for i, note, interval, mode in zip_list:
            chord = [note]
            if not isinstance(interval, list):
                interval = flatten([interval])
            for intrvl in interval:
                if intrvl != 0:
                    chord.append(self.transpose(note, intrvl, mode))
            chords.append(self.chord([c.tone for c in chord], note.dur, note.ornamentation))
        return chords

    def triplets(self, notes):
        return ['\\tuplet 3/2 {'] + notes + ['}']

    def grace(self, notes):
        return ['\\grace {'] + notes + ['}']

    def ottava(self, notes, shift):
        return ['\\ottava #{}'.format(shift)] + notes + ['\\ottava #0']

    def voices(self, *voices):
        score = ["<<\n"]
        for i, voice in enumerate(voices):
            score.extend(["{"] + voice + ["}\n"])
            if i < (len(voices) - 1):
                score += ["\\\\\n"]
        score += [">>\n"]
        return score

    def repeat(self, notes, times=2):
        if times > 2:
            notes[-1].ornamentation += '^"x' + str(times) + '"'
        return ["\\repeat volta " + str(times) + '{'] + notes + ['}']

    def annotation(self, text):
        return '^"' + text + '" '

    def name(self, notes, name):
        index = next(i for i, note in enumerate(notes) if isinstance(note, Note) or isinstance(note, Chord))
        notes[index] = deepcopy(notes[index])
        notes[index].ornamentation += ('^"' + name + '"')

    def tempo_change(self, tempo):
        return ["\\time {}".format(tempo)]

    def relative_key(self, mode, relationship):
        my_root = self.key.root
        index_of_my_root = self.key.letters.index(my_root)
        new_index = index_of_my_root + relationship
        new_root = (self.key.letters * 2)[new_index]

        try:
            return self.key_dictionary[mode][new_root]
        except KeyError:
            try:
                new_root2 = self.key.tonespace.equivalent_letters[new_root]
                return self.key_dictionary[mode][new_root2]
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
