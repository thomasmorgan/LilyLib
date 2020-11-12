from util import flatten
from tones import tonify, all_tones, all_durs, letter, pitch
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

