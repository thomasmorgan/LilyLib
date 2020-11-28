API
=======

Lilylib's code is organized into the following files, (roughly) ordered according to their co-dependencies:

- **util.py**; generic helper functions to flatten and splice lists etc.
- **keys.py**; the Key class, key subclasses, key dictionary and keyify function.
- **staves.py**; the Stave class and subclasses.
- **tones.py**; definition and manipulation of tones, the tonify function.
- **points.py**; the Point class, permitted point durations, functions for generating, transposing and harmonizing points.
- **markup.py**; functions for adding markup to passages of music.
- **piece.py**; the Piece class.

util
---------

**flatten** (*List*)
	Returns a new, un-nested list with the same contents as the passed (nested) list.

**split_and_flatten** (*item*)
	Splits any strings within the passed item at white space, flattens the result and returns it.

**select** (*List, \*indexes*)
	Returns a list containing the subset of items in the passed list whose indexes are also passed. Counts from 1, not 0. Respects ordering of passed list, not passed indexes. Items are not duplicated even if passed indexes contains duplicates.


**pattern** (*List, \*indexes*)
	Builds and returns a new list by repeatedly selecting the items in the passed List at the passed indexes. Counts from 1 not 0. Ordering is determined by the passed indexes not the passed List. Duplicate indexes result in duplicate items in the returned list.


**omit** (*List, \*indexes*)
	Returns a list containing the subset of items in the passed list whose indexes are **not** in the passed indexes. Counts from 1, not 0. Inverse of *select*.


**subset** (*List, start, stop*)
	Returns subset of List from start to stop. Both indexes are inclusive. If stop < start, order of items is reversed relative to passed List.


**join** (*\*motifs*)
	Returns a dictionary which contains the contents of all passed motifs concatenated. Assumes all passed motifs have the same keys as the first motif.

keys
----------

**Key** ()
	The base Key class.

	**Key.__init__** ()
		Makes the Key class.

	**Key.define** ()
		Raises an error by default, subclasses of Key must overwrite this function to set Key.root, Key.name and Key.letters.

	**Key.confirm_definition** ()
		Checks Key has been correctly defined. See Key.define().

	**Key.root**
		The root letter of the key, e.g. "c" for C Major.

	**Key.name**
		The name of the key, e.g. "c major".

	**Key.letters**
		The letters of the tones of the scale of the key in ascending order (which letter is first does not matter).

	**Key.tones**
		Returns a list of all tones in the scale of the key. It is the subset of tones.all_tones where the tones letter is in Key.letters.

	**Key.all_letters**
		Returns a list of all letters in the key. Includes accidentals (e.g. cs is included with C Major) but no duplicates (e.g. df is not included with C Major). Keys with sharps in their signature include sharps in all_letters, keys with flats in their signature include flats.

	**Key.all_tones**
		Returns a list of all tones in the key, including accidentals but not duplicates. It is produced by taking the subset of tones.all_tones where the letter of the tone is in Key.all_letters.

	**Key.arpeggio_letters**
		Returns a list of the letters of the tones of the arpeggio of the key in ascending order.

	**Key.arpeggio_tones**
		Returns a list of the tones of the argpeggio of the key. It is created by taking the subset of tones.all_tones where the tones letter is in Key.arpeggio_letters.

	**Key.arpeggio7_tones**
		Returns a list of the tones of the argpeggio of the key, with the 7th included too.

	**Key.dominant7_tones**
		Returns a list of the tones of the dominant 7th of the key.

	**Key.diminished7_tones**
		Returns a list of the tones of the diminished 7th of the key.

	**Key.scale_subset** (*positions*)
		Returns a list of all tones from the specified positions of the key of the scale. e.g. Key.scale_subset(1, 3, 5) returns the argpeggio_tones.

	**Key.descending_chromatic_letters**
		Returns a list of the letters with all accidentals being flats, not sharps.

	**Key.ascending_chromatic_letters**
		Returns a list of the letters with all accidentals being sharps, not flats.

	**Key.descending_chromatic_tones**
		Returns a list of tones with all accidentals being flats, not sharps.

	**Key.ascending_chromatic_tones**
		Returns a list of tones with all accidentals being sharps, not flats.

	**Key.bias** ()
		Returns "sharp" if the key signature includes sharps (or an equal number of sharps and flats), otherwise returns "flat". For harmonic minors, the number of sharps does not include the sharpened 7th.

	**Key.__str__** ()
		Returns a lilypond description of the key suitable for typesetting.

	**Key.relative_letter** (*i*)
		Returns the ith letter of the scale of the key. Counts from 0, not 1.

	**Key.relative_chromatic_letter** (*i*)
		Returns the ith letter of the chromatic scale of the key (using Key.all_letters). Counts from 0, not 1.

	**Key.tonic**
	    Return the 1st letter of the scale of the key.

	**Key.supertonic**
	    Return the 2nd letter of the scale of the key.

	**Key.mediant**
	    Return the 3rd letter of the scale of the key.

	**Key.subdominant**
	    Return the 4th letter of the scale of the key.

	**Key.dominant**
	    Return the 5th letter of the scale of the key.

	**Key.submediant**
	    Return the 6th letter of the scale of the key.

	**Key.leading**
	    Return the 7th letter of the scale of the key.

	**Key.subtonic**
	    Return the 7th letter of the scale of the key.

	**Key.i**
	    Return the 1st letter of the scale of the key.

	**Key.ii**
	    Return the 2nd letter of the scale of the key.

	**Key.iii**
	    Return the 3rd letter of the scale of the key.

	**Key.iv**
	    Return the 4th letter of the scale of the key.

	**Key.v**
	    Return the 5th letter of the scale of the key.

	**Key.vi**
	    Return the 6th letter of the scale of the key.

	**Key.vii**
	    Return the 7th letter of the scale of the key.

	**Key.I**
	    Return the 1st letter of the scale of the key.

	**Key.II**
	    Return the 2nd letter of the scale of the key.

	**Key.III**
	    Return the 3rd letter of the scale of the key.

	**Key.IV**
	    Return the 4th letter of the scale of the key.

	**Key.V**
	    Return the 5th letter of the scale of the key.

	**Key.VI**
	    Return the 6th letter of the scale of the key.

	**Key.VII**
	    Return the 7th letter of the scale of the key.

