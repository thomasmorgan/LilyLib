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


linebreak = ['\\break\n']


def clef(clef):
    return ['\\clef {}'.format(clef)]


def select(List, *indexes):
    indexes = flatten(list(indexes))
    return [j for i, j in enumerate(List) if (i + 1) in indexes]


def pattern(List, *indexes):
    indexes = flatten(list(indexes))
    new_list = []
    for i in indexes:
        new_list.append(List[i - 1])
    return new_list


def omit(List, *indexes):
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
