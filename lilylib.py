from models import *
from util import *
from keys import *
from tempi import *
from staves import *

title = ""
subtitle = ""
composer = ""
opus = ""
staves = []
tempo = None
key = CMajor()

def header():
	return (
		'\\version "2.18.2"\n' +
		'\\language "english"\n' +
		'\\header {\n' +
		'    title = "{}"\n'.format(title) + 
		'    subtitle = "{}"\n'.format(subtitle) +
		'    composer = "{}"\n'.format(composer) +
		'    mutopiacomposer = ""\n' +
		'    mutopiainstrument = "piano"\n' +
		'    source = ""\n' +
		'    style = "Romatic"\n' +
		'    license = "Creative Commons Attribution-ShareAlike 4.0"\n' +
		'    maintainer = "Anonymous"\n' +
		'    opus = "{}"\n'.format(opus) +
		'}\n'
	)

def start_score():
	return (
		'\\score { <<\n'
	)

def end_score():
	return (
    	'>> }\n'
	)

def notes(notes, dur="", art=""):
	notes = notes.split(" ")
	new_notes = []
	for note in notes:
		if note:
			new_notes.append(Note(note, dur=dur, art=art))
	return new_notes

N = notes

def notify(n):
	if isinstance(n, str):
		return notes(n)
	return n

def scale(start, stop):
	if not isinstance(start, Note):
		start = Note(start)
	if not isinstance(stop, Note):
		stop = Note(stop)
	
	index_of_start = [i for i, n in enumerate(key.notes) if n.letter == start.letter and n.pitch == start.pitch][0]
	index_of_stop = [i for i, n in enumerate(key.notes) if n.letter == stop.letter and n.pitch == stop.pitch][0]

	if index_of_stop > index_of_start:
		notes = key.notes[index_of_start:index_of_stop + 1]
	else:
		notes = key.notes[index_of_stop:index_of_start + 1]
		notes.reverse()

	new_notes = []
	for n in notes:
		new_notes.append(Note(n.letter + n.pitch))

	return new_notes

S = scale

def chord(root, notes):
	if not isinstance(root, Note):
		root = Note(root)

	if not key.includes(root.letter):
		print_error("Cannot build chord on {}as it is not in {}".format(note, key.name))

	index_of_root = [i for i, n in enumerate(key.notes) if n.letter == root.letter and n.pitch == root.pitch][0]

	new_notes = []
	for note in notes:
		new_note = key.notes[index_of_root + note]
		new_notes.append(new_note)

	chord = Chord(new_notes)
	return [chord]

C = chord


def interval(notes, size):
	if isinstance(notes, str):
		notes = notes.split(" ")
	if isinstance(notes, Note):
		notes = [notes]

	new_notes = []
	for note in notes:
		if note:
			if not isinstance(note, Note):
				note = Note(note)

			if not key.includes(note.letter):
				print(note.letter)
				print(key.letters)
				print_error("Cannot build interval on {} as it is not in {}".format(note, key.name))
			
			index_of_note = [i for i, n in enumerate(key.notes) if n.letter == note.letter and n.pitch == note.pitch][0]
			new_note = key.notes[index_of_note + size]
			new_chord = Chord(note.chord_repr() + " " + new_note.chord_repr())
			new_chord.dur = note.dur
			new_notes.append(new_chord)
	return new_notes

I = interval

def second(note):
	return interval(note, 1)

def third(note):
	return interval(note, 2)

def third_b(note):
	return interval(note, -5)

def fourth(note):
	return interval(note, 3)

def fourth_b(note):
	return interval(note, -4)

def fifth(note):
	return interval(note, 4)

def fifth_b(note):
	return interval(note, -3)

def sixth(note):
	return interval(note, 5)

def sixth_b(note):
	return interval(note, -2)

def seventh(note):
	return interval(note, 6)

def octave(note):
	return interval(note, 7)

O = octave

def rhythm(rhythm, notes):
	if not isinstance(rhythm, list):
		rhythm = [rhythm]
	for i, n in enumerate(notes):
		n.dur = str(rhythm[i % len(rhythm)])
	return notes

def create_sections(names):
	sections = {}
	for name in names:
		sections[name] = Section(name=name, staves=staves)
	return sections

def rest(dur=""):
	durs = dur.split(" ")

	rests = []
	for dur in durs:
		if dur:
			rests.append(Note("r", dur=dur))
	return rests

R = rest

def voices():
	return(["\n<<\n{"])

V = voices()

def change_voice():
	return(["} \\\\ {"])

CV = change_voice()

def end_voices():
	return(["}\n>>\n"])

EV = end_voices()

def print_score():
	score = header() + start_score()
	for stave in staves:
		score += stave.start()
		score += str(key)
		score += str(tempo)
		for section in sections:
			score += sections[section].print_stave(stave.name)
		score += stave.end()
	score += end_score()
	print(score)




