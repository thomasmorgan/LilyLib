from util import print_error, flatten, map_harmony_to_int


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
        pitch = pitch.replace("`", "'")
        pitches = [",,,", ",,", ",", "", "'", "''", "'''"]
        if pitch not in pitches:
            raise ValueError("{} is not a valid pitch".format(pitch))
        else:
            self.pitch = pitch

    def __str__(self):
        return self.pitch

class Note:
	def __init__(self, note, dur=""):
		note = note.replace("`", "'")
		if note[-1] == "'":
			dum = note.split("'", 1)
			self.letter = dum[0]
			self.pitch = dum[1] + "'"
		elif note[-1] == ",":
			dum = note.split(",", 1)
			self.letter = dum[0]
			self.pitch = dum[1] + ","
		else:
			self.letter = note
			self.pitch = ""
		self.dur = str(dur)

	def __repr__(self):
		return self.letter + self.pitch + self.dur

	def chord_repr(self):
		return self.letter + self.pitch

class Chord:
	def __init__(self, notes, dur=""):
		self.notes = []
		if isinstance(notes, str):
			notes = notes.split(" ")
		for note in notes:
			if isinstance(note, Note):
				self.notes.append(note)
			else:
				if note:
					self.notes.append(Note(note))
		self.dur = self.notes[0].dur
		if dur:
			self.dur = str(dur)

	def __repr__(self):
		rep = "<"
		for note in self.notes:
			rep += note.chord_repr() + " "
		if self.notes:
			rep = rep[:-1]
		rep += ">" + self.dur
		return(rep)

class Key:
	def __init__(self):
		letters = ['c', 'd', 'e', 'f', 'g', 'a', 'b']
		accents = ['ff', 'f', '', 's', 'ss']
		pitches = [",,,", ",,", ",", "", "'", "''", "'''"]
		self.all_notes = []
		for p in pitches:
			for l in letters:
				for a in accents:
					self.all_notes.append(Note(l+a+p))

		self.letters = None
		self.name = None

	def __repr__(self):
		string = "\\key " + self.name
		string = string.replace(" minor", " \\minor")
		string = string.replace(" major", " \\major")
		string = string.replace(" harmonic", "")
		string = string.replace(" melodic", "")
		return string +'\n'

	def includes(self, letter):
		return letter in self.letters

	def filter_notes(self):
		self.notes = [n for n in self.all_notes if n.letter in self.letters]

class Melody():
	def __init__(self, key, *notes):
		self.key = key
		if notes:
			self.notes = flatten(notes)
		else:
			self.notes = []

	def __repr__(self):
		return " ".join(str(note) for note in self.notes)

	def __add__(self, other_melody):
		return Melody(self.key, self.notes + other_melody.notes)

	def __radd__(self, other_melody):
		return Melody(other_melody.key, other_melody.notes + self.notes)

	def __mul__(self, number):
		return Melody(self.key, self.notes*number)

	def __rmul__(self, number):
		return Melody(self.key, self.notes*number)

	def __len__(self):
		return len(self.notes)

	def __iter__(self):
		return self.notes.__iter__()

	def __next__(self):
		return self.notes.__next__()

	def __getitem__(self, index):
		if isinstance(index, int):
			if index > 0:
				index -= 1
			return Melody(self.key, self.notes.__getitem__(index))

		new_start = index.start
		new_stop = index.stop
		if isinstance(new_start, int) and new_start > 0:
			new_start -= 1
		if isinstance(new_stop, int) and  new_stop > 0:
			new_stop -= 1
		index = slice(new_start, new_stop, index.step)
		return Melody(self.key, self.notes.__getitem__(index))

	def __setitem__(self, index, value):
		if isinstance(index, int):
			if index > 0:
				index -= 1
			return Melody(self.key, self.notes.__setitem__(index, value))

		new_start = index.start
		new_stop = index.stop
		if isinstance(new_start, int) and new_start > 0:
			new_start -= 1
		if isinstance(new_stop, int) and  new_stop > 0:
			new_stop -= 1
		index = slice(new_start, new_stop, index.step)
		return Melody(self.key, self.notes.__setitem__(index, value))

	def rhythm(self, *rhythm):
		rhythm = flatten(rhythm)
		for i, note in enumerate(self.notes):
			note.dur = str(rhythm[i % len(rhythm)])
		return self

	r = rhythm

	def harmony(self, *harmony):
		harmony = flatten(harmony)
		new_notes = []
		for i, note in enumerate(self.notes):
			this_harmony = harmony[i % len(harmony)]
			this_harmony = map_harmony_to_int(this_harmony)
			if this_harmony == 0 or note.letter == "r":
				new_notes.append(note)
			else:
				if not self.key.includes(note.letter):
					print_error("Cannot build interval on {} as it is not in {}".format(note, key.name))
				index_of_note = [i for i, n in enumerate(self.key.notes) if n.letter == note.letter and n.pitch == note.pitch][0]
				new_note = self.key.notes[index_of_note + this_harmony]
				new_chord = Chord([note, new_note])
				new_notes.append(new_chord)
		self.notes = new_notes
		return self

	h = harmony

	def harmony_note(self, *args):
		notes = []
		harmonies = []
		for i, arg in enumerate(args):
			if i % 2 == 0:
				notes.append(arg)
			else:
				harmonies.append(arg)
		for note, harmony in zip(notes, harmonies):
			harmony = map_harmony_to_int(harmony)
			note = str(Note(note))
			for i, n in enumerate(self.notes):
				if not isinstance(n, Chord):
					if n.chord_repr() == note:
						index_of_note = [i for i, nn in enumerate(self.key.notes) if nn.letter == n.letter and nn.pitch == n.pitch][0]
						new_note = self.key.notes[index_of_note + harmony]
						new_chord = Chord([n, new_note])
						self.notes[i] = new_chord
		return self

	hn = harmony_note

	def harmony_position(self, *args):
		positions = []
		harmonies = []
		for i, arg in enumerate(args):
			if i % 2 == 0:
				positions.append(arg)
			else:
				harmonies.append(arg)

		for position, harmony in zip(positions, harmonies):
			harmony = map_harmony_to_int(harmony)
			current_note = self[position].notes[0]
			index_of_note = [i for i, nn in enumerate(self.key.notes) if nn.letter == current_note.letter and nn.pitch == current_note.pitch][0]
			new_note = self.key.notes[index_of_note + harmony]
			new_chord = Chord([current_note, new_note])
			self[position] = new_chord

		return self

	hp = harmony_position


class Section:
	def __init__(self, name, staves):
		self.name = name
		self.staves = {}
		for staff in staves:
			self.staves[staff] = Melody(key=Key())

	def __getitem__(self, index):
		return self.staves.__getitem__(index)

	def __setitem__(self, index, value):
		return self.staves.__setitem__(index, value)

	def print_stave(self, stave):
		return " ".join(str(note) for note in self[stave]) + "\n"

	def print_score(self, index):
		return " ".join(str(n) for n in self.staves[index])

class Tempo:
	def __init__(self):
		self.name = None

	def __repr__(self):
		return "\\time {}\n".format(self.name)

class Stave:
	def __init__(self, name=None):
		if name is None:
			try:
				self.name = self.type
			except:
				self.name = None
		else:
			self.name = name

	def start(self):
		return (
			'<< \\new Staff {\n' +
			'\\clef {}\n'.format(self.type)
		)

	def end(self):
		return (
			'} >>\n'
		)