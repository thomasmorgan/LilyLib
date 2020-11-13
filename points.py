from util import flatten, split_and_flatten
from tones import tonify, separate, all_pitches, pitch, letter, equivalent_tone, all_tones, all_durs
from keys import keyify

from itertools import cycle


class Point:
    """ An element in sheet music with a specified duration.
        Prints as either a rest, note or chord."""

    def __init__(self, tones, dur, ornamentation=""):
        self.check_init_arguments(tones, dur, ornamentation)
        self.tones = tones
        self.dur = dur
        self.ornamentation = ornamentation

    def check_init_arguments(self, tones, dur, ornamentation):
        if not isinstance(tones, list):
            raise ValueError("Cannot create Point with {} as tones. tones must be a list.".format(tones))
        for t in tones:
            if t not in all_tones:
                raise ValueError("Cannot create Point with tones containing {} as it is not a valid tone.".format(t))
        if dur not in all_durs:
            raise ValueError("Cannot create Point with {} as dur. dur must be one of {}.".format(dur, all_durs))
        if not isinstance(ornamentation, str):
            raise ValueError("Cannot create Point with {} as ornamentation. ornamentation must be a string.".format(ornamentation))

    def __str__(self):
        if self.is_rest:
            return 'r' + str(self.dur) + self.ornamentation
        elif self.is_note:
            return self.tone + str(self.dur) + self.ornamentation
        elif self.is_chord:
            return "<" + " ".join(self.tones) + ">" + str(self.dur) + self.ornamentation
        else:
            raise ValueError("Cannot print {} as it is neither a rest, nor note, nor chord. Its tones are {}".format(self, self.tones))

    @property
    def tone(self):
        if len(self.tones) == 1:
            return self.tones[0]
        else:
            raise AttributeError("Cannot get {}.tone as it has multiple tones: {}".format(self, self.tones))

    @property
    def letter(self):
        return letter(self.tone)

    @property
    def pitch(self):
        return pitch(self.tone)

    @property
    def is_rest(self):
        return len(self.tones) == 0

    @property
    def is_note(self):
        return len(self.tones) == 1

    @property
    def is_chord(self):
        return len(self.tones) > 1

    def add(self, tones):
        tones = flatten([tonify(tones)])
        for tone in tones:
            if tone not in self.tones:
                self.tones.append(tone)

    def remove(self, tones):
        tones = flatten([tonify(tones)])
        self.tones = [tone for tone in self.tones if tone not in tones]

    def replace(self, old_tones, new_tones):
        old_tones = flatten([tonify(old_tones)])
        new_tones = tonify(new_tones)
        new_tones = new_tones if isinstance(new_tones, list) else [new_tones]

        max_length = max(len(old_tones), len(new_tones))
        zip_list = zip(range(max_length), cycle(old_tones), cycle(new_tones))

        for i, old_tone, new_tone in zip_list:
            if old_tone in self.tones:
                self.remove(old_tone)
                self.add(new_tone)


def rest(dur):
    """ Returns a list with a single Point that prints as a rest with the specified duration. """
    return [Point([], dur)]


def rests(*dur):
    """ Returns a list of Points that print as rests with the specified durations. """
    return flatten([rest(d) for d in flatten(dur)])


def note(tone, dur, ornamentation=""):
    """ Returns a list with a single Point that prints as a note with the specified tone and duration.
    Passing an empty string or list as tone will return a rest.
    Passing a list of tones (or a string that can be split into multiple tones raises an error. """
    tone = flatten([tonify(tone)])
    if len(tone) > 1:
        raise ValueError("Cannot create single note with tone of {}.".format(tone))
    return [Point(tone, dur, ornamentation)]


def notes(tones, dur, ornamentation=""):
    """ Returns a list of Points that print as notes with the specified tone(s) and duration(s).
    If tones is a string including adjacent white space, rests are produced.
    If tones is a list including empty lists or empty strings, rests are produced.
    Nested lists of tones are not permitted as tones will not be flattened to avoid removing empty lists."""
    tones = tonify(tones)
    tones = [tones] if isinstance(tones, str) else tones
    dur = split_and_flatten(dur)
    orn = split_and_flatten(ornamentation) if '"' not in ornamentation else flatten([ornamentation])

    max_length = max([len(tones), len(dur), len(orn)])

    zip_list = zip(range(max_length), cycle(tones), cycle(dur), cycle(orn))
    return flatten([note(t, d, o) for i, t, d, o in zip_list])


def chord(tones, dur, ornamentation=""):
    """ Returns a list containing a single Point that prints as a chord with the specified tones and duration. """
    tones = flatten([tonify(tones)])
    return [Point(tones, dur, ornamentation)]


def chords(tones, dur, ornamentation=""):
    dur = split_and_flatten(dur)
    orn = split_and_flatten(ornamentation) if '"' not in ornamentation else flatten([ornamentation])

    max_length = max([len(tones), len(dur), len(orn)])

    zip_list = zip(range(max_length), cycle(tones), cycle(dur), cycle(orn))
    return flatten([chord(t, d, o) for i, t, d, o in zip_list])


def add(point, tones, *tweaks):
    if isinstance(point, list):
        for subpoint in point:
            add(subpoint, tones)
    elif isinstance(point, Point):
        if not point.is_rest or "include rests" in tweaks:
            point.add(tones)
    return point


