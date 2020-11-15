Core concepts
================

Piece
--------------

When a piece of music is written in LilyLib, it is written as a subclass of the LilyLib class `Piece`. `Piece` is a somewhat powerful class, and you can see the source code in `piece.py`, but for now, we'll look at the two functions all custom pieces must overwrite; `details` and `write_score`. To illustrate, here's the code for a piece that is just middle C played in both hands:

::

	from piece import Piece
	from points import note


	class MiddleC(Piece):

	    def details(self):
	        self.title = "Middle C"

	    def write_score(self):
	        self.score["treble"] = note("c`", 1)
	        self.score["bass"] = note("c`", 1)


	if __name__ == "__main__":
	    MiddleC()


This is what this looks like when it's compiled (via Lilypond) to a pdf:

.. image:: _static/middle_c.png

Let’s go through this line by line. First we import the base class Piece from LilyLib.

::

	from piece import Piece

This is critical because otherwise python doesn’t know what a Piece is. The next line is more python syntax that declares out intention to make a new Piece:

::

	class MiddleC(Piece):

We’ve imaginatively called our `Piece` `MiddleC` and we tag `(Piece)` on the end to let python know that `MiddleC` is a kind of `Piece`. If this is confusing to you, you should take an intro to python course and then everything will become clear.

Our new piece contains two functions: `details` and `write_score`. These contain the meta-data and the musical content of the piece respectively and all pieces must have them. In the details function here we are titling our piece “Middle C”, this is the text that will appear at the top of the pdf after compilation, but we can set other things too. To see what, open `piece.py` and look at the `__init__` function right at the top:

::

	class Piece:

	    def __init__(self):
	        self.title = ""
	        self.subtitle = ""
	        self.composer = ""
	        self.opus = ""
	        self.staves = [Treble(), Bass()]
	        self.tempo = "4/4"
	        self.key = "C Major"
	        self.score = {}

	        self.details()

	        self.set_key(self.key)
	        print(self)

From top to bottom this function sets default values for things like the title, subtitle, composer and so on, before later calling `self.details()`. By writing our own details function and having it change these values we can overwrite things like the title, tempo or key signature, and so on.

The `write_score` function does most of the work though, and for complex pieces it will get quite complex too. But, whatever the piece is, the requirement is that it modifies the score of the `Piece` (referred to as `self.score`) adding the contents of the staves. Here our piece has the default staves: one treble, one bass. We refer to these staves by name; `self.score["treble"]` and `self.score["bass"]`.

::

    def write_score(self):
        self.score["treble"] = note("c`", 1)
    	self.score["bass"] = note("c`", 1)

In this demo, we write the score using the function `note`. This function can be found in points.py (it is imported at the top of the demo) and, as the name suggests, it makes notes, one at a time. Here, both staves get the note c`, which is lilypond notation for middle c. They're also given duration `1` which corresponds to a semibreve.

The last bit of code:

::

	if __name__ == "__main__":
	    MiddleC()

is just python for "when this file runs, run the MiddleC class". This ensures that when the file is executed, it prints out the lilypond for the piece. You'll want the same bit of code (swapping out the class name for whatever you called your piece) at the end of any pieces you write.


Single notes, chords and rests
---------------------------------

The above demo uses the `note` function to create a single note. In general, LilyLib discourages the use of atomistic functions like this, in favor of higher-level functions we'll come to later. However, we'll look at a few low-level functions first to get comfortable with what's going on under-the-hood. `note` take three arguments: the tone of the note (effectively the "name" of the sound produced; a combination of letter, accent and pitch), the duration of the note, and, optionally, any ornamentation. It builds notes one at a time, but these are returned in lists and so can be concatenated by adding. Here's a simple example with 4 notes of various tones, durations and ornamentation:

::

    def write_score(self):
        self.score["treble"] = note("c`", 4) + note("e`", '4.', "~") + note("e`", 8) + note("c`", 4, "\\staccato")
        self.score["bass"] = note("c`", 1)


.. image:: _static/core_concepts_fig1.png

We'll discuss tones in more detail shortly. But for now, note that durations are integers, unless they are dotted in which case they are strings. Note also that ornamentation is a string and it follows lilypond conventions, however any slashes must be double to make it through the python interpreter, so `~` starts a tie, whereas `\\staccato` adds the staccato point.

