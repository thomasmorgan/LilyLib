from lilylib import Point
from copy import deepcopy

linebreak = ['\\break\n']


def clef(clef):
    return ['\\clef {}'.format(clef)]


def triplets(passage):
    return ['\\tuplet 3/2 {'] + passage + ['}']


def grace(passage):
    return ['\\grace {'] + passage + ['}']


def after_grace(passage, grace):
    return ['\\afterGrace'] + passage + ['{'] + grace + ['}']


def acciaccatura(passage):
    return ['\\acciaccatura {'] + passage + ['}']


def ottava(passage, shift):
    return ['\\ottava #{}'.format(shift)] + passage + ['\\ottava #0']


def voices(*voices):
    score = ["<<\n"]
    for i, voice in enumerate(voices):
        score.extend(["{"] + voice + ["}\n"])
        if i < (len(voices) - 1):
            score += ["\\\\\n"]
    score += [">>\n"]
    return score


def repeat(passage, times=2):
    if times > 2:
        passage[-1].ornamentation += '^"x' + str(times) + '"'
    return ["\\repeat volta " + str(times) + '{'] + passage + ['}']


def annotation(text):
    return '^"' + text + '" '


def name(passage, name):
    index = next(i for i, point in enumerate(passage) if isinstance(point, Point))
    passage[index] = deepcopy(passage[index])
    passage[index].ornamentation += ('^"' + name + '"')


def tempo_change(tempo):
    return ["\\time {}".format(tempo)]
