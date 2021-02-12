from util import flatten, split_and_flatten
from tones import tonify, all_pitches, pitch, letter, equivalent_tone, all_tones
from keys import keyify

from itertools import cycle
from copy import deepcopy


all_durs = ['\\longa' '\\breve', 1, '1', 2, '2', 4, '4', 8, '8', 16, '16', 32, '32', 64, '64', 128, '128', '1.', '2.', '4.', '8.', '16.', '32.', '64.', '128.', '1..', '2..', '4..', '8..', '16..', '32..', '64..', '128..']


class Point:
    """ An element in sheet music with a specified duration.
        Prints as either a rest, note or chord.
        May have a variety of articulations, ornaments, dynamics and so on."""

    def __init__(self, tones, dur, phrasing="", articulation="", ornamentation="", dynamics="", markup="", markdown="", prefix="", suffix=""):
        self.check_init_arguments(tones, dur, phrasing, articulation, ornamentation, dynamics, markup, markdown, prefix, suffix)
        self.tones = tones
        self.dur = dur
        self.phrasing = phrasing
        self.articulation = articulation
        self.ornamentation = ornamentation
        self.dynamics = dynamics
        self.markup = markup
        self.markdown = markdown
        self.prefix = prefix
        self.suffix = suffix

    def check_init_arguments(self, tones, dur, phrasing, articulation, ornamentation, dynamics, markup, markdown, prefix, suffix):
        if not isinstance(tones, list):
            raise ValueError("Cannot create Point with {} as tones. tones must be a list.".format(tones))
        for t in tones:
            if t not in all_tones:
                raise ValueError("Cannot create Point with tones containing {} as it is not a valid tone.".format(t))
        if dur not in all_durs:
            raise ValueError("Cannot create Point with {} as dur. dur must be one of {}.".format(dur, all_durs))
        if not isinstance(phrasing, str):
            raise ValueError("Cannot create Point with {} as phrasing. phrasing must be a string.".format(phrasing))
        if not isinstance(articulation, str):
            raise ValueError("Cannot create Point with {} as articulation. articulation must be a string.".format(articulation))
        if not isinstance(ornamentation, str):
            raise ValueError("Cannot create Point with {} as ornamentation. ornamentation must be a string.".format(ornamentation))
        if not isinstance(dynamics, str):
            raise ValueError("Cannot create Point with {} as dynamics. dynamics must be a string.".format(dynamics))
        if not isinstance(markup, str):
            raise ValueError("Cannot create Point with {} as markup. markup must be a string.".format(markup))
        if not isinstance(markdown, str):
            raise ValueError("Cannot create Point with {} as markdown. markdown must be a string.".format(markdown))
        if not isinstance(prefix, str):
            raise ValueError("Cannot create Point with {} as prefix. prefix must be a string.".format(prefix))
        if not isinstance(suffix, str):
            raise ValueError("Cannot create Point with {} as suffix. suffix must be a string.".format(suffix))

    def __str__(self):
        if self.is_rest:
            tone_string = 'r'
        elif self.is_note:
            tone_string = self.tone
        elif self.is_chord:
            tone_string = "<" + " ".join(self.tones) + ">"
        else:
            raise ValueError("Cannot print {} as it is neither a rest, nor note, nor chord. Its tones are {}".format(self, self.tones))

        string = '{}{}'.format(tone_string, self.dur)
        if self.prefix:
            string = self.prefix + string
        if self.phrasing:
            string += self.phrasing
        if self.articulation:
            string += '-' + self.articulation
        if self.ornamentation:
            string += '\\' + self.ornamentation
        if self.dynamics:
            string += '\\' + self.dynamics
        if self.markup:
            string += "^\\markup{" + self.markup + "}"
        if self.markdown:
            string += "_\\markup{" + self.markdown + "}"
        if self.suffix:
            string += self.suffix
        return string

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


def rest(dur, phrasing="", articulation="", ornamentation="", dynamics="", markup="", markdown="", prefix="", suffix=""):
    """ Returns a list with a single Point that prints as a rest with the specified duration. """
    return [Point([], dur, phrasing, articulation, ornamentation, dynamics, markup, markdown, prefix, suffix)]


def rests(*dur):
    """ Returns a list of Points that print as rests with the specified durations. """
    return flatten([rest(d) for d in split_and_flatten(dur)])


def note(tone, dur, phrasing="", articulation="", ornamentation="", dynamics="", markup="", markdown="", prefix="", suffix=""):
    """ Returns a list with a single Point that prints as a note with the specified tone and duration.
    Passing an empty string or list as tone will return a rest.
    Passing a list of tones (or a string that can be split into multiple tones raises an error. """
    tone = flatten([tonify(tone)])
    if len(tone) > 1:
        raise ValueError("Cannot create single note with tone of {}.".format(tone))
    return [Point(tone, dur, phrasing, articulation, ornamentation, dynamics, markup, markdown, prefix, suffix)]


