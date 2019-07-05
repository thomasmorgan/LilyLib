class Note:
	def __init__(self, note, dur="", dynamics="", art=""):
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
		self.dynamics = str(dynamics)
		self.articulation = str(art)

	def __repr__(self):
		rep = self.letter + self.pitch + self.dur + self.articulation
		if self.dynamics:
			rep += ("\\" + self.dynamics)
		return rep

	def chord_repr(self):
		rep = self.letter + self.pitch
		return rep

class Chord:
	def __init__(self, notes, dur="", dynamics="", art=""):
		self.notes = []
		if isinstance(notes, str):
			notes = notes.split(" ")
		for note in notes:
			if isinstance(note, Note):
				self.notes.append(note)
			else:
				if note:
					self.notes.append(Note(note))
		self.dur = str(dur)
		self.dynamics = str(dynamics)
		self.articulation = str(art)

	def __repr__(self):
		rep = "<"
		for note in self.notes:
			rep += note.chord_repr() + " "
		if self.notes:
			rep = rep[:-1]
		rep += ">" + self.dur + self.articulation
		if self.dynamics:
			rep += ("\\" + self.dynamics)
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

class Section:
	def __init__(self, name, staves):
		self.name = name
		self.score = {}
		for stave in staves:
			self.score[stave.name] = []

	def print_stave(self, stave):
		return " ".join(str(note) for note in self.score[stave]) + "\n"

	def print_score(self, index):
		return " ".join(str(n) for n in self.score[index])

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