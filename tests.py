from models import Letter

print("Testing Letter class...", end="")

letter = Letter('a')
assert isinstance(letter, Letter)
assert letter.letter == 'a'

letter = Letter('b')
letter = Letter('ff')
letter = Letter('css')

try:
    letter = Letter('fa')
except ValueError:
    pass
else:
    raise ValueError("Error, letter fa created. This should not be possible.")

print(" passed!")
