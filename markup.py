from util import flatten
from copy import deepcopy
from keys import keyify

linebreak = '\\break\n'

nolinebreak = '\\noBreak'

pagebreak = '\\pageBreak\n\n'

barbreak = ' \\bar "|" %{ bar %}\n'

thick_barbreak = ' \\bar "." %{ bar %}\n'

double_barbreak = ' \\bar "||" %{ bar %}\n'

thickthin_barbreak = ' \\bar ".|" %{ bar %}\n'

doublethick_barbreak = ' \\bar ".." %{ bar %}\n'

triple_barbreak = ' \\bar "|.|" %{ bar %}\n'

thinthick_barbreak = ' \\bar "|." %{ bar %}\n'

signe = '\\mark \\markup { \\musicglyph #"scripts.segno" } '


def italic(text):
    return('\\italic{' + text + '}')


def bold(text):
    return('\\bold{' + text + '}')


def clef(clef, passage, end_clef=""):
    passage = deepcopy(passage)
    passage = flatten([passage])
    passage[0].prefix = '\\clef {} '.format(clef) + passage[0].prefix
    if end_clef:
        passage[-1].suffix += '\\clef {} '.format(end_clef)
    return passage


def time_signature(tempo, passage, end_tempo=""):
    passage = deepcopy(passage)
    passage = flatten([passage])
    passage[0].prefix = '\\time {} '.format(tempo) + passage[0].prefix
    if end_tempo:
        passage[-1].suffix += '\\time {} '.format(end_tempo)
    return passage


def key_signature(key1, passage, key2=""):
    passage = deepcopy(passage)
    passage = flatten([passage])
    passage[0].prefix = str(keyify(key1)) + passage[0].prefix
    if key2:
        passage[-1].suffix += str(keyify(key2))
    return passage


def triplets(passage, omit_number=False):
    passage = deepcopy(passage)
    passage = flatten([passage])
    passage[0].prefix = '\\tuplet 3/2 {' + passage[0].prefix
    if omit_number:
        passage[0].prefix = '\\omit TupletNumber ' + passage[0].prefix
    passage[-1].suffix += '} %{ end triplets %}'
    return passage


def quintuplets(passage, omit_number=False):
    passage = deepcopy(passage)
    passage = flatten([passage])
    passage[0].prefix = '\\tuplet 5/4 {' + passage[0].prefix
    if omit_number:
        passage[0].prefix = '\\omit TupletNumber ' + passage[0].prefix
    passage[-1].suffix += '} %{ end quintuplets %}'
    return passage


def sustain(passage):
    passage = deepcopy(passage)
    passage = flatten([passage])
    passage[0].suffix += '\\sustainOn '
    passage[-1].suffix += '\\sustainOff '
    return passage


def grace(passage):
    passage = deepcopy(passage)
    passage = flatten([passage])
    passage[0].prefix = '\\grace {' + passage[0].prefix
    passage[-1].suffix += '} %{ end grace %}'
    return passage


def after_grace(passage, grace):
    passage = deepcopy(passage)
    grace = deepcopy(grace)
    passage = flatten([passage])
    grace = flatten([grace])
    passage[0].prefix = '\\afterGrace {' + passage[0].prefix
    passage[-1].suffix += ' } %{ end after grace passage %} '
    grace[0].prefix = ' %{ start after grace %}{' + grace[0].prefix
    grace[-1].suffix += '} %{ end after grace %}'
    return passage + grace


def acciaccatura(passage):
    passage = deepcopy(passage)
    passage = flatten([passage])
    passage[0].prefix = '\\acciaccatura {' + passage[0].prefix
    passage[-1].suffix += '} %{ end acciaccatura %}'
    return passage


def ottava(passage, shift):
    passage = deepcopy(passage)
    passage = flatten([passage])
    passage[0].prefix = '\\ottava #{} '.format(shift) + passage[0].prefix
    passage[-1].suffix += '\\ottava #0 '
    return passage


def slur(passage):
    passage = deepcopy(flatten([passage]))
    if passage[0].phrasing == '':
        passage[0].phrasing = '('
    else:
        passage[0].phrasing += '('
    if passage[-1].phrasing == '':
        passage[-1].phrasing = ')'
    else:
        passage[-1].phrasing += ')'
    return passage


def phrase(passage):
    passage = deepcopy(flatten([passage]))
    if passage[0].ornamentation == '':
        passage[0].ornamentation = '('
    else:
        passage[0].ornamentation += '\\('
    if passage[-1].ornamentation == '':
        passage[-1].ornamentation = ')'
    else:
        passage[-1].ornamentation += '\\)'
    return passage


def crescendo(passage, end=''):
    passage = deepcopy(flatten([passage]))
    passage[0].dynamics = '<'
    if end:
        passage[-1].dynamics = end
    else:
        passage[-1].dynamics = '!'
    return passage


def diminuendo(passage, end=''):
    passage = deepcopy(flatten([passage]))
    passage[0].dynamics = '>'
    if end:
        passage[-1].dynamics = end
    else:
        passage[-1].dynamics = '!'
    return passage


def voices(*voices):
    voices = [deepcopy(voice) for voice in voices]
    for i, voice in enumerate(voices):
        voice = flatten(voice)
        voice[0].prefix = "{ " + voice[0].prefix
        voice[-1].suffix += " }"
        if i < (len(voices) - 1):
            voice[-1].suffix += "\n\\\\\n"
    flatten(voices[0])[0].prefix = "\n<<\n" + flatten(voices[0])[0].prefix
    flatten(voices[-1])[-1].suffix += "\n>>\n"
    passage = []
    for voice in voices:
        passage += voice
    return passage


def repeat(passage, times=2):
    passage = deepcopy(passage)
    passage = flatten([passage])
    passage[0].prefix = (
        "\\repeat volta " + str(times) + '{' + passage[0].prefix)
    if times > 2:
        passage[-1].suffix += '^"x' + str(times) + '"'
    passage[-1].suffix += '}'
    return passage
