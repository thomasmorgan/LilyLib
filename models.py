class Letter:
    """ A letter associated with a note, e.g. a or bf """

    def __init__(self, letter):
        permitted_letters = []
        letters = ['c', 'd', 'e', 'f', 'g', 'a', 'b']
        accents = ['ff', 'f', '', 's', 'ss']
        for l in letters:
            for a in accents:
                permitted_letters.append(l + a)
        if letter not in permitted_letters:
            raise ValueError("{} is not a valid letter".format(letter))
        else:
            self.letter = letter

    def __str__(self):
        return self.letter


class Pitch:
    """ A pitch associated with a note, e.g. ' (written as `) or , """

    def __init__(self, pitch):
        pitches = [",,,", ",,", ",", "", "`", "``", "```"]
        if pitch not in pitches:
            raise ValueError("{} is not a valid pitch".format(pitch))
        else:
            self.pitch = pitch

    def __str__(self):
        return self.pitch


class Tone:
    """ The sound of a single note. """
    """ Has a letter and a pitch, but no duration etc. """

    def __init__(self, tone):
        if tone[-1] == "`":
            tone = tone.split("`", 1)
            self.letter = Letter(tone[0])
            self.pitch = Pitch(tone[1] + "`")
        elif tone[-1] == ",":
            tone = tone.split(",", 1)
            self.letter = Letter(tone[0])
            self.pitch = Pitch(tone[1] + ",")
        else:
            self.letter = Letter(tone)
            self.pitch = Pitch("")

    def __str__(self):
        return str(self.letter) + str(self.pitch)


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
        return("<" + " ".join([(t.letter.letter + t.pitch.pitch) for t in self.tones]) + ">" + str(self.dur))


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
        letters = ['c', 'd', 'e', 'f', 'g', 'a', 'b']
        accents = ['ff', 'f', '', 's', 'ss']
        pitches = [",,,", ",,", ",", "", "`", "``", "```"]
        self.all_tones = []
        for p in pitches:
            for l in letters:
                for a in accents:
                    self.all_tones.append(Tone(l + a + p))

        self.letters = None
        self.name = None

    def __str__(self):
        string = "\\key " + self.name
        string = string.replace(" minor", " \\minor")
        string = string.replace(" major", " \\major")
        string = string.replace(" harmonic", "")
        string = string.replace(" melodic", "")
        return string + '\n'

    def includes(self, letter):
        return letter in self.letters

    def filter_notes(self):
        self.tones = [n for n in self.all_tones if n.letter.letter in self.letters]

    def scale(self, start, stop):
        try:
            start_index = [i for i, tone in enumerate(self.tones) if str(tone) == start][0]
            stop_index = [i for i, tone in enumerate(self.tones) if str(tone) == stop][0]
        except IndexError:
            raise ValueError("Cannot write scale from {} to {} in key {}".format(start, stop, self))

        if stop_index >= start_index:
            step = 1
        elif stop_index < start_index:
            stop_index -= 2
            step = -1

        return self.tones[start_index:stop_index + 1:step]


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
