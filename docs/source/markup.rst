Markup
==========

As we've covered, LilyLib writes music as a list of *Points*, a class of object introduced by LilyLib that correspond to notes, chords and rests. These points can be given values for a range of properties that modify how they print, and collectively we call this markup. This includes things like ornamentation, phrasing and so on, and these proprties of points can be edited at any time or assigned by the *note*, *rest* and *chord* functions. However, markup can do more than this, and, in particular, there are some forms of markup that don't apply to a single note, but rather apply to a passage of multiple notes. An example might be the use of triplets. In these cases the markup requires that multiple points be edited, typically to denote the start and stop points of the markup and LilyLib includes a number of functions to do exactly this. We've seen one example of this already with the *key_signature* function from the key changing demo:

::

    self.score["bass"] += key_signature(self.key, note(self.key.root, 1))

Here we are applying the key change to a single note, but if we look at the underlying function (in *markup.py*) we can see it can be applied to a passage of any length:

::

    def key_signature(key1, passage, key2=""):
        passage = deepcopy(passage)
        passage = flatten([passage])
        passage[0].prefix = str(keyify(key1)) + passage[0].prefix
        if key2:
            passage[-1].suffix += str(keyify(key2))
        return passage

Here the function is given a key signature and a passage and it modifies the *prefix* of the first point to include a key change. If you want the key signature to change again at the end of the passage you can pass another key signature and this is added to the *suffix* of the final point. Note that the function also makes a deepcopy of the passage. This means that marking up a passage returns an new version of the passage with the markup, but the original passage is unchanged. This is because passages are often repeated, but with different markup, and so its useful to apply markup to one instance, but not the others. This behavior is common to all markup functions.

Here's another example, the *triplets* function:

::

    def triplets(passage):
        passage = deepcopy(passage)
        passage = flatten([passage])
        passage[0].prefix = '\\tuplet 3/2 {' + passage[0].prefix
        passage[-1].suffix += '}'
        return passage

Here both the first and final point must be modified because lilypond requires that the start and stop of triplets be explicitly defined.

As one last example, here's the voices function:

::

    def voices(*voices):
        voices = [deepcopy(voice) for voice in voices]
        for i, voice in enumerate(voices):
            voice = flatten(voice)
            voice[0].prefix = "{ " + voice[0].prefix
            voice[-1].suffix += " }"
            if i < (len(voices) - 1):
                voice[-1].suffix += "\n\\\\\n"
        flatten(voices[0])[0].prefix = "\n<<\n" + flatten(voices[0])[0].prefix
        flatten(voices[-1])[-1].suffix += "\n>>\n"
        passage = []
        for voice in voices:
            passage += voice
        return passage

This function accepts a list of multiple passages and applies markup to them such that they print as multiple simultaneous voices. First each voice is bookended by curcly brackets to denote the start and stop of each voice. Then the final point of all but the last voice have slashes appeneded to their suffix to indicate the change from one voice to another. Finally, the first note of the first voice, and the last note of the last voice have chevrons added to indicate the beginning and end of the voiced section. These voices are then joined to form a single long list of points and returned.

Note that, as per lilypond convention, voices should be passed in the following order: highest, lowest, 2nd highest, 2nd lowest, 3rd highest, and so on. Also, note than when counting points in order to seelct or modify a specific point (e.g. *passage[12]*), for voices you need to count through each voice, in order, one after another.

The markup file also includes many other functions for things like clef changes, repeat bars, ottava markings, and so on. For a full list see the API doc file.
