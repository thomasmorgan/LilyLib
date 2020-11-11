from util import flatten, split_and_flatten
from tones import tonify
from models import Point

from itertools import cycle


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
