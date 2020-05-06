from models import Tone, Note, Chord, Key
from staves import Treble, Bass
from keys import CMajor
from util import flatten

from itertools import cycle


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

    def create_sections(self, *sections):
        self.sections = sections
        for stave in self.staves:
            self.score[stave.name] = {}
            for section in sections:
                self.score[stave.name][section] = ""

    def print_stave(self, stave):
        if type(self.score[stave.name]) is dict:
            return " ".join([str(note) for note in flatten([self.score[stave.name][section] for section in self.sections])])

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

    def notes(self, notes, dur):
        notes = flatten([notes])
        notes = flatten([self.tones(n) if isinstance(n, str) else n for n in notes])
        dur = flatten([dur])
        zip_list = zip(notes, cycle(dur)) if len(notes) > len(dur) else zip(cycle(notes), dur)
        return [Note(n, d) for n, d in zip_list]

    def rests(self, dur):
        return self.notes('r', dur)

    def series(self, mode, start, stop_or_length, key=None, dur=None, step=1, root=None):
        if key is None:
            key = self.key
        elif isinstance(key, Key):
            pass
        elif issubclass(key, Key):
            key = key()
        else:
            raise ValueError("Cannot create {} in key {}".format(mode, key))

        series = key.series(mode=mode, start=start, stop_or_length=stop_or_length, step=step, root=root)

        if dur is not None:
            series = [Note(tone, dur) for tone in series]

        return series

    def scale(self, start, stop_or_length, key=None, dur=None, step=1):
        return self.series("scale", start, stop_or_length, key, dur, step)

    def arpeggio(self, start, stop_or_length, key=None, dur=None, step=1, root=None):
        return self.series("arpeggio", start, stop_or_length, key, dur, step, root)

    def chromatic(self, start, stop_or_length, key=None, dur=None, step=1):
        return self.series("chromatic", start, stop_or_length, key, dur, step)
