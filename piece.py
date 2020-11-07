from models import Note, Chord, Key
from keys import key_dictionary
from staves import Treble, Bass
from util import flatten, split_and_flatten, all_tones, tonify, all_pitches, separate, equivalent_letters, pitch, letter, equivalent_tone

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
            return key()
        elif isinstance(key, str):
            try:
                key = key.split(" ")
                letter = key[0].lower()
                mode = " ".join(key[1:]).lower()
                if 'harmonic' in mode:
                    mode = 'harmonic'
                return key_dictionary[mode][letter]
            except Exception:
                raise ValueError("{} is not a valid string format for a key".format(key))
        else:
            raise ValueError("{} is not a valid key".format(key))

    def set_key(self, key):
        self.key = self.keyify(key)

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
            return " ".join([str(note) for note in flatten([self.score[stave.name]])])

        stave = self.score[stave.name]
        if isinstance(stave, Note) or isinstance(stave, Chord):
            return(str(stave))
        elif isinstance(stave, list):
            stave = [str(s) for s in flatten(stave)]
            return(" ".join(stave))
        else:
            raise TypeError("stave with value {} cannot be printed".format(stave))

    def notes(self, tones, dur, ornamentation=""):
        tones = flatten([tonify(tones)])
        dur = split_and_flatten(dur)
        orn = split_and_flatten(ornamentation) if '"' not in ornamentation else flatten([ornamentation])

        max_length = max([len(tones), len(dur), len(orn)])

        zip_list = zip(range(max_length), cycle(tones), cycle(dur), cycle(orn))
        return [Note(n, d, o) for i, n, d, o in zip_list]

    def chord(self, tones, dur, ornamentation=""):
        tones = flatten([tonify(tones)])
        return [Chord(tones, dur, ornamentation)]

    def rests(self, dur):
        return self.notes('r', dur)

    def series(self, tones, start, stop_or_length, dur=None, step=1):
        tones = tonify(tones)
        start, stop_or_length = self.validate_series_args(tones, start, stop_or_length, dur, step)

        start_index = tones.index(start)

        if isinstance(stop_or_length, str):
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
            if not isinstance(t, str):
                raise ValueError("series arg tones cannot contain {}, it must be a list of strings".format(t))
            if t not in all_tones:
                raise ValueError("series arg tones cannot contain {}, it is not a valid tone".format(t))

        start = tonify(start)
        if start not in tones:
            raise ValueError("Cannot start series on {} as it it not in tones: {}.".format(start, [str(t) for t in tones]))

        if not isinstance(stop_or_length, int):
            stop_or_length = tonify(stop_or_length)
            if stop_or_length not in tones:
                raise ValueError("Cannot stop series on {} as it it not in tones: {}.".format(stop_or_length, [str(t) for t in tones]))

        if not isinstance(step, int):
            raise ValueError("series step must be an int, not {}".format(step))

        return start, stop_or_length

    def add(self, chords, tones):
        tones = flatten([tonify(tones)])
        chords = flatten([chords])
        for c in chords:
            if isinstance(c, Chord):
                for t in tones:
                    if t not in c.tones:
                        c.tones.append(t)

    def remove(self, chords, tones):
        tones = flatten(tonify(tones))
        chords = flatten([chords])
        for c in chords:
            if isinstance(c, Chord):
                c.tones = [t for t in c.tones if t not in tones]

    def replace(self, item, old, new):
        if isinstance(item, list):
            for subitem in item:
                self.replace(subitem, old, new)
        elif isinstance(item, Note):
            if item.tone == old:
                item.tone = tonify(new)
        elif isinstance(item, Chord):
            if old in item.tones:
                self.remove(item, old)
                self.add(item, new)

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
        dominant7_tones = [t for t in key.all_tones if separate(t)[0] in dominant7_letters]
        return self.series(dominant7_tones, start, stop_or_length, dur, step)

    def diminished7(self, start, stop_or_length, dur=None, key=None, step=1):
        key = self.keyify(key)
        diminished7_letters = [key.relative_chromatic_letter(i) for i in [0, 3, 6, 9]]
        diminished7_tones = [t for t in key.all_tones if separate(t)[0] in diminished7_letters]
        return self.series(diminished7_tones, start, stop_or_length, dur, step)

    def chromatic(self, start, stop_or_length, dur=None, key=None, step=1):
        key = self.keyify(key)
        return self.series(key.all_tones, start, stop_or_length, dur, step)

    def scale_subset(self, positions, start, stop_or_length, dur=None, key=None, step=1):
        key = self.keyify(key)
        custom_tones = key.scale_subset(positions)
        return self.series(custom_tones, start, stop_or_length, dur, step)

    def transpose(self, item, shift, mode="octave", key=None):
        self.validate_transpose_args(shift, mode)

        key = self.keyify(key)

        if isinstance(item, dict):
            new_dict = {}
            for key in item:
                new_dict[key] = self.transpose(item[key], shift, mode)
            return new_dict

        elif isinstance(item, list):
            return [self.transpose(subitem, shift, mode, key) for subitem in item]

        elif isinstance(item, Chord):
            return Chord(self.transpose(item.tones, shift, mode, key), item.dur, item.ornamentation)

        elif isinstance(item, Note):
            return Note(self.transpose(item.tone, shift, mode, key), item.dur, item.ornamentation)

        elif item == 'r':
            return item

        elif isinstance(item, str):
            try:
                item = tonify(item)
            except ValueError:
                return item
            if isinstance(item, list):
                return self.transpose(item, shift, mode, key)
            else:
                try:
                    if mode == "octave":
                        new_pitch = all_pitches[all_pitches.index(pitch(item)) + shift]
                        return letter(item) + new_pitch
                    elif mode == "scale":
                        current_index = key.tones.index(item)
                        return key.tones[current_index + shift]
                    elif mode == "semitone":
                        return key.all_tones[key.all_tones.index(item) + shift]
                except ValueError:
                    return self.transpose(equivalent_tone(item), shift, mode, key)

        else:
            raise ValueError("Cannot transpose {} as it is a {}".format(item, type(item)))

    def validate_transpose_args(self, shift, mode):
        if not isinstance(shift, int):
            raise ValueError("{} is not a valid shift for piece.transpose(), it must be an int".format(shift))
        if mode not in ["octave", "scale", "semitone"]:
            raise ValueError("{} is not a valid mode for piece.transpose()".format(mode))

    def harmonize(self, notes, intervals, mode="octave", key=None):
        key = self.keyify(key)
        chords = []
        notes = [notes] if not isinstance(notes, list) else notes
        intervals = [intervals] if not isinstance(intervals, list) else intervals
        mode = [mode] if not isinstance(mode, list) else mode

        max_length = max([len(notes), len(intervals), len(mode)])
        zip_list = zip(range(max_length), cycle(notes), cycle(intervals), cycle(mode))

        for i, note, interval, mode in zip_list:
            root = note.tone if isinstance(note, Note) else note
            tones = [root]
            interval = [interval] if not isinstance(interval, list) else interval

            for intrvl in interval:
                if intrvl != 0:
                    new_tone = self.transpose(root, intrvl, mode, key)
                    if new_tone not in tones:
                        tones.append(new_tone)
            chords += self.chord(tones, note.dur, note.ornamentation)
        return chords

    def triplets(self, notes):
        return ['\\tuplet 3/2 {'] + notes + ['}']

    def grace(self, notes):
        return ['\\grace {'] + notes + ['}']

    def acciaccatura(self, notes):
        return ['\\acciaccatura {'] + notes + ['}']

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