The function `rest` lets you make rests. It behaves just like `note` however you only need to specify a duration (because rests don't have a tone or ornamentation). Here's the same code from above, but switching out the third note for a rest:

::

    def write_score(self):
        self.score["treble"] = note("c`", 4) + note("e`", '4.', "~") + rest(8) + note("c`", 4, "\\staccato")
        self.score["bass"] = note("c`", 1)

.. image:: _static/core_concepts_fig2.png

Just remember that these functions reside in `points.py` and to use them in a piece you need to import them like so:

::

	from piece import Piece
	from points import note, rest

To create chords, `piece.py` includes the function `chord`. Like `note` it accepts a duration and, optionally, ornamentation. However, it lets you specify multiple tones. These tones can either be specified as a python list of multiple tone strings or a single string consisting of multiple tones separated by a single space. The file `demo_c_major_chord.py` shows both:

::

	from piece import Piece
	from points import chord


	class CMajorChord(Piece):

	    def details(self):
	        self.title = "C Major Chord"

	    def write_score(self):
	        self.score["treble"] = chord("c` e` g` c``", 1)
	        self.score["bass"] = chord(["c,", "c"], 1)


	if __name__ == "__main__":
	    CMajorChord()

.. image:: _static/core_concepts_demo_chord.png


Multiple notes, chords and rests
-------------------------------------

The functions `note`, `chord` and `rest` each return a single item, but each function has a corresponding function that returns multiple items. These are called `notes`, `chords` and `rests`, respectively. All of them behave just like their singular counterparts, but take lists of arguments. Let's start with `rests`. In this case, the only argument is the duration of the rests and so the user must supply a list of these durations (or a string of multiple durations separated by spaces). For example:

::

    def write_score(self):
        self.score["treble"] = rests([2, 4, 8, 16, 32, 32])
        self.score["bass"] = note("c`", 1)

.. image:: _static/core_concepts_rests.png

`notes` behaves similarly. You can provide a list of tones, a list of durations or a list of ornamentation (all of which can either be a list or a single string with spaces separating the multiple values). Which ever list is longest determines the total number of notes created, and shorter lists are cycled to reach the length of the longest list. This helps efficiency, so if you want multiple notes with different tones, but the same duration and ornamentation, you only need list out the tones:

::

	def write_score(self):
		self.score["treble"] = notes("c` d` e` f`", 4)
		self.score["bass"] = notes("c` g e c", 4)

.. image:: _static/core_concepts_notes1.png

Here's a more complicated example:

::

	def write_score(self)
		self.score["treble"] = notes('c` c` f` e`', '4 8 4. 4', "~   ") * 2
		self.score["bass"] = notes('c g g c', '4. 8 8 4.', " ~") * 2

.. image:: _static/core_concepts_notes2.png

There's a couple of things to note here: First, the durations are specified as a single string separated by spaces. Second, ornamentation is a single string too, but excess whitespace is used to give some notes no ornamentation at all. So in the treble clef `"~   "` means start a tie on every 4th note, starting with the first. While in the bass clef, `" ~"` means start a tie on every other note, starting with the 2nd. Lastly, because all these functions return lists of notes/rests/etc. you can multiple the result to continue the pattern. Here it is multipled by 2, doubling the passage.

The `notes` function can also return a mix of rests and notes, and rests are indicated by either whitespace (in a single string) or an empty list (`[]`) in a list. To illustrate:

::

    def write_score(self):
		self.score["treble"] = notes("c`  e` ", 4)
		self.score["bass"] = notes(["c`", [], [], "c"], 4)

.. image:: _static/core_concepts_notes_and_rests.png

Lastly, the `chords` function can create multiple chords. As with `notes`, duration and ornamentation can be single values or lists (or strings containing multiple elements separated by spaces). The first argument, however, must be either a list-of-lists of tones, or a list of strings, each of which can contain multiple tones. Here's an example:

::

    def write_score(self):
        self.score["treble"] = chords(["c` e` g` c``", "b d` g` b`", "c` f` a` c``", "c` e` g` c``"], 4)
        self.score["bass"] = chords([["c,", "c"], ["g,", "g"], ["f,", "f"], ["c,", "c"]], 4)

.. image:: _static/core_concepts_chords.png


Points
----------

So far we've been talking about notes, chords and rests as if they were different things. However, under the hood they are actually all instances of the same class, `Point`. In LilyLib a `Point` is any element that appears in sheet music and corresponds to some sound (or absence of sound). These can be differentiated from what Lilylib calls `markup` which are other things that appear on sheet music, but are not sounds (things like annotations, or flagging a series of printed notes as grace notes, but more on this later).

You can see the code for the `Point` class in `points.py`, but it's quite simple. A `Point` consists of a duration and oramentation, which are stored as single values, and a list of tones. It is the contents of the tones list that determines it's behavior when printed. If tones is empty, it prints as a rest, if tones contains a single tone it prints as a note, and if tones contains multiple tones it prints as a chord:

::

    def __str__(self):
        if self.is_rest:
            return 'r' + str(self.dur) + self.ornamentation
        elif self.is_note:
            return self.tone + str(self.dur) + self.ornamentation
        elif self.is_chord:
            return "<" + " ".join(self.tones) + ">" + str(self.dur) + self.ornamentation
        else:
            raise ValueError("Cannot print {} as it is neither a rest, nor note, nor chord. Its tones are {}".format(self, self.tones))

Points have a handful of other function too. For instance you can use `is_rest`, `is_note` and `is_chord` to check what kind of thing a Point is:

::

    @property
    def is_rest(self):
        return len(self.tones) == 0

    @property
    def is_note(self):
        return len(self.tones) == 1

    @property
    def is_chord(self):
        return len(self.tones) > 1

If you are confident a Point is currently behaving like a note, you can also ask for its tone, or even split the tone into a letter or pitch:

::

    @property
    def tone(self):
        if len(self.tones) == 1:
            return self.tones[0]
        else:
            raise AttributeError("Cannot get {}.tone as it has multiple tones: {}".format(self, self.tones))

    @property
    def letter(self):
        return letter(self.tone)

    @property
    def pitch(self):
        return pitch(self.tone)

Lastly, you can add new tones to a Point, remove existing tones, or even replace specific tones with new ones:

::

    def add(self, tones):
        tones = flatten([tonify(tones)])
        for tone in tones:
            if tone not in self.tones:
                self.tones.append(tone)

    def remove(self, tones):
        tones = flatten([tonify(tones)])
        self.tones = [tone for tone in self.tones if tone not in tones]

    def replace(self, old_tones, new_tones):
        old_tones = flatten([tonify(old_tones)])
        new_tones = tonify(new_tones)
        new_tones = new_tones if isinstance(new_tones, list) else [new_tones]

        max_length = max(len(old_tones), len(new_tones))
        zip_list = zip(range(max_length), cycle(old_tones), cycle(new_tones))

        for i, old_tone, new_tone in zip_list:
            if old_tone in self.tones:
                self.remove(old_tone)
                self.add(new_tone)

These functions are only possible because rests, notes and chords are all just Points. For instance, adding a tone to a rest makes it immediately behave like a note. Similarly, if you keep removing tones from a chord it will turn first into a note and then into a rest.

As a slight digression, the word `Point` was chosen as it is suitably generic to subsume rests, notes and chords, but also because it has a historical tie-in: In the middle ages, written notes, which often lacked stems, were referred to with the Latin word 'punctum' which translates to the modern English word point. One vestige of this is the word 'counterpoint' which refers to music comprising multiple voices that overlap each other. Early composers described this style of music as '`punctum contra punctum`', which means `note against note`, and this phrase was later condensed to counterpoint.

Tones
----------

We've encountered the word "tone" a lot so far: `Points` have tones (one if they're a note, multiple if they're a chord, none if they're a rest) and the `note`, `notes`, `chord` and `chords` functions all take one or more tones as an argument. But what exactly is a tone? The good news is that it's quite basic: a tone is just a string and there is no special `Tone` class. Not all strings are tones though, and for a string to be a valid tone it must correspond to a sound an instrument can make. We can see how all possible tones are contructed inside `tones.py`. First, note that a tone is made of a letter and a pitch, and that the letter itself can be decomposed into a base letter and an accent. Here's the code for these:

