from models import Note, Chord, Key
from staves import Treble, Bass
from keys import CMajor
from util import flatten


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

    def __str__(self):
        printed_score = self.header() + self.start_score()
        for stave in self.staves:
            printed_score += stave.start
            printed_score += str(self.key)
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

    def notes(self, notes, dur):
        notes = flatten([notes])
        new_notes = []
        for note in notes:
            if isinstance(note, str):
                note = note.split(" ")
                for n in note:
                    new_notes.append(Note(n, dur))
            else:
                new_notes.append(Note(note, dur))
        return new_notes

    def scale(self, start, stop, key=None, dur=None):
        if isinstance(start, Note):
            start = str(start)
        if isinstance(stop, Note):
            stop = str(stop)

        if key is None:
            key = self.key
        elif isinstance(key, Key):
            pass
        elif issubclass(key, Key):
            key = key()
        else:
            raise ValueError("Cannot create scale in key {}".format(key))

        scale = key.scale(start=start, stop=stop)

        if dur is not None:
            scale = [Note(tone, dur) for tone in scale]

        return scale