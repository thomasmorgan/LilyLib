Writing music
=========================

So far we have seen how music in LilyLib is composed of *Points*, and how we can use the *notes*, *rests* and *chords* functions to make multiple *Points*. In this section we'll look at functions that let us quickly writes higher-level musical entities, things like scales and arpeggios, as well as perform operations like transposition and harmonization.

.. NOTE::
	All these functions exist in two versions, one found in *points.py*, the other within the the Piece class in *piece.py*. The difference between the two is that the functions in *points.py* need to be told what key they are operating in, while the those within the Point class automatically operate in the current key of the piece. If you look at the code, you'll see the functions in the Piece class are just wrappers the call the functions in *points.py* but pass the piece's current key as an argument.

Scales
-----------

The *scale* function within *points.py* returns a list of points corresponding to a series of notes drawn from a scale. Here's the function:

::

	def scale(start, stop_or_length, key, dur=None, step=1):
	    key = keyify(key)
	    return series(key.tones, start, stop_or_length, dur, step)

The arguments are:

- *start*; the tone at which to start the scale (can be a Point too, the tone will be automatically extracted).
- *stop_or_length*; either the tone at which to stop, or the desired length of the scale (negative lengths create descending scales).
- *key*; the key in which to write the scale (see below for details)
- *dur*; the duration of any notes, can be a single value or a list of values which will be cycled. If no value is provided the function returns tones, and not Points.
- *step*; the step size. 1 = a full scale, 2 = every other note, 3 = every third note, and so on.

The *demo_c_major_scale* provides an example:

::

	from piece import Piece
	from points import scale


	class CMajorScale(Piece):

	    def details(self):
	        self.title = "C Major Scale"

	    def write_score(self):
	        self.score["treble"] = scale("c`", "c``", 'C Major', 8) + scale("c``", -8, 'C Major', 8)
	        self.score["bass"] = self.scale("c`", "c", 8) + self.scale("c", 8, 8)


	if __name__ == "__main__":
	    CMajorScale()

.. image:: _static/scales.png

First look at the treble clef. Note how the first scale specifies a stop tone, but the second specifies a numeric length. Both specify the key as C Major, and the duration as 8 (i.e. quavers). The bass is different though, it doesn't specify a key and it calls *self.scale* instead of *scale*. This is because the `Piece` class offers wrappers to all these functions, with the only difference being that it automatically passes the current key of the piece. In this way you can use *self.scale* to compose in the dominant key of the piece, but *scale* when you want to create scales in another key. The demo `c_major_modal_scales` shows this in action, we'll deal with it in two parts. The first is:

::

	from piece import Piece
	from tones import letter
	from points import scale
	from util import join


	class CMajorModalScales(Piece):

	    def details(self):
	        self.title = "C Major Modal Scales"

	    def write_score(self):
	        # The looped section programmatically builds a series of scales
	        # Note that the bass clef is just a tansposition of the treble clef
	        looped = {"treble": []}
	        for start in self.scale('c`', 'c``'):
	            looped["treble"] += self.scale(start, 8, 8)
	        looped["bass"] = self.transpose(looped["treble"], -1, 'octave')

.. image:: _static/modal_scales1.png

Note how first a scale of tones is generated, and then these tones are used as the start notes of a series of scales, all in the key of C Major. The bass clef is just a transposition of the treble clef, but more on transposition below.

::

	        # The smart section programmatically builds a series of scales in different keys
	        # Note how we use list comprehension to avoid a for loop, and use step = 2 to play every other note in the treble clef
	        start_notes = self.scale('c```', 'c``')
	        smart = {
	            "treble": [scale(start, -8, key=letter(start) + " major", dur=8, step=2) for start in start_notes],
	            "bass": [scale(self.transpose(start, -1, 'octave'), -8, key=letter(start) + " major", dur=8) for start in start_notes]
	        }

	        self.score = join(looped, smart)


	if __name__ == "__main__":
	    CMajorModalScales()


.. image:: _static/modal_scales2.png

The second part does the same thing, but note it takes the letter of the start tone and combines it with the word "major" to set the key. Thus the key of the scale changes with the start note. Keys are actually a class of object in Lilylib (see later docs), but they can be referred to with strings of the format "<base letter> <mode>", for instance: "c major", "fs minor", "bf harmonic". The lookup function is case insensitive, so capitalization does not matter.

