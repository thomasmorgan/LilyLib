
class Manuscript:

	def __init__(self):
		self.title = ""
		self.subtitle = ""
		self.composer = ""
		self.opus = ""
		self.staves = []
		self.tempo = None

	def __repr__(self):

		score = self.header() + self.start_score()
		for stave in self.staves:
			score += stave.start()
			score += str(self.key)
			score += str(self.tempo)
			for section in self.sections:
				score += self.sections[section].print_stave(stave.name)
			score += stave.end()
		score += self.end_score()
		return score

	def header(self):
		return (
			'\\version "2.18.2"\n' +
			'\\language "english"\n' +
			'\\header {\n' +
			'    title = "{}"\n'.format(self.title) + 
			'    subtitle = "{}"\n'.format(self.subtitle) +
			'    composer = "{}"\n'.format(self.composer) +
			'    mutopiacomposer = ""\n' +
			'    mutopiainstrument = "piano"\n' +
			'    source = ""\n' +
			'    style = "Romatic"\n' +
			'    license = "Creative Commons Attribution-ShareAlike 4.0"\n' +
			'    maintainer = "Anonymous"\n' +
			'    opus = "{}"\n'.format(self.opus) +
			'}\n'
		)

	def start_score(self):
		return (
			'\\score { <<\n'
		)

	def end_score(self):
		return (
	    	'>> }\n'
		)

	def print_error(self, message):
		print("*** ERROR ***: {}".format(message))

	def interval(self, note, size, key=None):
		if key is None:
			key = self.key

		if not key.includes(note.letter):
			self.print_error("Cannot build interval on {}as it is not in {}".format(note, key.name))
		
		index_of_note = [i for i, n in enumerate(key.notes) if n.letter == note.letter and n.pitch == note.pitch]
		index_of_note = index_of_note[0]
		new_note = key.notes[index_of_note + size]
		return Chord([note, new_note])

	def octave(self, note, key=None):
		return self.interval(note, 7, key)

	def rhythm(self, rhythm, notes):
		if not isinstance(rhythm, list):
			rhythm = [rhythm]
		for i, n in enumerate(notes):
			n.duration = str(rhythm[i % len(rhythm)])
		return notes

	def create_sections(self, names):
		self.sections = {}
		for name in names:
			self.sections[name] = Section(name=name, staves=self.staves)

	def rest(self, duration=""):
		return Note("r", duration=duration)

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

class Note:

	def __init__(self, note, duration="", dynamics=""):
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
		self.duration = str(duration)
		self.dynamics = str(dynamics)

	def __repr__(self):
		rep = self.letter + self.pitch + self.duration
		if self.dynamics:
			rep += ("\\" + self.dynamics)
		return rep

	def chord_repr(self):
		rep = self.letter + self.pitch
		return rep



class Chord:

	def __init__(self, notes, duration="", dynamics=""):
		self.notes = []
		for note in notes:
			if isinstance(note, Note):
				self.notes.append(note)
			else:
				self.notes.append(Note(note))
		self.duration = str(duration)
		self.dynamics = str(dynamics)

	def __repr__(self):
		rep = "<"
		for note in self.notes:
			rep += note.chord_repr() + " "
		if self.notes:
			rep = rep[:-1]
		rep += ">" + self.duration
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
		string = string.replace(" major", "")
		return string +'\n'

	def includes(self, letter):
		return letter in self.letters

	def filter_notes(self):
		self.notes = [n for n in self.all_notes if n.letter in self.letters]

class Tempo:

	def __init__(self):
		self.name = None

	def __repr__(self):
		return "\\time {}\n".format(self.name)



