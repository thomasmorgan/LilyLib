from models import Tone, Note, Chord, Key
from staves import Treble, Bass
from keys import CMajor
from util import flatten, all_pitches

from itertools import cycle
from copy import deepcopy


class Piece:

    def __init__(self):
        self.title = ""
        self.subtitle = ""
        self.composer = ""
        self.opus = ""
        self.staves = [Treble(), Bass()]
        self.tempo = "4/4"
        self.key = CMajor()
        self.score = {}
        self.details()
        print(self)

    def details():
        raise NotImplementedError("You must overwrite details to create a piece")

    def write_score(self):
        raise NotImplementedError("You must overwrite write_score to create a piece")

    def __str__(self):
        printed_score = self.header() + self.start_score()
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
        return [Tone(t) for t in tones]

    def notes(self, notes, dur, ornamentation=""):
        notes = flatten([notes])
        notes = flatten([self.tones(n) if isinstance(n, str) else n for n in notes])
        dur = flatten([dur])
        dur = flatten([d.split(" ") if isinstance(d, str) else d for d in dur])
        orn = flatten([ornamentation])
        orn = flatten([o.split(" ") if isinstance(o, str) else o for o in orn])

        max_length = max([len(notes), len(dur), len(orn)])

        zip_list = zip(range(max_length), cycle(notes), cycle(dur), cycle(orn))
        return [Note(n, d, o) for i, n, d, o in zip_list]

    def rests(self, dur):
        return self.notes('r', dur)

    def series(self, tones, start, stop_or_length, dur=None, step=1):
        try:
            start_index = [str(t) for t in tones].index(str(start))
        except ValueError:
            raise ValueError("Cannot start series on {} as it it not in tones: {}.".format(str(start), [str(t) for t in tones]))

        if isinstance(stop_or_length, int):
            stop_index = start_index + (stop_or_length - 1) * step
        else:
            try:
                stop_index = [str(t) for t in tones].index(str(stop_or_length))
            except ValueError:
                raise ValueError("{} is not a valid stop for tone series {}.".format(str(stop_or_length), [str(t) for t in tones]))

        if not isinstance(step, int):
            raise ValueError("series step must be an int, not {}".format(step))

        if stop_index >= start_index:
            stop_index += 1
        elif stop_index < start_index:
            stop_index -= 1
            step *= -1

        series = tones[start_index:stop_index:step]

        if dur is not None:
            series = [Note(tone, dur) for tone in series]

        return series

    def keyify(self, key):
        if key is None:
            key = self.key
        elif issubclass(key, Key):
            key = key()
        else:
            raise ValueError("{} is not a valid key".format(key))

        return key

    def scale(self, start, stop_or_length, key=None, dur=None, step=1):
        key = self.keyify(key)
        return self.series(key.tones, start, stop_or_length, dur, step)

    def arpeggio(self, start, stop_or_length, key=None, dur=None, step=1):
        key = self.keyify(key)
        return self.series(key.arpeggio_tones, start, stop_or_length, dur, step)

    def arpeggio7(self, start, stop_or_length, key=None, dur=None, step=1):
        key = self.keyify(key)
        arpeggio7_tones = key.scale_subset([1, 3, 5, 7])
        return self.series(arpeggio7_tones, start, stop_or_length, dur, step)

    def chromatic(self, start, stop_or_length, key=None, dur=None, step=1):
        key = self.keyify(key)
        return self.series(key.all_tones, start, stop_or_length, dur, step)

    def scale_subset(self, positions, start, stop_or_length, key=None, dur=None, step=1):
        key = self.keyify(key)
        custom_tones = key.scale_subset(positions)
        return self.series(custom_tones, start, stop_or_length, dur, step)

    def transpose(self, notes, shift, mode="octave"):
        if not isinstance(shift, int):
            raise ValueError("{} is not a valid shift for piece.transpose(), it must be an int".format(shift))
        if mode not in ["octave", "scale", "semitone"]:
            raise ValueError("{} is not a valid mode for piece.transpose()".format(mode))

        notes = deepcopy(notes)

        if isinstance(notes, list):
            for i, n in enumerate(notes):
                notes[i] = self.transpose(n, shift, mode)

        elif isinstance(notes, Chord):
            for i, n in enumerate(notes.notes):
                notes.notes[i] = self.transpose(n, shift, mode)

        elif isinstance(notes, Note):
            notes.tone = self.transpose(notes.tone, shift, mode)

        elif isinstance(notes, Tone):
            if mode == "octave":
                notes.pitch = all_pitches()[all_pitches().index(notes.pitch) + shift]
            elif mode == "scale":
                notes = self.key.tones[self.key.tones.index(notes) + shift]
            elif mode == "semitone":
                notes = self.key.all_tones[self.key.all_tones.index(notes) + shift]

        return notes

    def triplets(self, notes):
        return ['\\tuplet 3/2 {'] + notes + ['}']

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

    def name(self, notes, name):
        index = next(i for i, note in enumerate(notes) if isinstance(note, Note) or isinstance(note, Chord))
        notes[index] = deepcopy(notes[index])
        notes[index].ornamentation += ('^"' + name + '"')

    def tempo_change(self, tempo):
        return ["\\time {}".format(tempo)]
