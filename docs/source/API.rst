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

**rep** (*passage, n*)
	Makes *n* deepcopies of the passed passage, joins them into a single list, and returns it.

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

points
------------

**all_durs**
	A list of all permitted Point durations.

**Point**
	The Point class. Notes, chords and rests are all instances of Point.

	**Point.__init__** (*tones, dur, ornamentation=""*)
		The init function for Point. *tones* is a list of tones, if empty you get a rest. *dur* is the duration of the Point. Ornamentation is optional and should conform to lilypond.

	**Point.check_init_arguments** (*tones, dur, ornamentation*)
		Internal function that validates the arguments passed to Point.\_\_init\_\_.

	**Point.__str__** ()
		Returns a liylpond string representation of the Point, including all forms of markup.

	**Point.tone**
		If the Point has a single tone, returns the tone, otherwise raises an error.

	**Point.letter**
		If the Point has a single tone, returns its letter, otherwise raises an error.

	**Point.pitch**
		If the Point has a single tone, returns its pitch, otherwise raises an error.

	**Point.is_rest**
		Returns true if the Point's tone list is empty, otherwise false.

	**Point.is_note**
		Returns true if the Point's tone has length 1, otherwise false.

	**Point.is_chord**
		Returns true if the Point's tone list has multiple tones, otherwise false.

	**Point.add** (*tones*)
		Adds the passed tones to the Point, if any tones are already present nothing happens.

	**Point.remove** (*tones*)
		Removes the passed tones from the Point if present.

	**Point.replace** (*old_tones, new_tones*)
		Removes the old_tones from the point and adds the new_tones in their place. The two arguments are flattened and zipped and iterated through together. If one is longer than the other, the shorter argument is cycled to reach the length of the longer.

**rest** (*dur, phrasing="", articulation="", ornamentation="", dynamics="", markup="", markdown="", prefix="", suffix=""*)
	Returns a list containing a single rest (i.e. a toneless Point) of the specified duration with the specified markup.

**rests** (*\*dur*)
	Returns a list of rests (i.e. toneless Points) with the specified durations.

**note** (*tone, dur, phrasing="", articulation="", ornamentation="", dynamics="", markup="", markdown="", prefix="", suffix=""*)
	Returns a list containing a single note (i.e. a Point with one tone) with the specified tone, dur and markup.

**notes** (*tones, dur, ornamentation*):
	Returns a list of notes (i.e. Points with a single tone). The arguments are flattened, zipped and iterated to produce the notes. The longest argument determines the number of notes created, the other arguments are cycled to reach the same length.

**chord** (*tones, dur, phrasing="", articulation="", ornamentation="", dynamics="", markup="", markdown="", prefix="", suffix=""*)
	Returns a list containing a single chord (i.e. a Point with multiple tones) with the specified tones, duration and markup.

**chords** (*tones, dur, ornamentation*)
	Returns a list of multiple chords (i.e. Points with multiple tones). The dur and ornamentation arguments are flattened, but *tones* is not and it must be a list of lists of tones. The arguments are then zipped and iterated to produce the chords. The longest argument determines the number of chords created, the other arguments are cycled to reach the same length.

**tied_note** (*tone, durs*)
	Returns a list of multiple Points all with the same tone, but different durations as specified and with phrasing set to "~" such that they print as a single tied note.

**tied_chord** (*tones, durs*)
	Returns a list of multiple Points all with the same tones, but different durations as specified and with phrasing set to "~" such that they print as a single tied chord.

**add** (*points, tones, \*tweaks*)
	Adds the passed tones to the passed points, if any tones are already present in a given point nothing happens. By default, rests (i.e. empty points) are skipped, pass "include rests" as an extra argument to edit rests too.

**remove** (*points, tones*)
	Removes the passed tones from the passed points if present. Removing enough tones will convert chords to notes and notes to rests.