::

	all_base_letters = ['c', 'd', 'e', 'f', 'g', 'a', 'b']
	all_accents = ['ff', 'f', '', 's', 'ss']
	all_pitches = [",,,", ",,", ",", "", "`", "``", "```"]

The list of all possible letters, and, in turn, all possible tones, is then constructed as follows:

::

	all_letters = flatten([[letter + accent for accent in all_accents] for letter in all_base_letters])
	all_tones = flatten([[letter + pitch for letter in all_letters] for pitch in all_pitches])

So `all_tones` includes everything all the way from `cff,,,` to `bss\`\`\``. Note that this list includes what one might call duplicates, for instance, `es` and `f` are both valid tones. LilyLib is vaguely aware of this and `tones.py` includes a dictionary of equivalent letters and a function to translate between equivalent tones:

::

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

	def equivalent_tone(tone):
	    new_letter = equivalent_letters[letter(tone)]
	    if base_letter(tone) == 'c' and base_letter(new_letter) == 'b':
	        new_pitch = all_pitches[all_pitches.index(pitch(tone)) - 1]
	    elif base_letter(tone) == 'b' and base_letter(new_letter) == 'c':
	        new_pitch = all_pitches[all_pitches.index(pitch(tone)) + 1]
	    else:
	        new_pitch = pitch(tone)
	    new_tone = new_letter + new_pitch
	    return new_tone

