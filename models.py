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
            if not isinstance(tones, Tone):
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
    """ A musical stave. """
    """ It has a clef, and optionally a name if multiple staves have the same clef. """

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
    """ A collection of sets of tones represented by a key signature. """
    """ Needs to be subclassed to be meaningful. """

    def __init__(self):
        # define must be overwritten in subclasses to:
        # 1. set the root letter
        # 2. set the included letters
        # 3. set the key's name
        self.define()

        self.create_all_tones()
        self.create_scale_tones()
        self.create_arpeggio_tones()

    def create_scale_tones(self):
        self.tones = [n for n in self.all_tones if n.letter in self.letters]

    def create_arpeggio_tones(self):
        index_of_root = self.letters.index(self.root)
        arpeggio_letters = [(self.letters * 2)[i] for i in [index_of_root, index_of_root + 2, index_of_root + 4]]
        self.arpeggio_tones = [t for t in self.all_tones if t.letter in arpeggio_letters]

    def create_all_tones(self):
        # creates a list of all *unique* tones
        # effectively a chromatic scale

        all_letters = [l for l in self.letters]
        for l in ['c', 'd', 'e', 'f', 'g', 'a', 'b']:
            if l not in all_letters and equivalent_letters[l] not in all_letters:
                all_letters.append(l)

        if self.bias() == "sharp":
            for l in ['cs', 'ds', 'es', 'fs', 'gs', 'as', 'bs']:
                if l not in all_letters and equivalent_letters[l] not in all_letters:
                    all_letters.append(l)
        if self.bias() == "flat":
            for l in ['cf', 'df', 'ef', 'ff', 'gf', 'af', 'bf']:
                if l not in all_letters and equivalent_letters[l] not in all_letters:
                    all_letters.append(l)

        self.all_tones = [t for t in all_tones() if t.letter in all_letters]

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

# class Melody():
# 	def __init__(self, key, *notes):
# 		self.key = key
# 		if notes:
# 			self.notes = flatten(notes)
# 		else:
# 			self.notes = []

# 	def __repr__(self):
# 		return " ".join(str(note) for note in self.notes)

# 	def __add__(self, other_melody):
# 		return Melody(self.key, self.notes + other_melody.notes)

# 	def __radd__(self, other_melody):
# 		return Melody(other_melody.key, other_melody.notes + self.notes)

# 	def __mul__(self, number):
# 		return Melody(self.key, self.notes*number)

# 	def __rmul__(self, number):
# 		return Melody(self.key, self.notes*number)

# 	def __len__(self):
# 		return len(self.notes)

# 	def __iter__(self):
# 		return self.notes.__iter__()

# 	def __next__(self):
# 		return self.notes.__next__()

# 	def __getitem__(self, index):
# 		if isinstance(index, int):
# 			if index > 0:
# 				index -= 1
# 			return Melody(self.key, self.notes.__getitem__(index))

# 		new_start = index.start
# 		new_stop = index.stop
# 		if isinstance(new_start, int) and new_start > 0:
# 			new_start -= 1
# 		if isinstance(new_stop, int) and  new_stop > 0:
# 			new_stop -= 1
# 		index = slice(new_start, new_stop, index.step)
# 		return Melody(self.key, self.notes.__getitem__(index))

# 	def __setitem__(self, index, value):
# 		if isinstance(index, int):
# 			if index > 0:
# 				index -= 1
# 			return Melody(self.key, self.notes.__setitem__(index, value))

# 		new_start = index.start
# 		new_stop = index.stop
# 		if isinstance(new_start, int) and new_start > 0:
# 			new_start -= 1
# 		if isinstance(new_stop, int) and  new_stop > 0:
# 			new_stop -= 1
# 		index = slice(new_start, new_stop, index.step)
# 		return Melody(self.key, self.notes.__setitem__(index, value))

# 	def rhythm(self, *rhythm):
# 		rhythm = flatten(rhythm)
# 		for i, note in enumerate(self.notes):
# 			note.dur = str(rhythm[i % len(rhythm)])
# 		return self

# 	r = rhythm

# 	def harmony(self, *harmony):
# 		harmony = flatten(harmony)
# 		new_notes = []
# 		for i, note in enumerate(self.notes):
# 			this_harmony = harmony[i % len(harmony)]
# 			this_harmony = map_harmony_to_int(this_harmony)
# 			if this_harmony == 0 or note.letter == "r":
# 				new_notes.append(note)
# 			else:
# 				if not self.key.includes(note.letter):
# 					print_error("Cannot build interval on {} as it is not in {}".format(note, key.name))
# 				index_of_note = [i for i, n in enumerate(self.key.notes) if n.letter == note.letter and n.pitch == note.pitch][0]
# 				new_note = self.key.notes[index_of_note + this_harmony]
# 				new_chord = Chord([note, new_note])
# 				new_notes.append(new_chord)
# 		self.notes = new_notes
# 		return self

# 	h = harmony

# 	def harmony_note(self, *args):
# 		notes = []
# 		harmonies = []
# 		for i, arg in enumerate(args):
# 			if i % 2 == 0:
# 				notes.append(arg)
# 			else:
# 				harmonies.append(arg)
# 		for note, harmony in zip(notes, harmonies):
# 			harmony = map_harmony_to_int(harmony)
# 			note = str(Note(note))
# 			for i, n in enumerate(self.notes):
# 				if not isinstance(n, Chord):
# 					if n.chord_repr() == note:
# 						index_of_note = [i for i, nn in enumerate(self.key.notes) if nn.letter == n.letter and nn.pitch == n.pitch][0]
# 						new_note = self.key.notes[index_of_note + harmony]
# 						new_chord = Chord([n, new_note])
# 						self.notes[i] = new_chord
# 		return self

# 	hn = harmony_note

# 	def harmony_position(self, *args):
# 		positions = []
# 		harmonies = []
# 		for i, arg in enumerate(args):
# 			if i % 2 == 0:
# 				positions.append(arg)
# 			else:
# 				harmonies.append(arg)

# 		for position, harmony in zip(positions, harmonies):
# 			harmony = map_harmony_to_int(harmony)
# 			current_note = self[position].notes[0]
# 			index_of_note = [i for i, nn in enumerate(self.key.notes) if nn.letter == current_note.letter and nn.pitch == current_note.pitch][0]
# 			new_note = self.key.notes[index_of_note + harmony]
# 			new_chord = Chord([current_note, new_note])
# 			self[position] = new_chord

# 		return self

# 	hp = harmony_position


class Tempo:
    """ A time signature. """
    """ Defaults to 4/4. """

    def __init__(self, tempo):
        self.tempo = "4/4"

    def __str__(self):
        return "\\time {}\n".format(self.tempo)
