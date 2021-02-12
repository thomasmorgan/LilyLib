Prelude in C
===============

This and the next chapter go through a couple of demo pieces to show LilyLib in action. First we'll start with Bach's Prelude in C. There's actually four different versions of this demo, of increasing complexity, and we'll go through them in order.

Simple
---------

The most basic demo is in *demo_prelude_in_c_simple.py*. As the name suggests this is quite simple. The main thing is to realize that the piece is constructed around an 8 note motif that progresses through different chords. So, for some basic refactoring, this demo first creates a function that produces this motif:

::

    def motif(self, c):
        tones = tonify(c)
        return {
            'treble': rep(rest(8) + notes(pattern(tones, 2 * [3, 4, 5]), 16), 2),
            'bass': rep(voices(rest(16) + tied_note(select(tones, 2), ['8.', 4]), note(select(tones, 1), 2)), 2)
        }

This function gets passed a five note chord (*c*) and then it adds the first two notes to the bass clef, and adds the 3rd, 4th and 5th to the treble (twice). The treble clef if semiquavers, preceded by a quaver rest. The bass clef has two voices because the notes are held. Both parts are doubled, because the motif is repeated twice for each chord.

After this the piece lists the different chords to be applied to the motif:

::

    @property
    def chords(self):
        bar = [''] * 40

        bar[1] = 'c` e` g` c`` e``'
        bar[2] = 'c` d` g` c`` e``'
        bar[3] = 'b d` g` d`` f``'
        bar[4] = 'c` e` g` c`` e``'

        bar[5] = 'c` e` a` e`` a``'
        bar[6] = 'c` d` df` a` d``'
        bar[7] = 'b d` g` d`` g``'
        bar[8] = 'b c` e` g` c``'

These are simple strings, put in a list called *bar*. We start counting from 1, and because the motif is one bar long this means that *bar[x]* contains the chord played in the xth bar of the piece.

We then iterate through the chords, applying the motif function as we go:

::

    def write_score(self):
        self.score = join([self.motif(chord) for chord in self.chords[1:33]])

The end of the piece actually does something a bit different, so we need a bit more code:

::

    def held_bass(self, tones):
        tones = tonify(tones)
        return voices(rest(16) + tied_note(tones[1], ['8.', 4, 2]), note(tones[0], 1))

    def long_melody(self, tones):
        tones = tonify(tones)
        return rest(8) + notes(pattern(tones, 1, 2, 3, 4, 3, 2, 3, 2, 1, 2), 16)

    @property
    def outro(self):
        return {
            'treble': self.long_melody('f a c` f`') + notes('f d', 16) * 2 + self.long_melody('g` b` d`` f``') + pattern(self.scale('d`', 'f`', 16), 1, 3, 2, 1) + chord('e` g` c`', 1),
            'bass': self.held_bass('c, c') + self.held_bass('c, b,') + chord('c, c', 1)
        }

    def write_score(self):
        self.score = join([self.motif(chord) for chord in self.chords[1:33]])
        self.score = join(self.score, self.outro)

But with that complete the piece is ready to print:

.. image:: _static/prelude_in_c_simple.png

Intermediate
----------------

The simple demo works fine, but listing out the chords note-for-note means we don't make any attempt to understand what the piece is doing, we also don't use any of the LilyLib functions like *arpeggio*. That's where we go next in *demo_prelude_in_c.py*. Rather than list the notes in each chord, we describe what each chord *is*:

::

    @property
    def chords(self):
        bar = [''] * 40

        bar[1] = self.arpeggio('c`', 'e``')
        bar[2] = omit(arpeggio7('c`', 'f``', 'D Minor'), 3, 5)
        bar[3] = omit(dominant7('b', 'f``', 'G Major'), 3, 5)
        bar[4] = deepcopy(bar[1])

        bar[5] = omit(arpeggio('c`', 'a``', 'A Minor'), 4)
        bar[6] = ['c`'] + arpeggio('d`', 'd``', 'D Major')
        bar[7] = self.transpose(bar[5], -1)
        bar[8] = ['b'] + self.arpeggio('c`', 'c``')

Now whether this is more readable or not is debateable. But it is undoubtedly more explicit about the harmonic changes going on, and the structure of the chords. So the opening bar is an arpeggio in the root chord, then it moves to D Minor (which could also have been referenced as *self.II*), G Major (or *self.V*), before coming back to C Major. Note that we can take advantage of the fact that bar 4 is the same as bar 1 to explicitly make them copies of each other. Applying this to the whole piece takes a little while, but once it's done you get the same nice sheet music.