In addition, note in the above demo that the treble clef sets the 'step' argument to 2, so the treble clef covers two octaves and catches up with the bass clef. Lastly, note that the score is the combination of the two dictionaries called `looped` and `smart` and they are combined with the function `join` which is imported from `util.py`.

Arpeggios
-----------

In addition to `scale`, `points.py` includes the function `arpeggio`, and `Piece` has a corresponding function which can be called with `self.arpeggio` too. Here's the function:

::

	def arpeggio(start, stop_or_length, key, dur=None, step=1):
	    key = keyify(key)
	    return series(key.arpeggio_tones, start, stop_or_length, dur, step)


Note it takes all the same arguments as the scale function. Just remember that the start tone must be part of the arpeggio in the key you are working with, so trying to start a C Major arpeggio on F won't get you very far. This function can be seen in action in the demo_arpeggios code:

::

	from piece import Piece
	from points import note, notes, arpeggio
	from util import join


	class Arpeggios(Piece):

	    def details(self):
	        self.title = "Arpeggios"

	    def write_score(self):
	        # The basic section manually builds a scale note by note
	        basic = {
	            "treble": [note("c`", 8), note("e`", 8), note("g`", 8), note("c``", 8)],
	            "bass": [note("c", 8), note("e", 8), note("g", 8), note("c`", 8)]
	        }

	        # The notes section uses the notes function to build a list of notes from a single string
	        intermediate = {
	            "treble": notes('d` fs` a` d``', 8),
	            "bass": notes('d fs a d`', 8)
	        }

	        # The arpeggio section uses the arpeggio function to build a scale from one note to the next
	        arpeggios = {
	            "treble": arpeggio('e`', 'e``', 'E Major', 8),
	            "bass": arpeggio('e', 4, 'E major', 8)
	        }

	        # The length section uses the arpeggio function to build an arpeggio, but specifies a length, rather than a stop note
	        length = {
	            "treble": arpeggio('f`', 4, 'F Major', 8),
	            "bass": arpeggio('f', 4, 'F Major', 8)
	        }

	        starts = self.arpeggio('c`', 'c``')
	        stepped = {
	            'treble': [[self.arpeggio(start, self.transpose(start, 7), 16, step=step) for step in [3, 3, 1]] for start in starts],
	            'bass': [[self.arpeggio(self.transpose(start, -7), start, 16, step=step) for step in [1, 3, 3]] for start in starts]
	        }

	        self.score = join(basic, intermediate, arpeggios, length, stepped)


	if __name__ == "__main__":
	    Arpeggios()


.. image:: _static/arpeggios.png

This shows a variety of ways you can make arpeggios. First using the `note` and `notes` functions, but then with `arpeggio` function itself. The `stepped` section uses a list of values for the step argument (along with pythonic list comprehension) to create something reminiscent of Beethoven's 3rd piano sonata.

Other series
---------------

Lilylib also includes functions that generate other common series of tones:

- arpeggio7; arpeggios including the 7th
- dominant7; dominant 7ths
- diminished7; diminished 7ths
- chromatic; chromatic scales

Note that the dominant and diminished 7ths are the same for major, minor and harmonic versions of the same key. The chromatic function also follows convention by using sharps when the scale is ascending, and flats when descending, as this minimizes the number of accidentals. Here's the chromatic demo:

::

	from piece import Piece


	class ChromaticScales(Piece):

	    def details(self):
	        self.title = "Chromatic Scales in C and F Major"

	    def write_score(self):
	        self.score["treble"] = self.chromatic('c`', 'c``', [16] * 12 + [4]) + self.chromatic('c``', 'c`', [16] * 12 + [4])

	        self.set_key("f major")
	        self.score["treble"] += key_signature(self.key, self.chromatic('f`', 'f``', [16] * 12 + [4])) + self.chromatic('f``', 'f`', [16] * 12 + [4])

	        self.score["bass"] = self.transpose(self.score["treble"], -1, 'octave')


	if __name__ == "__main__":
	    ChromaticScales()

.. image:: _static/chromatic.png

You can also create custom scales with `scale_subset`:

