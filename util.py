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
