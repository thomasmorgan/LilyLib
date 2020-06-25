def all_tones():
    from models import Tone
    all_tones = []
    for p in [",,,", ",,", ",", "", "`", "``", "```"]:
        for l in ['c', 'd', 'e', 'f', 'g', 'a', 'b']:
            for a in ['ff', 'f', '', 's', 'ss']:
                all_tones.append(Tone(l + a + p))
    return all_tones


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
