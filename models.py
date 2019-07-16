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
			self.notes = self.flatten(notes)
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
		return Melody(self.key, self.notes.__getitem__(index))

	def __setitem__(self, index, value):
		return Melody(self.key, self.notes.__setitem__(index, value))

	def rhythm(self, *rhythm):
		rhythm = self.flatten(rhythm)
		for i, note in enumerate(self.notes):
			note.dur = str(rhythm[i % len(rhythm)])
		return self

	r = rhythm

	def harmony(self, *harmony):
		harmony = self.flatten(harmony)
		new_notes = []
		for i, note in enumerate(self.notes):
			this_harmony = harmony[i % len(harmony)]
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

	def flatten(self, List):
		while any([isinstance(i, list) for i in List]):
			new_list = []
			for i in List:
				if isinstance(i, list):
					new_list += i
				else:
					new_list += [i]
			List = new_list
		return List

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