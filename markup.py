from util import flatten

linebreak = '\\break\n'

pagebreak = '\\pageBreak\n\n'


def clef(clef, passage):
    passage = flatten([passage])
    passage[0].prefix = '\\clef {} '.format(clef) + passage[0].prefix
    return passage


def time_signature(tempo, passage):
    passage = flatten([passage])
    passage[0].prefix = '\\time {} '.format(tempo) + passage[0].prefix
    return passage


def triplets(passage):
    passage = flatten([passage])
    passage[0].prefix = '\\tuplet 3/2 {' + passage[0].prefix
    passage[-1].suffix += '}'
    return passage


def grace(passage):
    passage = flatten([passage])
    passage[0].prefix = '\\grace {' + passage[0].prefix
    passage[-1].suffix += '}'
    return passage


def after_grace(passage, grace):
    passage = flatten([passage])
    grace = flatten([grace])
    passage[0].prefix = '\\afterGrace {' + passage[0].prefix
    grace[0].prefix = '{' + passage[0].grace
    grace[-1].suffix += '}'
    return passage + grace


def acciaccatura(passage):
    passage = flatten([passage])
    passage[0].prefix = '\\acciaccatura {' + passage[0].prefix
    passage[-1].suffix += '}'
    return passage


def ottava(passage, shift):
    passage = flatten([passage])
    passage[0].prefix + '\\ottava #{}'.format(shift) + passage[0].prefix
    passage[-1].suffix += '\\ottava #0 '
    return passage


def voices(*voices):
    for i, voice in enumerate(voices):
        voice[0].prefix = "{" + voice[0].prefix
        voice[-1].suffix += "}"
        if i < (len(voices) - 1):
            voice[-1].suffix += "\\\\\n"
    voices[0][0].prefix = "<<\n" + voices[0][0].prefix
    voices[-1][-1].suffix += ">>\n"
    passage = []
    for voice in voices:
        passage += voice
    return passage


def repeat(passage, times=2):
    passage = flatten([passage])
    passage[0].prefix = "\\repeat volta " + str(times) + '{' + passage[0].prefix
    if times > 2:
        passage[-1].suffix += '^"x' + str(times) + '"'
    passage[-1].suffix += '}'
    return passage
