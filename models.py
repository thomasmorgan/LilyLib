class Tone:
    """ The sound of a single note. """
    """ Has a letter and a pitch, but no duration etc. """
    """ Rests are tones, they have the letter r. """

    def __init__(self, tone):

        if not isinstance(tone, str):
            raise ValueError("Tones must be created with a string, not {}".format(tone))

        self.valid_letters = []
        self.valid_pitches = []
        if tone == 'r':
            self.valid_letters.append('r')
            self.valid_pitches.append('')
            self.letter = 'r'
            self.pitch = ''
        else:
            letters = ['c', 'd', 'e', 'f', 'g', 'a', 'b']
            accents = ['ff', 'f', '', 's', 'ss']
            for l in letters:
                for a in accents:
                    self.valid_letters.append(l + a)
            self.valid_pitches = [",,,", ",,", ",", "", "`", "``", "```"]

            if tone[-1] == "`":
                tone = tone.split("`", 1)
                letter = tone[0]
                pitch = tone[1] + "`"
            elif tone[-1] == ",":
                tone = tone.split(",", 1)
                letter = tone[0]
                pitch = tone[1] + ","
            else:
                letter = tone
                pitch = ""

            if letter not in self.valid_letters:
                raise ValueError("Cannot create Tone with letter {}".format(letter))
            if pitch not in self.valid_pitches:
                raise ValueError("Cannot create Tone with pitch {}".format(pitch))

            self.letter = letter
            self.pitch = pitch

    def __str__(self):
        return self.letter + self.pitch

    def shift(self, shift):
        current_index = self.valid_pitches.index(self.pitch)
        new_pitch = self.valid_pitches[current_index + shift]
        return Tone(self.letter + new_pitch)


class Note:
    """ The sounding of a single tone for a specified time. """
    """ Prints as a single note in sheet music. """

    def __init__(self, tone, dur):
        if isinstance(tone, Tone):
            self.tone = tone
        elif isinstance(tone, str):
            self.tone = Tone(tone)
        else:
            raise ValueError("Cannot create note with {} as tone. tone must be a Tone or string.".format(tone))
        self.dur = dur

    def __repr__(self):
        return str(self.tone) + str(self.dur)


