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
