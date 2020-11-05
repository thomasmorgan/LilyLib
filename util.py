from copy import deepcopy


def duplicate(item):
    if isinstance(item, list):
        return [duplicate(i) for i in item]

    elif isinstance(item, str):
        return copy.deepcopy(item)

    else:
        return item.duplicate()


def print_error(message):
    print("*** ERROR ***: {}".format(message))


def flatten(List):
    while any([isinstance(i, list) or isinstance(i, tuple) for i in List]):
        new_list = []
        for i in List:
            if isinstance(i, list) or isinstance(i, tuple):
                new_list += i
            else:
                new_list += [i]
        List = new_list
    return List


def split_and_flatten(item):
    item = flatten([item])
    for subitem in item:
        if not isinstance(subitem, str) and not isinstance(subitem, int):
            raise ValueError("Cannot split and flatten {} as it is not a string or int".format(subitem))

    return flatten([subitem.split(" ") if isinstance(subitem, str) else subitem for subitem in item])


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


def duplicate(item):
    if isinstance(item, list):
        return [duplicate(i) for i in item]

    elif isinstance(item, str):
        return copy.deepcopy(item)

    else:
        return item.duplicate()


def print_error(message):
    print("*** ERROR ***: {}".format(message))


def select(List, *indexes):
    indexes = flatten(list(indexes))
    return [j for i, j in enumerate(List) if (i + 1) in indexes]


def pattern(List, *indexes):
    indexes = flatten(list(indexes))
    new_list = []
    for i in indexes:
        new_list.append(List[i - 1])
    return new_list


def remove(List, *indexes):
    indexes = flatten(list(indexes))
    return [j for i, j in enumerate(List) if (i + 1) not in indexes]


def subset(List, start, stop):
    if stop >= start:
        return List[start - 1:stop]
    else:
        if stop == 1:
            return List[start - 1::-1]
        else:
            return List[start - 1:stop - 2:-1]


def copy(List):
    return [deepcopy(x) for x in List]


def merge(*motifs):
    merged = motifs[0]
    for motif in motifs[1:]:
        for key in merged:
            merged[key] += motif[key]
    return merged


def map_harmony_to_int(harmony):
    if not isinstance(harmony, str):
        return harmony
    if harmony == "1st":
        return 0
    if harmony == "2nd":
        return 1
    if harmony == "3rd":
        return 2
    if harmony == "4th":
        return 3
    if harmony == "5th":
        return 4
    if harmony == "6th":
        return 5
    if harmony == "7th":
        return 6
    if harmony == "8th":
        return 7
    if harmony == "Oct":
        return 7
    if harmony == "1st_":
        return 0
    if harmony == "2nd_":
        return -6
    if harmony == "3rd_":
        return -5
    if harmony == "4th_":
        return -4
    if harmony == "5th_":
        return -3
    if harmony == "6th_":
        return -2
    if harmony == "7th_":
        return -1
    if harmony == "8th_":
        return -7
    if harmony == "Oct_":
        return -7
    raise ValueError()
