import util

all_base_letters = ['c', 'd', 'e', 'f', 'g', 'a', 'b']
all_accents = ['ff', 'f', '', 's', 'ss']

all_letters = util.flatten([[letter + accent for accent in all_accents] for letter in all_base_letters])

all_pitches = [",,,", ",,", ",", "", "`", "``", "```"]
all_tones = util.flatten([[letter + pitch for letter in all_letters] for pitch in all_pitches])


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
    if tone[-1] in ["`", ","]:
        split = tone.split(tone[-1], 1)
        return split[0], split[1] + tone[-1]
    else:
        return tone, ''


def pitch(tone):
    return separate(tone)[1]


def letter(tone):
    return separate(tone)[0]


def accent(tone):
    let = letter(tone)
    if len(let) == 1:
        return ''
    else:
        return let[-1]


def base_letter(tone):
    return letter(tone)[0]


def equivalent_tone(tone):
    new_letter = equivalent_letters[letter(tone)]
    if base_letter(tone) == 'c' and base_letter(new_letter) == 'b':
        new_pitch = all_pitches[all_pitches.index(pitch(tone)) - 1]
    elif base_letter(tone) == 'b' and base_letter(new_letter) == 'c':
        new_pitch = all_pitches[all_pitches.index(pitch(tone)) + 1]
    else:
        new_pitch = pitch(tone)
    new_tone = new_letter + new_pitch
    return new_tone


def flatten(tone):
    let = letter(tone)
    if len(let) == 1 or let[-1] == 'f':
        return let + 'f' + pitch(tone)
    else:
        return let[:-1] + pitch(tone)


def sharpen(tone):
    let = letter(tone)
    if len(let) == 1 or let[-1] == 's':
        return let + 's' + pitch(tone)
    else:
        return let[:-1] + pitch(tone)


def tonify(item):
    """ Returns an unflattened list of valid tones and empty lists.

    Multi-tone strings are split into lists of valid tones. A seris of N spaces is
    converted into a seris of N-1 empty lists. These produce rests when assigned to
    Points, but will be erased by flattening the list. """

    if isinstance(item, list):
        return [tonify(subitem) for subitem in item]
    elif isinstance(item, str):
        if " " in item:
            split_tones = item.split(" ")
            split_tones = [tone if tone != '' else [] for tone in split_tones]
            return tonify(split_tones)
        else:
            if item not in all_tones:
                raise ValueError("{} is not a valid tone.".format(item))
            return item
    else:
        try:
            return item.tones
        except AttributeError:
            raise ValueError("Cannot tonify {}".format(item))