Note the neat trick here: inheritance. Because this is the same as the simple version, but with the chords defined differently, we can inherit everything else from the simpler version. This is done by having the new piece extend the simple version:

::

    from demos.demo_prelude_in_c_simple import PreludeInCSimple


    class PreludeInC(PreludeInCSimple):

We'll do this a couple more times now.

Advanced
------------

LilyLib let's you manipulate music in helpful ways. Let's look at two specific examples in *demo_prelude_in_c_fancy.py*. First, imagine that you know Prelude in C well enough to not need to see the motif. What you really want is just a list of the chords. Second, let's imagine you want to see the name of the chords on the sheet music too, just to remind you what's going on harmonically. The motif function generates the motifs, and we can modify it to do both of these things. First, let's provide a list of the chord names:

::

    def chord_names(self):
        return ['',
                'I', 'ii D7', 'V D7', 'I',
                'vi', 'II D7', 'V', 'I7',
                'vi7', 'II D7', 'V', 'V d7',
                'ii', 'ii d7', 'I', 'IV7',
                'ii7', 'V D7', 'I', 'I D7',
                'IV7', 'VI d7', 'IV ?', 'V D7',
                'I', 'V 4/7', 'V D7', 'V/VI d7',
                'I', 'V 4/7', 'V D7', 'I D7']

Now, let's have the motif function accept both the chord and the name, and then (1) create either a motif or a single chord according to the *summary* property, and (2) and a text label, or not, according to the *annotate* property:

::

    def write_score(self):
        self.score = join([self.motif(chord, name) for chord, name in zip(self.chords[1:33], self.chord_names[1:33])])
        self.score = join(self.score, self.outro)

    def motif(self, c, n):
        summary = True
        annotate = True
        if summary:
            tones = tonify(c)
            passage = {
                'treble': chord(subset(tones, 3, 5), 4),
                'bass': chord(subset(tones, 1, 2), 4)
            }
        else:
            passage = super().motif(c)

        if annotate:
            passage['treble'][0].markup = n

        return passage

The last thing we do is append a bit of lilypond to reduce the horizontal spacing for visual pleasure:

::

    def end_score(self):
        return ('>>\n  \\layout {\n \\context {\n \\Score\n \\override SpacingSpanner.common-shortest-duration =\n #(ly:make-moment 1/16)\n }\n }\n }')

That's it! Here's the sheet music that prints when both properties are set to *True*:

.. image:: _static/prelude_in_c_fancy.png

For someone who is comfortable with this piece, the sheet music in this format is perfectly easy to read, but also more informative than the regular sheet music. Critically it takes just a few minutes to modify the basic LilyLib code to produce this format, and note we're still using inheritance to avoid repeating code shared with other pieces.

Experimental
---------------

Piano music is typically written across two staves. Often these correspond to the two hands, but this is often not the case too. Even when it is the case, the separation of the hands in this way can mask the unity of what the hands are doing. This is the case in Prelude in C: The two hands are actually playing a single voice (let's ignore that the music is actually a little polyphonic). To better convey this I have been experimenting with a single combined staff. It resembles the traditional treble and bass staves, but the gap between them is "anatomically correct" and the music freely flows across them. This is baked into LilyLib, here's how to implement it:

First, in the details, set the staves to a single *Super* staff:

::

    def details(self):
        self.title = "Prelude in C"
        self.staves = [Super()]

Next, modify the motif function to print both hands as separate voices on the same staff (treating the hands as separate voices keeps the stems of the two hands separate):

::

    def motif(self, c):
        passage = super().motif(c)
        new_passage = {
            'treble': voices(passage['treble'], notes(tonify(c)[0:2], 16) + rests(8, 4))
        }
        new_passage['treble'][0].prefix += ' \\override Rest.transparent = ##t '
        new_passage['treble'][14].prefix += ' \\override Rest.transparent = ##t '
        new_passage['treble'][14].ornamentation = 'laissezVibrer'
        new_passage['treble'][15].ornamentation = 'laissezVibrer'
        return new_passage

All the stuff about rest transparency is to make rests invisible, this is to avoid cluttering the music given that there are two voices on the same staff. I also use *laissez vibrer* marks on the left hand, rather than multiple notes with ties. That's basically it (there are some modifications to the outro too), and here's what the music looks like:

.. image:: _static/prelude_in_c_super.png

Maybe you like this (I do), maybe you hate it. The point is not that this is a good way to write music, the point is that LilyLib let's you quickly rewrite music in multiple different ways with just a few tweaks to different functions.
