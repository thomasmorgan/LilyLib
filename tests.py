from models import Letter, Pitch, Tone

##########################
# Tests for Letter class #
##########################

print("Testing Letter class", end="")

letter = Letter('b')
letter = Letter('ff')
letter = Letter('css')
letter = Letter('a')

print(".", end="")

assert isinstance(letter, Letter)

print(".", end="")

assert letter.letter == 'a'

print(".", end="")

assert str(letter) == 'a'

print(".", end="")

try:
    letter = Letter('fa')
except ValueError:
    pass
else:
    raise ValueError("Error, letter fa created. This should not be possible.")

print(" passed!")

#########################
# Tests for Pitch class #
#########################

print("Testing Pitch class", end="")

pitch = Pitch('')
pitch = Pitch(',')
pitch = Pitch('``')
pitch = Pitch(',,')

print(".", end="")

assert isinstance(pitch, Pitch)

print(".", end="")

assert pitch.pitch == ',,'

print(".", end="")

assert str(pitch) == ',,'

print(".", end="")

try:
    pitch = Pitch(',`')
except ValueError:
    pass
else:
    raise ValueError("Error, letter ,` created. This should not be possible.")

print(" passed!")

########################
# Tests for Tone class #
########################

print("Testing Tone class", end="")

tone = Tone('a')
tone = Tone('fs,')
tone = Tone('dss``')
tone = Tone('ef,,')

print(".", end="")

assert isinstance(tone, Tone)
assert str(tone) == 'ef,,'

print(".", end="")

assert isinstance(tone.letter, Letter)
assert tone.letter.letter == 'ef'
assert str(tone.letter) == 'ef'

print(".", end="")

assert isinstance(tone.pitch, Pitch)
assert tone.pitch.pitch == ",,"
assert str(tone.pitch) == ',,'

print(".", end="")

try:
    tone = Tone(',,')
except ValueError:
    pass
else:
    raise ValueError("Error, tone ,, created. This should not be possible.")

print(" passed!")
