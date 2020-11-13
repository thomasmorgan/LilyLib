# LilyLib

A python library that provides a mid-level language for writing sheet music. Lilylib let's you write music in terms of scales, arpeggios, key changes, motifs, transpositions, and so on. It can be compiled into Lilypond which can then be compiled into a pdf.

# tl;dr

Starting with this bit of spoken language:

> “Starting from the E above middle C, and in E Major. First the right hand plays an ascending 1 octave scale while the left hand plays a descending 1 octave arpeggio. Then the right hand plays a descending one octave dominant 7th, while the left hand plays a dominant 7th chord. Finally, both hands play a major chord.”

You can write this bit of lilylib:

```python
from piece import Piece
from points import chord


class TLDR(Piece):

    def details(self):
        self.title = "tl;dr demo"
        self.key = 'E Major'

    def write_score(self):
        self.score["treble"] = self.scale('e`', 8, 8) + self.dominant7('d``', -4, 4) + chord(self.arpeggio('e`', 4), 1)
        self.score["bass"] = self.arpeggio('e`', -4, 4) + chord(self.dominant7('e', 5), 1) + chord(self.arpeggio('e,', 4), 1)
```

Executing this in the terminal prints out the following lilypond:

```

\version "2.18.2"
\language "english"
\header {
    title = "tl;dr demo"
    subtitle = ""
    composer = ""
    mutopiacomposer = ""
    mutopiainstrument = "piano"
    source = ""
    style = "Romatic"
    license = "Creative Commons Attribution-ShareAlike 4.0"
    maintainer = "Anonymous"
    opus = ""
}
\score { <<
<< \new Staff {
\clef treble
\key e \major
\time 4/4
e'8 fs'8 gs'8 a'8 b'8 cs''8 ds''8 e''8 d''4 b'4 gs'4 e'4 <e' gs' b' e''>1} >>
<< \new Staff {
\clef bass
\key e \major
\time 4/4
e'4 b4 gs4 e4 <e gs b d' e'>1 <e, gs, b, e>1} >>
>> }

```

Which compiles into this sheet music:

![tldr demo image](https://raw.githubusercontent.com/thomasmorgan/LilyLib/master/docs/source/_static/tldr.png)


## Authors

- Thomas Morgan


## License

This project is licensed under the MIT License.


## Acknowledgments

Thanks to creators of lilypond, lilylib is basically just a lilypond wrapper and relies on lilypond compilers to produce nice sheet music.