def remove(point, tones):
    if isinstance(point, list):
        for subpoint in point:
            remove(subpoint, tones)
    elif isinstance(point, Point):
        point.remove(tones)
    return point


def replace(point, old_tones, new_tones):
    if isinstance(point, list):
        for subitem in point:
            replace(subitem, old_tones, new_tones)
    elif isinstance(point, Point):
        point.replace(old_tones, new_tones)
    return point


def series(tones, start, stop_or_length, dur=None, step=1):
    tones, start = tonify(tones), tonify(start)
    stop_or_length = tonify(stop_or_length) if isinstance(stop_or_length, str) else stop_or_length

    validate_series_args(tones, start, stop_or_length, dur, step)

    start_index = tones.index(start)

    if isinstance(stop_or_length, str):
        stop_index = tones.index(stop_or_length)
    else:
        if stop_or_length > 0:
            stop_index = start_index + (stop_or_length - 1) * step
        else:
            stop_index = start_index + (stop_or_length + 1) * step

    stop_index = stop_index + 1 if stop_index >= start_index else stop_index - 1

    step = -step if stop_index < start_index else step

    series = tones[start_index:stop_index:step]

    return series if not dur else notes(series, dur)


def validate_series_args(tones, start, stop_or_length, dur, step):
    if start not in tones:
        raise ValueError("Cannot start series on {} as it it not in tones: {}.".format(start, [str(t) for t in tones]))

    if not isinstance(stop_or_length, int) and stop_or_length not in tones:
        raise ValueError("Cannot stop series on {} as it it not in tones: {}.".format(stop_or_length, [str(t) for t in tones]))

    if not isinstance(step, int):
        raise ValueError("series step must be an int, not {}".format(step))


def scale(start, stop_or_length, key, dur=None, step=1):
    key = keyify(key)
    return series(key.tones, start, stop_or_length, dur, step)


def arpeggio(start, stop_or_length, key, dur=None, step=1):
    key = keyify(key)
    return series(key.arpeggio_tones, start, stop_or_length, dur, step)


def arpeggio7(start, stop_or_length, key, dur=None, step=1):
    key = keyify(key)
    arpeggio7_tones = key.scale_subset([1, 3, 5, 7])
    return series(arpeggio7_tones, start, stop_or_length, dur, step)


def dominant7(start, stop_or_length, key, dur=None, step=1):
    key = keyify(key)
    dominant7_letters = key.arpeggio_letters + [key.relative_chromatic_letter(10)]
    dominant7_tones = [t for t in key.all_tones if separate(t)[0] in dominant7_letters]
    return series(dominant7_tones, start, stop_or_length, dur, step)


def diminished7(start, stop_or_length, key, dur=None, step=1):
    key = keyify(key)
    diminished7_letters = [key.relative_chromatic_letter(i) for i in [0, 3, 6, 9]]
    diminished7_tones = [t for t in key.all_tones if separate(t)[0] in diminished7_letters]
    return series(diminished7_tones, start, stop_or_length, dur, step)


def chromatic(start, stop_or_length, key, dur=None, step=1):
    key = keyify(key)
    return series(key.all_tones, start, stop_or_length, dur, step)


def scale_subset(positions, start, stop_or_length, key, dur=None, step=1):
    key = keyify(key)
    custom_tones = key.scale_subset(positions)
    return series(custom_tones, start, stop_or_length, dur, step)


def transpose(item, shift, key, mode="scale"):
    key = keyify(key)
    validate_transpose_args(shift, mode)

    if isinstance(item, dict):
        new_dict = {}
        for dict_key in item:
            new_dict[dict_key] = transpose(item[dict_key], shift, key, mode)
        return new_dict

    elif isinstance(item, list):
        return [transpose(subitem, shift, key, mode) for subitem in item]

    elif isinstance(item, Point):
        return Point(transpose(item.tones, shift, key, mode), item.dur, item.ornamentation)

    elif isinstance(item, str):
        try:
            item = tonify(item)
        except ValueError:
            return item
        if isinstance(item, list):
            return transpose(item, shift, key, mode)
        else:
            try:
                if mode == "octave":
                    new_pitch = all_pitches[all_pitches.index(pitch(item)) + shift]
                    return letter(item) + new_pitch
                elif mode == "scale":
                    current_index = key.tones.index(item)
                    return key.tones[current_index + shift]
                elif mode == "semitone":
                    return key.all_tones[key.all_tones.index(item) + shift]
            except ValueError:
                return transpose(equivalent_tone(item), shift, key, mode)
    else:
        raise ValueError("Cannot transpose {} as it is a {}".format(item, type(item)))


def validate_transpose_args(shift, mode):
    if not isinstance(shift, int):
        raise ValueError("{} is not a valid shift for piece.transpose(), it must be an int".format(shift))
    if mode not in ["octave", "scale", "semitone"]:
        raise ValueError("{} is not a valid mode for piece.transpose()".format(mode))


def harmonize(points, intervals, key, mode="scale"):
    return merge(points, transpose(points, intervals, key, mode))


def merge(*passages):
    base = [p for p in flatten(passages[0]) if isinstance(p, Point)]
    for passage in passages[1:]:
        target = [p for p in flatten(passage) if isinstance(p, Point)]
        for p, q in zip(base, target):
            p.add(q.tones)
    return passages[0]
