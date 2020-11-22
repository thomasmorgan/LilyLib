Markup
==========

We've already seen how LilyLib writes music as a list of two kinds of things: `Points` and markup. Points are a class of object introduced by LilyLib that correspond to notes, chords and rests. Markup are strings that modify the presentation of points. We've seen one example of markup already: `key_signature`. This is a property of the `Piece` class and it can be used to insert the current key signature into a piece of music. First the property:

::

    @property
    def key_signature(self):
        return [str(self.key)]

And here's it being used in `demo_keys.py`:

::

	self.score["treble"] += self.key_signature + note(self.key.root + "`", 1, ornamentation=annotation(self.key.name))

Key signatures are unusual though in that they are one of the only kinds of markup that depends on the current state of the piece (the result of calling `key_signature` depends on the key the piece is in at the time the call is made). This is why `key_signature` is a property of the `Piece` class. Most other markup, however, it totally independent of any specific piece and so it resides in the file `markup.py`. This distinction is mirrored between the `Piece` class and `points.py`: functions that depend on the piece are part of the `Piece` class, but functions that don't are in `points.py`. One example is the `scale` function, the `Piece` class contains a version that builds scales in the current key of the piece, while `points.py` contains a version that builds scales in any key, but the key must be passed as an argument.

Here are the functions included in `markup.py`:

**clef** (*clef*)
    Change the clef. e.g. `clef('bass')` inserts the bass clef.

**triplets** (*passage*)
    Returns the passed passage, flagged as triplets.

**grace** (*passage*)
    Returns the passed passage, flagged as grace notes.

**after_grace** (*passage, grace*)
	Returns the passed passage, with the passed grace notes appended as grace notes.

**acciaccatura** (*passage*)
    Returns the passed passage, flagged as acciaccatura (a visual tweak on grace notes).

**ottava** (*passage, shift*)
    Returns the passed passage, with ottava markings. The argument shift specifies the direction and number of octaves by which the printed notes and shifted.

**voices** (*\*voices*)
    Returns a single passage in which all the passed passages are joined as multiple voices. Voices should be ordered from high to low.

**repeat** (*passage, times=2*)
	Returns the passed passage wrapped in repeat bar lines. The times argument is the number of repeats. If this this more than 2 (the default), the number of repeats is printed above the final bar line.

**annotation** (*text*)
	Adds text to the score at this point with the specified content.

**name** (*passage, name*)
	Adds a text label with content *name* to the first point in the passed passage.

**tempo_change** (*tempo*)
    Change the tempo of this stave. For example, *tempo_change('4/4')* changes the tempo to 4/4.