**CFlatMajor**
	The Key subclass for C-flat Major.

**CFlatMinor**
	The Key subclass for C-flat Minor.

**CFlatMinorH**
	The Key subclass for C-flat Minor harmonic.

\.\.\. *see keys.py for all key subclasses* \.\.\.

**key_dictionary** [*mode*][*root*]
	A dicitonary containing all key subclasses, keyed by mode and root, e.g. key_dictionary["minor"]["bf"] returns an instance of the BFMinor key subclass.

**keyify** (*key*)
	Converts the passed key to an instance of a Key subclass. The argument should either be a subclass of Key or a string. Where a string, it should be of the form "<root> <mode>", although capitalization does not matter. e.g. "c major", "af minor", or "g harmonic".

staves
------------

**Stave** ()
	The parent staff class.

	**Stave.__init__** (*clef, name*)
		Creates a Stave instance. String clef must be a valid lilypond clef, name can be anything.

**Treble** ()
	A subclass of Stave, appears as a staff starting with the treble clef.

	**Treble.__init__** (*name*)
		Creates a treble staff. Name can be anything.

**Bass** ()
	A subclass of Stave, appears as a staff starting with the bass clef.

	**Bass.__init__** (*name*)
		Creates a bass staff. Name can be anything.

**Super** ()
	A subclass of Stave, appears as a staff starting with the treble clef, but has rows for both the treble and bass staves. See demo_prelude_in_c_super.py for an example.

	**Super.__init__** (*name*)
		Creates a super staff. Name can be anything.

tones
----------

**all_base_letters**
	A list containing all permitted base letters (i.e. a through g).

**all_accents**
	A list containing all permitted accents (i.e. ff, f, , s, ss)

**all_letters**
	An ordered list containing all possible combinations of *all_base_letters* and *all_accents*.

**all_pitches**
	A list contianing all permitted pitches (i.e. ,,, ,, ,  ` `` \`\`\`)

**all_tones**
	An ordered list containing all possible combination of *all_letters* and *all_pitches*.

**equivalent_letters**
	A dictionary with a value for each letter corresponding to the alternative letter. Does not support double flats or accidentals. e.g. *equivalent_letters['cs']* returns df.

**equivalent_tone** (*tone*)
	Returns a tone with the same pitch as, and an equivalent letter to, the passed tone. e.g. *equivalent_tone(fs,,)* returns gf,,.

**separate** (*tone*)
	Splits a tone into a letter and pitch, returns them as a tuple.

**letter** (*tone*)
	Returns the letter of a tone, e.g. fs.

**pitch** (*tone*)
	Retuns the pitch of a tone, e.g. \`\`.

**base_letter** (*tone*)
	Returns the base letter of a tone (i.e. with any accents removed).

**accent** (*tone*)
	Returns the accent of a tone.

**flatten** (*tone*)
	Returns a new tone, one semitone below the passed tone. e.g. *flatten(c)* returns cf. With return an illegal triple-flat if you flatten a double-flat.

**sharpen** (*tone*)
	Returns a new tone, one semitone above the passed tone. e.g. *sharpen(c)* returns cs. With return an illegal triple-sharp if you flatten a double-sharp.

**tonify** (*tones*)
	Converts passed tones to an unflattened list of valid tones and empty lists and returns it. Multi-tone strings (separated by whitespce) are split into lists of tones. If any (sub)strings do not correspond to valid tone an error is raised. A seris of N spaces is converted into a seris of N-1 empty lists. If empty lists are used to create a Point, a toneless Point (i.e. a rest) will be produced, but the empty lsits will be erased if the list is flattened (util.flatten). For instance, *tonify('a  c')* returns ['a', [], 'c'].