::

	def scale_subset(positions, start, stop_or_length, key, dur=None, step=1):
	    key = keyify(key)
	    custom_tones = key.scale_subset(positions)
	    return series(custom_tones, start, stop_or_length, dur, step)

Here, `positions` is a list of numbers describing the points of the regular scale you want to include. So setting `positions` to [1, 3, 5] would produce regular arpeggios. Similarly, a scale subset with positions [1, 3] would include only root and third notes.

Tranposition
----------------

We've seen `transpose` used a few times above. It takes an (arbitrarily nested) list of Points or tones, transposes each item by the specified interval, and then returns the result. It's a long function so we won't show it all here, but here are the arguments:

::

	def transpose(item, shift, key, mode="scale", clean=False):

- *item*; the thing you want to transpose
- *shift*; the interval you want it transposed by
- *key*; the key in which the transposition occurs
- *mode*; the "`kind`" of transposition. Either 'scale', 'octave' or 'semitone'.
- *clean*; whether or not the transposed passage is stripped on any ornamentation (etc.)

You need to specify a key because otherwise transposing according to a scale is not possible. Most of the cases we've seen above are where the bass clef is a -1 octave (or -7 scale) transposition of the treble clef.

Here's the bit of the function that does the transposing (by this point it is working only with tones):

::

    try:
        if mode == "octave":
            new_pitch = all_pitches[all_pitches.index(pitch(item)) + shift]
            return letter(item) + new_pitch
        elif mode == "scale":
            current_index = key.tones.index(item)
            return key.tones[current_index + shift]
        elif mode == "semitone":
            return key.all_tones[key.all_tones.index(item) + shift]
    except ValueError:
        return transpose(equivalent_tone(item), shift, key, mode)

Note how if transposition fails, it tries again with the equivalent tone. This means if you try to transpose g-flat two steps up the scale of D Major, it will initially fail (g-flat is not in D Major) but will then transform g-flat to f-sharp, which can then be transposed to a.

Lastly note that transposing a Point does not return a modified version of the original Point, but creates an entirely new Point. So if passage B is a transposition of passage A, modifications of A after the transposition has occurred will not affect B. Nonetheless, ornamentation that is present at the time of transposition will be added to the new passage.

Harmonization
-----------------

Lots of music involves relatively simple structures, like scales, but with harmonies imposed on the top. Lilylib can do this with the function `harmonize`. This function builds off `transpose`, but also another function `merge`. The `merge` function takes two or more lists of points, and smushes them together to make a single list. This has a few limitations: to work the multiple passages must have the same number of points in them, and if their durations differ then the durations of the first passage overwrite the others. Lastly, if the multiple series have a nested structure then the return list will have the same structure as the first series the function is passed. Here's an example:

::

	from piece import Piece
	from points import rests, merge


	class Merge(Piece):

	    def details(self):
	        self.title = "Merged Scales"

	    def write_score(self):
	        scale_1 = self.scale("c`", 8, 8)
	        scale_2 = self.scale("c``", -8, 8)

	        self.score["treble"] = scale_1 + scale_2 + merge(scale_1, scale_2)
	        self.score["bass"] = rests(1, 1, 1)


	if __name__ == "__main__":
	    Merge()

.. image:: _static/merge.png

You might be tempted to use the merge function to write music with multiple voices, and while that is possible, it removes any visual indication of the voices and so this is not the recommended method. For a better approach to voices see the section on markup.

With merge covered let's return to harmonize. The harmonize function works by first transposing points to the desired intervals and then merging the result with the original points:

::

	def harmonize(points, interval, key, mode="scale"):
	    return merge(points, transpose(points, interval, key, mode))

Here's a demo:

::

	from piece import Piece


	class Harmonize(Piece):

	    def details(self):
	        self.title = "Harmonized notes"

	    def write_score(self):

	        rh_melody = self.arpeggio('c`', 4, 4)
	        lh_melody = self.transpose(rh_melody, -1, 'octave')

	        self.score = {
	            'treble': self.harmonize(rh_melody, 3),
	            'bass': self.harmonize(lh_melody, -1, 'octave')
	        }


	if __name__ == "__main__":
	    Harmonize()

.. image:: _static/harmonize.png
