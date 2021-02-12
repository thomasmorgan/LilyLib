Keys and changing key
==============================

So far almost all the music we've seen set a key at the very start in the *details* function (or stuck with the default of C Major) and then wrote in that key. However, music often changes keys, in fact we've already seen one example of this with the chromatic scales demo:

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

Note how `self.set_key` is used to switch from C Major to F Major. This chapter will go into Keys in a little more detail.

The Key class and subclasses
------------------------------

LilyLib includes a `Key` class and it's located inside keys.py. Specific keys, like C Major, are subclasses of the rather abstract parent class, and all the key subclasses are in `keys.py` too. Each key is defined by a root letter, the letters included in the key's scale, and a name. These values are set when the key is created, by the `__init__` function of the `Key` class. Here's the code:

::

    def __init__(self):
        # define must be overwritten in subclasses to:
        # 1. set the root letter
        # 2. set the included letters
        # 3. set the key's name
        self.root = None
        self.letters = None
        self.name = None
        self.define()
        self.confirm_definition()

As you can see all the values are set to `None` by default, so for the key to "work" they must be overwritten, and this is done by the `define` function of each subclass. In the parent class `define` just raises an error:

::

    def define(self):
        raise NotImplementedError("Key.define must be overwritten.")

But in each subclass it has meaningful content:

::

	class CFlatMajor(Key):
	    def define(self):
	        self.root = 'cf'
	        self.letters = ['cf', 'df', 'ef', 'ff', 'gf', 'af', 'bf']
	        self.name = "c flat major"

In fact, overwriting `define` like this is all that needs to be done to create a specific key. After `define` is called the parent class runs `confirm_definition` to check that the values have all been set:

::

    def confirm_definition(self):
        if None in [self.root, self.letters, self.name]:
            raise ValueError("Must define root, letters and name of Key {}".format(self))

With these values set, the key behaves like a collection of sets of tones that can then be used to build things like scales or arpeggios. For instance, scales can be built by getting the `tones` property of the key:

::

    @property
    def tones(self):
        return [t for t in self.all_tones if letter(t) in self.letters]

This returns an ordered list of all tones whose letter is part of the scale of the key. There's similar properties for arpeggios, arpeggios including the 7th, dominant 7ths, diminished 7ths, and chromatic scales.

You can also get "relative letters" of a key. These can be referred to with roman numerals, or by name. For instance, F-sharp is the 2nd letter of E Major and the following properties will all return `fs`:

::

    @property
    def supertonic(self):
        return self.relative_letter(1)

    @property
    def ii(self):
        return self.supertonic

    @property
    def II(self):
        return self.supertonic

Or, in the terminal:

::

	>>> from keys import EMajor
	>>> key = EMajor()
	>>> key.ii
	'fs'
	>>> key.II
	'fs'
	>>> key.supertonic
	'fs'

LilyLib includes all "real" keys in keys.py (i.e. it does not include impossible/theoretical keys which include double sharps or double flats in their key signature) including both natural and harmonic versions of minor keys. For instance:

::

	class GMinor(Key):
	    def define(self):
	        self.root = 'g'
	        self.letters = ['c', 'd', 'ef', 'f', 'g', 'a', 'bf']
	        self.name = "g minor"


	class GMinorH(Key):
	    def define(self):
	        self.root = 'g'
	        self.letters = ['c', 'd', 'ef', 'fs', 'g', 'a', 'bf']
	        self.name = "g minor harmonic"

This is useful because, even though harmonic key signatures are not printed in sheet music, pieces are often written in the harmonic as opposed to natural minor.

The key dictionary
---------------------

The last thing `keys.py` does is create a dictionary of all the keys and provide a function, 'keyify', to get keys from this dictionary:

::

	key_dictionary = {
	    "major": {
	        "cf": CFlatMajor(),
	        "c": CMajor(),
	        "cs": CSharpMajor(),
	        ...
	        "a": AMajor(),
	        "bf": BFlatMajor(),
	        "b": BMajor()
	    },
	    "minor": {
	        "c": CMinor(),
	        "cs": CSharpMinor(),
	        "d": DMinor(),
	        ...
	        "as": ASharpMinor(),
	        "bf": BFlatMinor(),
	        "b": BMinor()
	    },
	    "harmonic": {
	        "c": CMinorH(),
	        "cs": CSharpMinorH(),
	        "d": DMinorH(),
	        ...
	        "as": ASharpMinorH(),
	        "bf": BFlatMinorH(),
	        "b": BMinorH()
	    }
	}

In this way, you can get Key objects by their name, e.g. `key_dictionary['major']['af']` will return an instance of the `AFlatMajor` class. The `keyify` function simply provides a nicer way to do this:

