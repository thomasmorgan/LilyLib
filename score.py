from models import Note, Chord
from staves import Treble, Bass
from keys import CMajor
from util import flatten


class Score:

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
            printed_score += self.print_stave(stave.name)
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

    def print_stave(self, name):
        stave = self.score[name]
    def create_sections(self, *sections):
        self.sections = sections
        for stave in self.staves:
            self.score[stave.name] = {}
            for section in sections:
                self.score[stave.name][section] = ""

        if isinstance(stave, Note) or isinstance(stave, Chord):
            return(str(stave))
        elif isinstance(stave, list):
            stave = [str(s) for s in flatten(stave)]
            return(" ".join(stave))
        else:
            raise TypeError("stave with value {} cannot be printed".format(stave))
