from util import flatten

all_base_letters = ['c', 'd', 'e', 'f', 'g', 'a', 'b']
all_accents = ['ff', 'f', '', 's', 'ss']

all_letters = flatten([[letter + accent for accent in all_accents] for letter in all_base_letters])

all_pitches = [",,,", ",,", ",", "", "`", "``", "```"]
all_tones = flatten([[letter + pitch for letter in all_letters] for pitch in all_pitches] + ['r'])


equivalent_letters = {
    'cf': 'b',
    'c': 'bs',
    'cs': 'df',
    'df': 'cs',
    'd': 'd',
    'ds': 'ef',
    'ef': 'ds',
    'e': 'ff',
    'es': 'f',
    'ff': 'e',
    'f': 'es',
    'fs': 'gf',
    'gf': 'fs',
    'g': 'g',
    'gs': 'af',
    'af': 'gs',
    'a': 'a',
    'as': 'bf',
    'bf': 'as',
    'b': 'cf',
    'bs': 'c'
}


def separate(tone):
    tone = tonify(tone)
    if tone == 'r':
        return 'r', ''
    else:
        if tone[-1] in ["`", ","]:
            split = tone.split(tone[-1], 1)
            return split[0], split[1] + tone[-1]
        else:
            return tone, ''


def tonify(item):
    if isinstance(item, list):
        return [tonify(subitem) for subitem in item]
    elif isinstance(item, str):
        if " " in item:
            return tonify(item.split(" "))
        else:
            if item not in all_tones:
                raise ValueError("{} is not a valid tone.".format(item))
            return item
    else:
        try:
            return item.tone
        except AttributeError:
            raise ValueError("Cannot tonify {}".format(item))