::


	def keyify(key):
	    if isinstance(key, Key):
	        return key
	    elif isclass(key) and issubclass(key, Key):
	        return key()
	    elif isinstance(key, str):
	        try:
	            key = key.split(" ")
	            letter = key[0].lower()
	            mode = " ".join(key[1:]).lower()
	            if 'harmonic' in mode:
	                mode = 'harmonic'
	            return key_dictionary[mode][letter]
	        except Exception:
	            raise ValueError("{} is not a valid string format for a key".format(key))
	    else:
	        raise ValueError("{} is not a valid key".format(key))

So if you keyify a Key, you just keep the key. If you keyify a subclass of Key, you get a instance of that subclass. More commonly, if you keyify a string, the string is used to look up the relevant key object. The function is not case sensitive, but it requires strings be of the format "`letter mode`". Letter must be a valid letter (e.g. `a`, `cs` or `ef`) while mode should be either `major`, `minor` or `harmonic` (strictly speaking 'harmonic minor' and 'minor harmonic' will work too).

Changing keys, printing key signatures
------------------------------------------

To change a piece's key you need to change it's `key` property, and it should contain an instance of the relevant key. Once this is done, functions like `self.scale` will produce scales in the newly adopted key. Given the above, one way to change a key is the following:

::

	self.key = keys.keyify('A Minor')

This will work (assuming you have imported `keys`), however, the `Piece` class offers a slightly tidier function to do this for you:

::

    def set_key(self, key):
        self.key = keyify(key)

So, with this, the following will work too:

::

	self.set_key('A Minor')

Often this is enough to handle brief forays into alternative keys. However, where the key change lasts long enough users may want to indicate this in the sheet music by printing the key key signature too. This is done with the following property of the `Piece` class:

::

    @property
    def key_signature(self):
        return str(self.key)

This returns a text description of the key which can be added to a point, for instabce, as it's prefix like so:

::

	passage = self.scale('c`', 8)

	self.set_key('c minor)')
	passage += self.scale('c`', 8)
	passage[8].prefix = self.key_signature

This will cause the key signature to print to the score and be interpreted by the lilypond compiler as an instruction to print the key signature on the sheet music. There's another way to do this using dedicated markup functions that we'll come to later.

Pieces can also change to relative keys. For instance, when a piece shifts from C Major to G Major, you may prefer to describe this as a shift to the Major 5th. Pieces can do this, with keys specified by roman numerals (upper case indicates a major key, lower case a minor key):

::


    @property
    def V(self):
        return self.relative_major_key(4)

    @property
    def v(self):
        return self.relative_minor_key(4)

LilyLib also introduces the notion of `cis` and `trans` keys. These are ways to switch to a major or minor key conditional on the mode of your current key; cis maintains the current mode, trans alters it. For instance, the cis fifth of C Major is G Major, while the trans fifth is G Minor. The utility of this distinction is quite uncommon, but it allows the user to compose music that is utterly agnostic of the starting key, meaning that the starting key can be changed, say, from E Major to B Minor, and the piece, including all key changes, will automatically adjust. A demo of this is provided with the piece "Mad Rush" later in the documentation. Cis and trans relative keys are denoted by the suffixes `c` and `t`:

::

    @property
    def Vc(self):
        return self.relative_cis_key(4)

    @property
    def Vt(self):
        return self.relative_trans_key(4) 

A demo
---------

We've already seen an example of a key being changed, but the demo `demo_keys.py` provides a fancier, automated one that cycles through all keys in the dictionary, prints their root notes, and adds an annotation with the name of the key:

::

	from piece import Piece
	from keys import key_dictionary
	from points import note
	from markup import annotation


	class AllKeys(Piece):

	    def details(self):
	        self.title = "Root notes in every key"
	        self.key = "cf major"

	    def write_score(self):
	        self.score["treble"] = []
	        self.score["bass"] = []

	        for mode in key_dictionary:
	            for letter in key_dictionary[mode]:
	                self.set_key(key_dictionary[mode][letter])
	                self.score["treble"] += key_signature(self.key, note(self.key.root + "`", 1, markup=self.key.name))
	                self.score["bass"] += key_signature(self.key, note(self.key.root, 1))

	        self.score["treble"][0].prefix = "\\set Staff.printKeyCancellation = ##f " + self.score["treble"][0].prefix
	        self.score["bass"][0].prefix = "\\set Staff.printKeyCancellation = ##f " + self.score["bass"][0].prefix


	if __name__ == "__main__":
	    AllKeys()

.. image:: _static/keys.png