However these don't handle double sharps or double flats currently. It's also worth noting that the equivalence of these tones is an artefact of modern equal tuning. Prior to the 20th century it was widely accepted that there were subtle differences between, say, f-sharp and g-flat, and different tuning systems placed them at difference frequencies. Some pianos were even made with split black keys allowing the performer to select which of the tones they wanted.

Just as `tones.py` inlcudes instructions for building tones, it also provides functions to decompose a tone into it's letter, pitch, accent, and base letter:

::

	def separate(tone):
	    tone = tonify(tone)
	    if tone[-1] in ["`", ","]:
	        split = tone.split(tone[-1], 1)
	        return split[0], split[1] + tone[-1]
	    else:
	        return tone, ''


	def pitch(tone):
	    return separate(tone)[1]


	def letter(tone):
	    return separate(tone)[0]


	def accent(tone):
	    let = letter(tone)
	    if len(let) == 1:
	        return ''
	    else:
	        return let[-1]


	def base_letter(tone):
	    return letter(tone)[0]

You can also sharpen or flatten tones:

::

	def flatten(tone):
	    let = letter(tone)
	    if len(let) == 1 or let[-1] == 'f':
	        return let + 'f' + pitch(tone)
	    else:
	        return let[:-1] + pitch(tone)


	def sharpen(tone):
	    let = letter(tone)
	    if len(let) == 1 or let[-1] == 's':
	        return let + 's' + pitch(tone)
	    else:
	        return let[:-1] + pitch(tone)

The last function in `tones.py` is the one users will encounter most often: `tonify`. This takes a string, or a (nested) list of strings, and parses the contents to make sure all strings are valid tones. Where strings include white space, they are split into a list of multiple strings, and each substring is checked for validity. Where a string contains multiple adjacent spaces, the empty gasps are replaced with empty lists in order to produce rests (assuming the returned list is used to create Points). Note, however, that `tonify` respects whatever nesting is present in the value it is passed and it does not flatten the list. If `tonify` is passed something that is neither a string nor a list, it gambles that it's been passed a `Point` and attempts to extract the tones from it, this way you can use `tonify` to get back to tones from Points. However, if this fails an error is raised.

::

	def tonify(item):
	    """ Returns an unflattened list of valid tones and empty lists.

	    Multi-tone strings are split into lists of valid tones. A seris of N spaces is
	    converted into a seris of N-1 empty lists. These produce rests when assigned to
	    Points, but will be erased by flattening the list. """

	    if isinstance(item, list):
	        return [tonify(subitem) for subitem in item]
	    elif isinstance(item, str):
	        if " " in item:
	            split_tones = item.split(" ")
	            split_tones = [tone if tone != '' else [] for tone in split_tones]
	            return tonify(split_tones)
	        else:
	            if item not in all_tones:
	                raise ValueError("{} is not a valid tone.".format(item))
	            return item
	    else:
	        try:
	            return item.tones
	        except AttributeError:
	            raise ValueError("Cannot tonify {}".format(item))

Here's a few examples of what it does:

::

	>>> tonify('cs,,')
	'cs,,'

	>>> tonify('cs,, es,, gs,, cs,')
	['cs,,', 'es,,', 'gs,,', 'cs,']

	>>> tonify('cs,,   cs,')  # note the two extra spaces here to create rests
	['cs,,', [], [], 'cs,']

	>>> tonify(['cs,,', 'es,,', 'gs,,', 'cs,'])
	['cs,,', 'es,,', 'gs,,', 'cs,']

	>>> tonify(['cs,, es,,', 'gs,, cs,'])  # note the argument here is a list of two strings
	[['cs,,', 'es,,'], ['gs,,', 'cs,']]

In many instances users won't be calling tonify themselves, but many functions (like `notes` and `chords`) do, to ensure the passed values are valid and to convert them into a usable form.