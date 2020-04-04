from models import Letter, Pitch

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