**replace** (*points, old_tones, new_tones*)
	Removes the old_tones from the points and adds the new_tones in their place. The arguments old_tones and new_tones are flattened and zipped and iterated through together. If one is longer than the other, the shorter argument is cycled to reach the length of the longer.

**series** (*tones, start, stop_or_length, dur=None, step=1*)
	Internal function used by scale, argpeggio etc. Returns a list of tones (or Points if dur is specified), selected from the passed tones, with start and stop points, and step size, corresponding to the passed arguments. The dur argument can be a list which cycles through the passed values.

**validate_series_args** (*tones, start, stop_or_length, dur, step*)
	Internal function that validates args passed to the series function.

**scale** (*start, stop_or_length, key, dur=None, step=1*)
	Returns a scale from *start* to *stop* or of length *length* in the key of *key* with stepsize *step*.


**arpeggio** (*start, stop_or_length, key, dur=None, step=1*)
	Returns an arpeggio from *start* to *stop* or of length *length* in the key of *key* with stepsize *step*.


**arpeggio7** (*start, stop_or_length, key, dur=None, step=1*)
	Returns an arpeggio (including the 7th) from *start* to *stop* or of length *length* in the key of *key* with stepsize *step*.


**dominant7** (*start, stop_or_length, key, dur=None, step=1*)
	Returns a dominant 7th from *start* to *stop* or of length *length* in the key of *key* with stepsize *step*.


**diminished7** (*start, stop_or_length, key, dur=None, step=1*)
	Returns a diminished 7th from *start* to *stop* or of length *length* in the key of *key* with stepsize *step*.


**chromatic** (*start, stop_or_length, key, dur=None, step=1*)
	Returns a chromatic scale from *start* to *stop* or of length *length* in the key of *key* with stepsize *step*. Ascending chromatic scales use sharps, descending scales use flats.


**scale_subset** (*positions, start, stop_or_length, key, dur=None, step=1*)
	Returns a subset of a scale from *start* to *stop* or of length *length* in the key of *key* with stepsize *step*. The *positions* argument indicates which notes are included and is indexed from 1. So [1, 3, 5] returns arpeggios and [1, 2, 3, 4, 5, 6, 7] returns full scales.

**transpose** (*item, shift, key, mode="scale"*)
	Returns a transposed version of the passed item or passage. The shift is the size of the transposition. Key is the key in which the transposition occurs. Mode indicates the kind of transposition; "scale", "octave" or "semitone".

**validate_transpose_args** (*shift, mode*)
	Internal function that validates arguments for *transpose*.

**merge** (*\*passages*)
	Takes multiple passages of music and blends them into a single passage which is returned. Passages are zipped together and the interated through, the tones of each point in each passage are added to a single point in the new passage.

**harmonize** (*points, interval, key, mode="scale"*)
	Harmonizes a passage my transposing it the indicated interval and then merging the result with the passed passage.

markup
-----------

**linebreak**
	A string that causes a linebreak both in the sheetmusic and in the terminal output, can be added to Points, usually as part of their suffix.

**pagebreak**
	A string that causes a pagebreak in the sheetmusic and a linebreak in the terminal output, can be added to Points, usually as part of their suffix.


**clef** (*clef, passage, end_clef=""*)
	Returns a flattened deepcopy of the *passage* with the *clef* added to the prefix of the first point and the optional *end_clef* added to the suffix of the final point.

**time_signature** (*tempo, passage, end_tempo=""*)
	Returns a flattened deepcopy of the *passage* with the *tempo* added to the prefix of the first point and the optional *end_tempo* added to the suffix of the final point.

**key_signature** (*key1, passage, key2=""*)
	Returns a flattened deepcopy of the *passage* with *key1* added to the prefix of the first point and the optional *key2* added to the suffix of the final point.

**triplets** (*passage*)
	Returns a deepcopy of the passage passage, with the first prefix and final suffix edited such that it appears as triplets.


**grace** (*passage*)
	Returns a deepcopy of the passage, with the first prefix and final suffix edited such that it appears as grace notes.