def notes(tones, dur):
    """ Returns a list of Points that print as notes with the specified tone(s) and duration(s).
    If tones is a string including adjacent white space, rests are produced.
    If tones is a list including empty lists or empty strings, rests are produced.
    Nested lists of tones are not permitted as tones will not be flattened to avoid removing empty lists."""
    tones = tonify(tones)
    tones = [tones] if isinstance(tones, str) else tones
    dur = split_and_flatten(dur)

    max_length = max([len(tones), len(dur)])

    zip_list = zip(range(max_length), cycle(tones), cycle(dur))
    return flatten([note(t, d) for i, t, d in zip_list])


def chord(tones, dur, phrasing="", articulation="", ornamentation="", dynamics="", markup="", markdown="", prefix="", suffix=""):
    """ Returns a list containing a single Point that prints as a chord with the specified tones and duration. """
    tones = flatten([tonify(tones)])
    return [Point(tones, dur, phrasing, articulation, ornamentation, dynamics, markup, markdown, prefix, suffix)]


def chords(tones, dur):
    dur = split_and_flatten(dur)

    max_length = max([len(tones), len(dur)])

    zip_list = zip(range(max_length), cycle(tones), cycle(dur))
    return flatten([chord(t, d) for i, t, d in zip_list])


def tied_note(tone, dur, articulation="", ornamentation="", dynamics="", markup="", markdown="", prefix="", suffix=""):
    """ Returns a list of Points that prints as a series of tied notes with the same specified tone but different durations.
    Passing an empty string or list as tone will return a rest.
    Passing a list of tones (or a string that can be split into multiple tones raises an error. """
    tone = flatten([tonify(tone)])
    if len(tone) > 1:
        raise ValueError("Cannot create tied note with tone of {}.".format(tone))
    if not isinstance(dur, list):
        raise ValueError("Cannot make tied note with duration {}. Dur must be a list of durations.".format(dur))

    points = []
    for i, d in enumerate(dur):
        if i == 0:
            points.append(Point(tone, d, "~", articulation, ornamentation, dynamics, markup, markdown, prefix, suffix))
        elif i < (len(dur) - 1):
            points.append(Point(tone, d, "~"))
        else:
            points.append(Point(tone, d))
    return points


def tied_chord(tones, dur, articulation="", ornamentation="", dynamics="", markup="", markdown="", prefix="", suffix=""):
    """ Returns a list of Points that prints as a series of tied chords with the same specified tones but different durations. """
    tones = flatten([tonify(tones)])
    if not isinstance(dur, list):
        raise ValueError("Cannot make tied chord with duration {}. Dur must be a list of durations.".format(dur))

    points = []
    for i, d in enumerate(dur):
        if i == 0:
            points.append(Point(tones, d, "~", articulation, ornamentation, dynamics, markup, markdown, prefix, suffix))
        elif i < (len(dur) - 1):
            points.append(Point(tones, d, "~"))
        else:
            points.append(Point(tones, d))
    return points


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
    return series(key.arpeggio7_tones, start, stop_or_length, dur, step)


def dominant7(start, stop_or_length, key, dur=None, step=1):
    key = keyify(key)
    return series(key.dominant7_tones, start, stop_or_length, dur, step)


def diminished7(start, stop_or_length, key, dur=None, step=1):
    key = keyify(key)
    return series(key.diminished7_tones, start, stop_or_length, dur, step)


def chromatic(start, stop_or_length, key, dur=None, step=1):
    key = keyify(key)
    if isinstance(stop_or_length, int):
        if stop_or_length > 1:
            return series(key.ascending_chromatic_tones, start, stop_or_length, dur, step)
        else:
            return series(key.descending_chromatic_tones, start, stop_or_length, dur, step)
    else:
        start_index = all_tones.index(tonify(start))
        stop_index = all_tones.index(tonify(stop_or_length))
        if stop_index > start_index:
            return series(key.ascending_chromatic_tones, start, stop_or_length, dur, step)
        else:
            return series(key.descending_chromatic_tones, start, stop_or_length, dur, step)


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
        return Point(transpose(item.tones, shift, key, mode),
                     item.dur,
                     articulation=item.articulation,
                     ornamentation=item.ornamentation,
                     dynamics=item.dynamics,
                     markup=item.markup,
                     markdown=item.markdown,
                     prefix=item.prefix,
                     suffix=item.suffix)

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


def harmonize(points, interval, key, mode="scale"):
    return merge(points, transpose(points, interval, key, mode))


def merge(*passages):
    passage_to_return = deepcopy(passages[0])
    base = [p for p in flatten(passage_to_return) if isinstance(p, Point)]
    for passage in passages[1:]:
        target = [p for p in flatten(passage) if isinstance(p, Point)]
        for p, q in zip(base, target):
            p.add(q.tones)
    return passage_to_return
