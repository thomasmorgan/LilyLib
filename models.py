class Tone:
    """ The frequency of a single note. A Tone has a letter and a pitch, but no duration etc.
    Rests are tones too, they have the letter r, and no pitch. Tones cannot be printed as sheet music.

    Tones are created from a string, e.g. "c`" for middle c.

    A unique set of Tones is created within a ToneSpace when a Key is created, and these Tones should be used
    as necessary without creating more. To dissuade users from creating more Tones than necessary the init
    function will raise an error unless "override=True" is passed."""

    def __init__(self, tone_string, override=False):
        self.check_init_arguments(tone_string, override)
        self.assign_letter_and_pitch(tone_string)

    def check_init_arguments(self, tone_string, override):
        if not override:
            raise ValueError("You are trying to create a new Tone. All necessary tones are created once and should just be shared from then on. If you must create a new tone pass override=True.")

        if not isinstance(tone_string, str):
            raise ValueError("Tones must be created with a string, not {}".format(tone_string))

    def assign_letter_and_pitch(self, tone_string):
        if tone_string == 'r':
            self.letter = 'r'
            self.pitch = ''
        else:
            if tone_string[-1] in ["`", ","]:
                split = tone_string.split(tone_string[-1], 1)
                self.letter = split[0]
                self.pitch = split[1] + tone_string[-1]
            else:
                self.letter = tone_string
                self.pitch = ""

    def __str__(self):
        return self.letter + self.pitch

    def duplicate(self):
        return self


class ToneSpace():
    """ An object that contains the full set of permissable Tones used to create Notes and Chords. """

    def __init__(self):
        self.create_tones()

    def create_tones(self):
        all_tones = []
        for p in self.all_pitches:
            for l in self.all_letters:
                all_tones.append(Tone(l + p, True))
        all_tones.append(Tone("r", True))
        self.tones = all_tones

    all_pitches = [",,,", ",,", ",", "", "`", "``", "```"]

    @property
    def all_letters(self):
        all_letters = []
        letters = ['c', 'd', 'e', 'f', 'g', 'a', 'b']
        accents = ['ff', 'f', '', 's', 'ss']
        for l in letters:
            for a in accents:
                all_letters.append(l + a)
        return all_letters

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

    def tone_with_string(self, string):
        return [t for t in self.tones if str(t) == string][0]


class Note:
    """ The sounding of a single Tone for a specified duration. Can be printed as sheet music. """

    def __init__(self, tone, dur, ornamentation=""):
        self.check_init_arguments(tone, dur, ornamentation)
        self.tone = tone
        self.dur = dur
        self.ornamentation = ornamentation

    def check_init_arguments(self, tone, dur, ornamentation):
        if not isinstance(tone, Tone):
            raise ValueError("Cannot create note with {} as tone. tone must be a Tone.".format(tone))
        if not isinstance(dur, int) and not isinstance(dur, str):
            raise ValueError("Cannot create note with {} as dur. dur must be an int or string.".format(dur))
        if not isinstance(ornamentation, str):
            raise ValueError("Cannot create note with {} as ornamentation. ornamentation must be a string.".format(ornamentation))

    def __str__(self):
        return str(self.tone) + str(self.dur) + self.ornamentation

    def duplicate(self):
        return Note(self.tone, self.dur, self.ornamentation)

    @property
    def letter(self):
        return self.tone.letter

    @property
    def pitch(self):
        return self.tone.pitch


class Chord:
    """ The simultaneous sounding of multiple Tones for a specified duration."""

    def __init__(self, tones, dur, ornamentation=""):
        self.check_init_arguments(tones, dur, ornamentation)
        self.tones = tones
        self.dur = dur
        self.ornamentation = ornamentation

    def check_init_arguments(self, tones, dur, ornamentation):
        if not isinstance(tones, list):
            raise ValueError("Cannot create note with {} as tones. tone must be a list.".format(tones))

        for tone in tones:
            if not isinstance(tone, Tone):
                raise ValueError("Cannot create note with {} as tone. tone must be a Tone.".format(tone))

        if not isinstance(dur, int) and not isinstance(dur, str):
            raise ValueError("Cannot create note with {} as dur. dur must be an int or string.".format(dur))
        if not isinstance(ornamentation, str):
            raise ValueError("Cannot create note with {} as ornamentation. ornamentation must be a string.".format(ornamentation))

    def __str__(self):
        return "<" + " ".join([str(t) for t in self.tones]) + ">" + str(self.dur) + self.ornamentation

    def duplicate(self):
        return Chord(self.tones, self.dur, self.ornamentation)


class Stave:
    """ A musical stave. It has a clef, and optionally a name if multiple staves have the same clef. """

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
    Key.tonespace.tones returns every possible Tone
    Key.all_tones returns all unique tones in the key (i.e. excluding equivalent tones)
    Key.tones returns all Tones in the scale of the key
    Key.arpeggio_tones returns all Tones in the arpeggio of the key. """

    def __init__(self, tonespace):
        # define must be overwritten in subclasses to:
        # 1. set the root letter
        # 2. set the included letters
        # 3. set the key's name
        self.root = None
        self.letters = None
        self.name = None
        self.define()
        self.confirm_definition()

        self.tonespace = tonespace
        self.init_all_tones()
        self.init_scale_tones()
        self.init_arpeggio_tones()

    def confirm_definition(self):
        if None in [self.root, self.letters, self.name]:
            raise ValueError("Must define root, letters and name of Key {}".format(self))

    def init_all_tones(self):
        all_letters = [l for l in self.letters]
        for l in ['c', 'd', 'e', 'f', 'g', 'a', 'b']:
            if l not in all_letters and self.tonespace.equivalent_letters[l] not in all_letters:
                all_letters.append(l)

        if self.bias() == "sharp":
            for l in ['cs', 'ds', 'es', 'fs', 'gs', 'as', 'bs']:
                if l not in all_letters and self.tonespace.equivalent_letters[l] not in all_letters:
                    all_letters.append(l)
        if self.bias() == "flat":
            for l in ['cf', 'df', 'ef', 'ff', 'gf', 'af', 'bf']:
                if l not in all_letters and self.tonespace.equivalent_letters[l] not in all_letters:
                    all_letters.append(l)

        self.all_tones = [t for t in self.tonespace.tones if t.letter in all_letters]

    def init_scale_tones(self):
        self.tones = [t for t in self.all_tones if t.letter in self.letters]

    def init_arpeggio_tones(self):
        index_of_root = self.letters.index(self.root)
        arpeggio_letters = [(self.letters * 2)[i] for i in [index_of_root, index_of_root + 2, index_of_root + 4]]
        self.arpeggio_tones = [t for t in self.all_tones if t.letter in arpeggio_letters]

    def scale_subset(self, positions):
        index_of_root = self.letters.index(self.root)
        custom_letters = [(self.letters * 2)[index_of_root + p - 1] for p in positions]
        return [t for t in self.all_tones if t.letter in custom_letters]

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
