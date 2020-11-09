import util



        self.dur = dur
        self.ornamentation = ornamentation


    @property
    def letter(self):
        return util.letter(self.tone)

    @property
    def pitch(self):
        return util.pitch(self.tone)


class Chord:
    """ The simultaneous sounding of multiple tones for a specified duration."""

    def __init__(self, tones, dur, ornamentation=""):
        tones = self.parse_tones(tones)
        self.check_init_arguments(tones, dur, ornamentation)
        self.tones = tones
        self.dur = dur
        self.ornamentation = ornamentation

    def parse_tones(self, tones):
        parsed_tones = []
        for t in util.flatten([tones]):
            if isinstance(t, str) and ' ' in t:
                parsed_tones.extend(t.split(" "))
            else:
                parsed_tones.append(t)
        return parsed_tones

    def check_init_arguments(self, tones, dur, ornamentation):
        if not isinstance(tones, list):
            raise ValueError("Cannot create note with {} as tones. tone must be a list.".format(tones))

        for tone in tones:
            if not isinstance(tone, str):
                raise ValueError("Cannot create note with {} as tone. tone must be a string.".format(tone))

        if not isinstance(dur, int) and not isinstance(dur, str):
            raise ValueError("Cannot create note with {} as dur. dur must be an int or string.".format(dur))
        if not isinstance(ornamentation, str):
            raise ValueError("Cannot create note with {} as ornamentation. ornamentation must be a string.".format(ornamentation))

    def __str__(self):
        return "<" + " ".join(self.tones) + ">" + str(self.dur) + self.ornamentation


class Stave:
    """ A musical stave. It has a clef, and optionally a name (for if multiple staves have the same clef). """

    def __init__(self, clef, name=None):
        if clef not in ['treble', 'bass', 'G', '"G2"', 'french', 'GG', 'tenorG', 'soprano', 'mezzosoprano', 'C', 'alto', 'tenor', 'baritone']:
            raise ValueError('{} is not a permitted clef'.format(clef))

        self.clef = clef
        if name:
            self.name = name
        else:
            self.name = clef

        self.start = '<< \\new Staff {{\n\\clef {}\n'.format(self.clef)
        self.end = '} >>\n'


class Key:
    """ A set of Tones represented by a key signature. Needs to be subclassed to be meaningful.
    util.all_tones returns every possible Tone
    Key.all_tones returns all unique tones in the key (i.e. excluding equivalent tones)
    Key.tones returns all Tones in the scale of the key
    Key.arpeggio_tones returns all Tones in the arpeggio of the key. """

    def __init__(self):
        # define must be overwritten in subclasses to:
        # 1. set the root letter
        # 2. set the included letters
        # 3. set the key's name
        self.root = None
        self.letters = None
        self.name = None
        self.define()
        self.confirm_definition()

        self.init_all_tones()
        self.init_scale_tones()
        self.init_arpeggio_tones()

    def confirm_definition(self):
        if None in [self.root, self.letters, self.name]:
            raise ValueError("Must define root, letters and name of Key {}".format(self))

    def init_all_tones(self):
        all_letters = [l for l in self.letters]
        for l in ['c', 'd', 'e', 'f', 'g', 'a', 'b']:
            if l not in all_letters and util.equivalent_letters[l] not in all_letters:
                all_letters.append(l)

        if self.bias() == "sharp":
            for l in ['cs', 'ds', 'es', 'fs', 'gs', 'as', 'bs']:
                if l not in all_letters and util.equivalent_letters[l] not in all_letters:
                    all_letters.append(l)
        if self.bias() == "flat":
            for l in ['cf', 'df', 'ef', 'ff', 'gf', 'af', 'bf']:
                if l not in all_letters and util.equivalent_letters[l] not in all_letters:
                    all_letters.append(l)

        self.all_letters = [l for l in util.all_letters if l in all_letters]
        self.all_tones = [t for t in util.all_tones if util.letter(t) in all_letters]

    def init_scale_tones(self):
        self.tones = [t for t in self.all_tones if util.letter(t) in self.letters]

    def init_arpeggio_tones(self):
        index_of_root = self.letters.index(self.root)
        self.arpeggio_letters = [(self.letters * 2)[i] for i in [index_of_root, index_of_root + 2, index_of_root + 4]]
        self.arpeggio_tones = [t for t in self.all_tones if util.letter(t) in self.arpeggio_letters]

    def scale_subset(self, positions):
        index_of_root = self.letters.index(self.root)
        custom_letters = [(self.letters * 2)[index_of_root + p - 1] for p in positions]
        return [t for t in self.all_tones if util.letter(t) in custom_letters]

    def bias(self):
        num_sharps = len([l for l in self.letters if "s" in l])
        num_flats = len([l for l in self.letters if "f" in l and l not in ['f', 'fs', 'fss']])

        if "harmonic" in self.name:
            num_flats -= 1

        if num_sharps < num_flats:
            return "flat"
        else:
            return "sharp"

    def define(self):
        raise NotImplementedError("Key.define must be overwritten.")

    def __str__(self):
        string = "\\key " + self.name
        string = string.replace(" minor", " \\minor")
        string = string.replace(" major", " \\major")
        string = string.replace(" sharp", "s")
        string = string.replace(" flat", "f")
        string = string.replace(" harmonic", "")
        string = string.replace(" melodic", "")
        return string + '\n'

    def relative_letter(self, relative_position):
        index_of_root = self.letters.index(self.root)
        new_index = index_of_root + relative_position
        return (self.letters * 2)[new_index]

    def relative_chromatic_letter(self, relative_position):
        index_of_root = self.all_letters.index(self.root)
        new_index = index_of_root + relative_position
        return (self.all_letters * 2)[new_index]

    @property
    def tonic(self):
        return self.relative_letter(0)

    @property
    def supertonic(self):
        return self.relative_letter(1)

    @property
    def mediant(self):
        return self.relative_letter(2)

    @property
    def subdominant(self):
        return self.relative_letter(3)

    @property
    def dominant(self):
        return self.relative_letter(4)

    @property
    def submediant(self):
        return self.relative_letter(5)

    @property
    def leading(self):
        return self.relative_letter(6)

    @property
    def subtonic(self):
        return self.leading

    @property
    def i(self):
        return self.tonic

    @property
    def ii(self):
        return self.supertonic

    @property
    def iii(self):
        return self.mediant

    @property
    def iv(self):
        return self.subdominant

    @property
    def v(self):
        return self.dominant

    @property
    def vi(self):
        return self.submediant

    @property
    def vii(self):
        return self.leading

    @property
    def I(self):
        return self.tonic

    @property
    def II(self):
        return self.supertonic

    @property
    def III(self):
        return self.mediant

    @property
    def IV(self):
        return self.subdominant

    @property
    def V(self):
        return self.dominant

    @property
    def VI(self):
        return self.submediant

    @property
    def VII(self):
        return self.leading