class Chord:
    """ The simultaneous sounding of multiple tones. """
    """ Prints as a chord in sheet music. """

    def __init__(self, tones, dur):
        self.tones = []
        if isinstance(tones, str):
            tones = tones.split(" ")
        for tone in tones:
            if isinstance(tone, Tone):
                self.tones.append(tone)
            else:
                if tone:
                    self.tones.append(Tone(tone))
        self.dur = dur

    def __repr__(self):
        return("<" + " ".join([(t.letter + t.pitch) for t in self.tones]) + ">" + str(self.dur))


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
    """ A collection of tones contained by a key signature. """
    """ Needs to be subclassed to be meaningful. """

    def __init__(self):
        self.create_all_tones()

        # define must be overwritten in sublcasses to:
        # 1. set the root letter
        # 2. set the included letters
        # 3. set the key's name
        self.define()

        self.create_scale_tones()
        self.create_arpeggio_tones()
        self.create_chromatic_tones()

    def create_all_tones(self):
        letters = ['c', 'd', 'e', 'f', 'g', 'a', 'b']
        accents = ['ff', 'f', '', 's', 'ss']
        pitches = [",,,", ",,", ",", "", "`", "``", "```"]
        self.all_tones = []
        for p in pitches:
            for l in letters:
                for a in accents:
                    self.all_tones.append(Tone(l + a + p))
        self.all_letters = [str(t) for t in self.all_tones if t.pitch == '']

    def create_scale_tones(self):
        self.tones = [n for n in self.all_tones if n.letter in self.letters]

    def create_arpeggio_tones(self):
        self.arpeggio_letters = {}
        self.arpeggio_tones = {}
        for root in self.letters:
            index_of_root = self.letters.index(root)
            self.arpeggio_letters[root] = [(self.letters * 2)[i] for i in [index_of_root, index_of_root + 2, index_of_root + 4]]
            self.arpeggio_tones[root] = [t for t in self.all_tones if t.letter in self.arpeggio_letters[root]]

    def create_chromatic_tones(self):
        # first add all letters from the main scale
        chromatic_letters = self.letters

        # we need to know which letters are equivalent to avoid duplicates
        equivalents = {
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

        # the add all natural letters if an equiavlent is not already there
        for l in ['c', 'd', 'e', 'f', 'g', 'a', 'b']:
            if l not in chromatic_letters and equivalents[l] not in chromatic_letters:
                chromatic_letters.append(l)

        # then add all letters that fit the bias if the equiavlent is not already there
        if self.bias() == "sharp":
            for l in ['cs', 'ds', 'es', 'fs', 'gs', 'as', 'bs']:
                if l not in chromatic_letters and equivalents[l] not in chromatic_letters:
                    chromatic_letters.append(l)
        if self.bias() == "flat":
            for l in ['cf', 'df', 'ef', 'ff', 'gf', 'af', 'bf']:
                if l not in chromatic_letters and equivalents[l] not in chromatic_letters:
                    chromatic_letters.append(l)

        # then order the letters and create the tones
        self.chromatic_letters = [l for l in self.all_letters if l in chromatic_letters]
        self.chromatic_tones = [t for t in self.all_tones if t.letter in self.chromatic_letters]

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
        string = string.replace(" harmonic", "")
        string = string.replace(" melodic", "")
        return string + '\n'

    def includes(self, letter):
        return letter in self.letters

    def series(self, mode, start, stop_or_length, step=1):
        if mode not in ["scale", "arpeggio", "chromatic"]:
            raise ValueError("{} is not a valid mode for key.series".format(mode))

        if not (isinstance(start, Tone) or isinstance(start, str)):
            raise ValueError("{} is not a valid start for key.series, must be a Tone or str".format(mode))

        if not (isinstance(stop_or_length, Tone) or isinstance(stop_or_length, str) or isinstance(stop_or_length, int)):
            raise ValueError("{} is not a valid stop_or_length for key.series, must be a Tone, str or int".format(mode))

        if not isinstance(step, int):
            raise ValueError("{} step must be an int, not {}".format(mode, step))

        if mode == "scale":
            tones = self.tones
        elif mode == "arpeggio":
            tones = self.arpeggio_tones
        elif mode == "chromatic":
            tones = self.chromatic_tones

        try:
            start_index = [str(t) for t in tones].index(str(start))
        except ValueError:
            raise ValueError("{} is not a valid start for a {} in key {}.".format(start, mode, self))

        if isinstance(stop_or_length, int):
            stop_index = start_index + (stop_or_length - 1) * step
        else:
            try:
                stop_index = [str(t) for t in tones].index(str(stop_or_length))
            except ValueError:
                raise ValueError("{} is not a valid stop for a {} in key {}.".format(stop_or_length, mode, self))

        if stop_index >= start_index:
            stop_index += 1
        elif stop_index < start_index:
            stop_index -= 1
            step *= -1

        return tones[start_index:stop_index:step]

    def scale(self, start, stop_or_length, step=1):
        return self.series("scale", start, stop_or_length, step)

    def arpeggio(self, start, stop_or_length, step=1):
        return self.series("arpeggio", start, stop_or_length, step)

    def chromatic(self, start, stop_or_length, step=1):
        return self.series("chromatic", start, stop_or_length, step)


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


class Section:
    def __init__(self, name, staves):
        self.name = name
        self.staves = {}
        for staff in staves:
            self.staves[staff] = None

    def __getitem__(self, index):
        return self.staves.__getitem__(index)

    def __setitem__(self, index, value):
        return self.staves.__setitem__(index, value)

    def print_stave(self, stave):
        return " ".join(str(note) for note in self[stave]) + "\n"

    def print_score(self, index):
        return " ".join(str(n) for n in self.staves[index])


class Tempo:
    def __init__(self, tempo):
        self.tempo = "4/4"

    def __str__(self):
        return "\\time {}\n".format(self.tempo)
