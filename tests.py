from models import Letter, Pitch

print("Testing Letter class", end="")

letter = Letter('a')
assert isinstance(letter, Letter)
assert letter.letter == 'a'

print(".", end="")

letter = Letter('b')
letter = Letter('ff')
letter = Letter('css')

print(".", end="")

try:
    letter = Letter('fa')
except ValueError:
    pass
else:
    raise ValueError("Error, letter fa created. This should not be possible.")

print(" passed!")

print("Testing Pitch class", end="")

pitch = Pitch(',,')
assert isinstance(pitch, Pitch)
assert pitch.pitch == ',,'

print(".", end="")

pitch = Pitch('')
pitch = Pitch(',')
pitch = Pitch('``')

print(".", end="")

try:
    pitch = Pitch(',`')
except ValueError:
    pass
else:
    raise ValueError("Error, letter ,` created. This should not be possible.")

print(" passed!")