**after_grace** (*passage, grace*)
	Returns a deepcopy of the passage and grace combined into a single list (passage then grace) with the first prefix and final suffix of both parts edited such that the grace appears as grace notes following the passage.


**acciaccatura** (*passage*)
	Returns a deep copy of the passage, with the first prefix and final suffix edited such that it appears as acciaccatura.


**ottava** (*passage, shift*)
	Returns a deepcopy of the passage, with the first prefix and final suffix edited such that it is marked with ottava. Shift indicates the magnitude of the ottava, negative numbers shift down.


**voices** (*\*voices*)
	Returns a single passage with markup such that the voices are played on top of each other. Voices should be ordered as highest, lowest, 2nd highest, 2nd lowest, and so on. The first prefix and final suffix or each voice are modified to do this.


**repeat** (*passage, times=2*)
	Returns a deepcopy of the passage with the first prefix and final suffix edited such that repeat bars are printed around it. If the number of repeats is greater than two, the number is indicated above the closing bracket.

piece
---------

**Piece** ()
	The base Piece class.

	**Piece.__init__** ()
		Piece init function. Sets default values, calls *details* to overwrite them, then prints itself to the terminal.
		
	**Piece.details** ()
		Must be overwritten by subclasses, allows configuration of piece deatils like title, composer, etc.

	**Piece.set_key** (*key*)
		Sets the pieces key to the passed value. *key* can be a string, a subclass of *Key* or an instance of a *Key*.

	**Piece.key_signature**
		Returns lilypond formatted string of the pieces current key, will print as a key signature in sheet music when added to a point.

	**Piece.write_score** ()
		Called by *Piece.str()*, creates a description of the score of the piece and adds it to the *self.score* dictionary.

	**Piece.__str__** ()
		Prints a lilypond description of the piece. It concatenates the results of the Pieces *header*, *subtext*, *start_score*, *write_score* and *end_score* functions.

	**Piece.header** ()
		Returns a string containing the metadata of the piece in lilypond format.

	**Piece.subtext** ()
		By default returns an empty string. Can be overwritten to add text between the header and score of a piece. Useful for starting sheetmusic with extended bodies of text.

	**Piece.start_score** ()
		Returns Lilypond string to open the score.

	**Piece.end_score** ()
		Returns Lilypond string to close the score

	**Piece.print_stave** (*stave*)
		Returns a lilypond formatted string description of the contents of the passed stave.

	**Piece.scale** (*start, stop_or_length, dur=None, step=1*)
		Returns a list of Points forming a scale by passing all arguments and the piece's current key to points.scale().

	**Piece.arpeggio** (*start, stop_or_length, dur=None, step=1*)
		Returns a list of Points forming an argpeggio by passing all arguments and the piece's current key to points.arpeggio().

	**Piece.arpeggio7** (*start, stop_or_length, dur=None, step=1*)
		Returns a list of Points forming an argpeggio7 by passing all arguments and the piece's current key to points.arpeggio7().

	**Piece.dominant7** (*start, stop_or_length, dur=None, step=1*)
		Returns a list of Points forming a dominant 7th by passing all arguments and the piece's current key to points.dominant7().

	**Piece.diminished7** (*start, stop_or_length, dur=None, step=1*)
		Returns a list of Points forming a diminished 7th by passing all arguments and the piece's current key to points.diminished7().

	**Piece.chromatic** (*start, stop_or_length, dur=None, step=1*)
		Returns a list of Points forming a chromatic scale by passing all arguments and the piece's current key to points.chromatic().

	**Piece.scale_subset** (*positions, start, stop_or_length, dur=None, step=1*)
		Returns a subset of a scale by passing all arguments and the piece's current key to points.scale_subset. The *positions* argument indicates which notes are included and is indexed from 1. So [1, 3, 5] returns arpeggios and [1, 2, 3, 4, 5, 6, 7] returns full scales.

	**Piece.transpose** (*item, shift, mode="scale"*)
		Returns a transposed version of the passed item or passage, by passing all arguments and the piece's current key to points.transpose.

	**Piece.harmonize** (*points, intervals, mode="scale"*)
		Returns a harmonized version of the passed points, by passing all arguments and the piece's current key to points.harmonize.

	**Piece.relative_key** (*mode, relationship*)
		Returns a key relative to the piece's current key. Mode is "major", "minor" or "harmonic". Relationship is the numeric distance between the current key and relative key. So if the current key is C Major (or minor), relative_key("minor", 2) returns E Minor.

	**Piece.relative_major_key** (*relationship*)
		Returns the relative major key of the piece's current key by passing relationship and "major" to Piece.relative_key.

	**Piece.relative_minor_key** (*relationship*)
		Returns the relative minor key of the piece's current key by passing relationship and "minor" to Piece.relative_key.

	**Piece.relative_harmonic_key** (*relationship*)
		Returns the relative harmonic key of the piece's current key by passing relationship and "harmonic" to Piece.relative_key.

	**Piece.relative_cis_key** (*relationship*)
		Passes relationship to Piece.relative_key to generate a relative key. Mode is specified according to the current key; if the current key is major, then "major" is passed, otherwise "minor" is passed (note "harmonic" is never passed).

	**Piece.relative_trans_key** (*relationship*)
		Passes relationship to Piece.relative_key to generate a relative key. Mode is specified according to the current key; if the current key is major, then "minor" is passed, otherwise "major" is passed (note "harmonic" is never passed).

	**Piece.I**
		Returns the relative_major_key with position 0.

	**Piece.II**
		Returns the relative_major_key with position 1.

	**Piece.III**
		Returns the relative_major_key with position 2.

	**Piece.IV**
		Returns the relative_major_key with position 3.

	**Piece.V**
		Returns the relative_major_key with position 4.

	**Piece.VI**
		Returns the relative_major_key with position 5.

	**Piece.VII**
		Returns the relative_major_key with position 6.

	**Piece.i**
		Returns the relative_minor_key with position 0.

	**Piece.i**
		Returns the relative_minor_key with position 1.

	**Piece.i**
		Returns the relative_minor_key with position 2.

	**Piece.i**
		Returns the relative_minor_key with position 3.

	**Piece.v**
		Returns the relative_minor_key with position 4.

	**Piece.v**
		Returns the relative_minor_key with position 5.

	**Piece.v**
		Returns the relative_minor_key with position 6.

	**Piece.ih**
		Returns the relative_harmonic_key with position 0.

	**Piece.ii**
		Returns the relative_harmonic_key with position 1.

	**Piece.ii**
		Returns the relative_harmonic_key with position 2.

	**Piece.iv**
		Returns the relative_harmonic_key with position 3.

	**Piece.vh**
		Returns the relative_harmonic_key with position 4.

	**Piece.vi**
		Returns the relative_harmonic_key with position 5.

	**Piece.vi**
		Returns the relative_harmonic_key with position 6.

	**Piece.Ic**
		Returns the relative_cis_key with position 0.

	**Piece.IIc**
		Returns the relative_cis_key with position 1.

	**Piece.IIIc**
		Returns the relative_cis_key with position 2.

	**Piece.IVc**
		Returns the relative_cis_key with position 3.

	**Piece.Vc**
		Returns the relative_cis_key with position 4.

	**Piece.VIc**
		Returns the relative_cis_key with position 5.

	**Piece.VIIc**
		Returns the relative_cis_key with position 6.

	**Piece.It**
		Returns the relative_trans_key with position 0.

	**Piece.IIt**
		Returns the relative_trans_key with position 1.

	**Piece.IIIt**
		Returns the relative_trans_key with position 2.

	**Piece.IVt**
		Returns the relative_trans_key with position 3.

	**Piece.Vt**
		Returns the relative_trans_key with position 4.

	**Piece.VIt**
		Returns the relative_trans_key with position 5.

	**Piece.VIIt**
		Returns the relative_trans_key with position 6.

