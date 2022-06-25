import tones
from tones import equivalent_letters, letter

from inspect import isclass


class Key:
    """ A set of Tones represented by a key signature. Needs to be subclassed to be meaningful.
    util.all_tones returns every possible Tone
    Key.all_tones returns all unique tones in the key (i.e. excluding equivalent tones)
    Key.tones returns all Tones in the scale of the key
    Key.arpeggio_tones returns all Tones in the arpeggio of the key. """

    def __init__(self):
        # define must be overwritten in subclasses to:
        # 1. set the root letter
        # 2. set the included letters
        # 3. set the key's name
        self.root = None
        self.letters = None
        self.name = None
        self.define()
        self.confirm_definition()
        self.generate_tones()

    def confirm_definition(self):
        if None in [self.root, self.letters, self.name]:
            raise ValueError("Must define root, letters and name of Key {}".format(self))

    def generate_tones(self):
        self.all_letters = [l for l in self.letters]
        for l in ['c', 'd', 'e', 'f', 'g', 'a', 'b']:
            if l not in self.all_letters and equivalent_letters[l] not in self.all_letters:
                self.all_letters.append(l)

        if self.bias() == "sharp":
            for l in ['cs', 'ds', 'es', 'fs', 'gs', 'as', 'bs']:
                if l not in self.all_letters and equivalent_letters[l] not in self.all_letters:
                    self.all_letters.append(l)
        if self.bias() == "flat":
            for l in ['cf', 'df', 'ef', 'ff', 'gf', 'af', 'bf']:
                if l not in self.all_letters and equivalent_letters[l] not in self.all_letters:
                    self.all_letters.append(l)
        self.all_letters = [l for l in tones.all_letters if l in self.all_letters]

        self.all_tones = [t for t in tones.all_tones if letter(t) in self.all_letters]

        self.tones = [t for t in self.all_tones if letter(t) in self.letters]

        index_of_root = self.letters.index(self.root)
        self.arpeggio_letters = [(self.letters * 2)[i] for i in [index_of_root, index_of_root + 2, index_of_root + 4]]

        self.arpeggio_tones = [t for t in self.all_tones if letter(t) in self.arpeggio_letters]

        self.arpeggio7_tones = self.scale_subset([1, 3, 5, 7])

        if "major" in self.name:
            self.dominant7_letters = self.arpeggio_letters + [tones.flatten(self.VII)]
        elif "harmonic" in self.name:
            self.dominant7_letters = [self.root, tones.sharpen(self.iii), self.V, tones.flatten(self.VII)]
        elif "minor" in self.name:
            self.dominant7_letters = [self.root, tones.sharpen(self.iii), self.V, self.VII]
        else:
            raise ValueError("Cannot provide dominant 7 tones for key {}".format(self.name))

        self.dominant7_tones = [t for t in tones.all_tones if letter(t) in self.dominant7_letters]

        if "major" in self.name:
            self.diminished7_letters = [self.root, tones.flatten(self.III), tones.flatten(self.V), tones.flatten(tones.flatten(self.VII))]
        elif "harmonic" in self.name:
            self.diminished7_letters = [self.root, self.iii, tones.flatten(self.V), tones.flatten(self.vii)]
        elif "minor" in self.name:
            self.diminished7_letters = [self.root, self.iii, tones.flatten(self.V), tones.flatten(self.vii)]
        else:
            raise ValueError("Cannot provide diminished 7 tones for key {}".format(self.name))
        self.diminished7_tones = [t for t in tones.all_tones if letter(t) in self.diminished7_letters]

        self.descending_chromatic_letters = ['c', 'df', 'd', 'ef', 'e', 'f', 'gf', 'g', 'af', 'a', 'bf', 'b']
        self.descending_chromatic_tones = [t for t in tones.all_tones if letter(t) in self.descending_chromatic_letters]
        self.ascending_chromatic_letters = ['c', 'cs', 'd', 'ds', 'e', 'f', 'fs', 'g', 'gs', 'a', 'as', 'b']
        self.ascending_chromatic_tones = [t for t in tones.all_tones if letter(t) in self.ascending_chromatic_letters]

    def scale_subset(self, positions):
        index_of_root = self.letters.index(self.root)
        custom_letters = [(self.letters * 2)[index_of_root + p - 1] for p in positions]
        return [t for t in self.all_tones if letter(t) in custom_letters]

    def bias(self):
        num_sharps = len([l for l in self.letters if "s" in l])
        num_flats = len([l for l in self.letters if "f" in l and l not in ['f', 'fs', 'fss']])

        if "harmonic" in self.name:
            num_flats -= 1

        if num_sharps < num_flats:
            return "flat"
        else:
            return "sharp"

    def define(self):
        raise NotImplementedError("Key.define must be overwritten.")

    def __str__(self):
        string = "\\key " + self.name
        string = string.replace(" minor", " \\minor")
        string = string.replace(" major", " \\major")
        string = string.replace(" sharp", "s")
        string = string.replace(" flat", "f")
        string = string.replace(" harmonic", "")
        string = string.replace(" melodic", "")
        return string + '\n'

    def relative_letter(self, relative_position):
        index_of_root = self.letters.index(self.root)
        new_index = index_of_root + relative_position
        return (self.letters * 2)[new_index]

    def relative_chromatic_letter(self, relative_position):
        index_of_root = self.all_letters.index(self.root)
        new_index = index_of_root + relative_position
        return (self.all_letters * 2)[new_index]

    @property
    def tonic(self):
        return self.relative_letter(0)

    @property
    def supertonic(self):
        return self.relative_letter(1)

    @property
    def mediant(self):
        return self.relative_letter(2)

    @property
    def subdominant(self):
        return self.relative_letter(3)

    @property
    def dominant(self):
        return self.relative_letter(4)

    @property
    def submediant(self):
        return self.relative_letter(5)

    @property
    def leading(self):
        return self.relative_letter(6)

    @property
    def subtonic(self):
        return self.leading

    @property
    def i(self):
        return self.tonic

    @property
    def ii(self):
        return self.supertonic

    @property
    def iii(self):
        return self.mediant

    @property
    def iv(self):
        return self.subdominant

    @property
    def v(self):
        return self.dominant

    @property
    def vi(self):
        return self.submediant

    @property
    def vii(self):
        return self.leading

    @property
    def I(self):
        return self.tonic

    @property
    def II(self):
        return self.supertonic

    @property
    def III(self):
        return self.mediant

    @property
    def IV(self):
        return self.subdominant

    @property
    def V(self):
        return self.dominant

    @property
    def VI(self):
        return self.submediant

    @property
    def VII(self):
        return self.leading


class CFlatMajor(Key):
    def define(self):
        self.root = 'cf'
        self.letters = ['cf', 'df', 'ef', 'ff', 'gf', 'af', 'bf']
        self.name = "c flat major"


class CMajor(Key):
    def define(self):
        self.root = 'c'
        self.letters = ['c', 'd', 'e', 'f', 'g', 'a', 'b']
        self.name = "c major"


class CSharpMajor(Key):
    def define(self):
        self.root = 'cs'
        self.letters = ['cs', 'ds', 'es', 'fs', 'gs', 'as', 'bs']
        self.name = "c sharp major"


class DFlatMajor(Key):
    def define(self):
        self.root = 'df'
        self.letters = ['c', 'df', 'eb', 'f', 'gf', 'af', 'bf']
        self.name = "d flat major"


class DMajor(Key):
    def define(self):
        self.root = 'd'
        self.letters = ['cs', 'd', 'e', 'fs', 'g', 'a', 'b']
        self.name = "d major"


class EFlatMajor(Key):
    def define(self):
        self.root = 'ef'
        self.letters = ['c', 'd', 'ef', 'f', 'g', 'af', 'bf']
        self.name = "e flat major"


class EMajor(Key):
    def define(self):
        self.root = 'e'
        self.letters = ['cs', 'ds', 'e', 'fs', 'gs', 'a', 'b']
        self.name = "e major"


class FMajor(Key):
    def define(self):
        self.root = 'f'
        self.letters = ['c', 'd', 'e', 'f', 'g', 'a', 'bf']
        self.name = "f major"


class FSharpMajor(Key):
    def define(self):
        self.root = 'fs'
        self.letters = ['cs', 'ds', 'es', 'fs', 'gs', 'as', 'b']
        self.name = "f sharp major"


class GFlatMajor(Key):
    def define(self):
        self.root = 'gf'
        self.letters = ['cf', 'df', 'ef', 'f', 'gf', 'af', 'bf']
        self.name = "g flat major"


class GMajor(Key):
    def define(self):
        self.root = 'g'
        self.letters = ['c', 'd', 'e', 'fs', 'g', 'a', 'b']
        self.name = "g major"


class AFlatMajor(Key):
    def define(self):
        self.root = 'af'
        self.letters = ['c', 'df', 'ef', 'f', 'g', 'af', 'bf']
        self.name = "a flat major"


class AMajor(Key):
    def define(self):
        self.root = 'a'
        self.letters = ['cs', 'd', 'e', 'fs', 'gs', 'a', 'b']
        self.name = "a major"


class BFlatMajor(Key):
    def define(self):
        self.root = 'bf'
        self.letters = ['c', 'd', 'ef', 'f', 'g', 'a', 'bf']
        self.name = "b flat major"


class BMajor(Key):
    def define(self):
        self.root = 'b'
        self.letters = ['cs', 'ds', 'e', 'fs', 'gs', 'as', 'b']
        self.name = "b major"


class CMinor(Key):
    def define(self):
        self.root = 'c'
        self.letters = ['c', 'd', 'ef', 'f', 'g', 'af', 'bf']
        self.name = "c minor"


class CMinorH(Key):
    def define(self):
        self.root = 'c'
        self.letters = ['c', 'd', 'ef', 'f', 'g', 'af', 'b']
        self.name = "c minor harmonic"


class CSharpMinor(Key):
    def define(self):
        self.root = 'cs'
        self.letters = ['cs', 'ds', 'e', 'fs', 'gs', 'a', 'b']
        self.name = "c sharp minor"


class CSharpMinorH(Key):
    def define(self):
        self.root = 'cs'
        self.letters = ['cs', 'ds', 'e', 'fs', 'gs', 'a', 'bs']
        self.name = "c sharp minor harmonic"


class DFlatMinor(Key):
    def define(self):
        self.root = 'df'
        self.letters = ['df', 'ef', 'ff', 'gf', 'af', 'bff', 'cf']
        self.name = 'd flat minor'


class DFlatMinorH(Key):
    def define(self):
        self.root = 'df'
        self.letters = ['df', 'ef', 'ff', 'gf', 'af', 'bff', 'c']
        self.name = 'd flat minor harmonic'


class DMinor(Key):
    def define(self):
        self.root = 'd'
        self.letters = ['c', 'd', 'e', 'f', 'g', 'a', 'bf']
        self.name = "d minor"


class DMinorH(Key):
    def define(self):
        self.root = 'd'
        self.letters = ['cs', 'd', 'e', 'f', 'g', 'a', 'bf']
        self.name = "d minor harmonic"


class DSharpMinor(Key):
    def define(self):
        self.root = 'ds'
        self.letters = ['cs', 'ds', 'es', 'fs', 'gs', 'as', 'b']
        self.name = "d sharp minor"


class DSharpMinorH(Key):
    def define(self):
        self.root = 'ds'
        self.letters = ['css', 'ds', 'es', 'fs', 'gs', 'as', 'b']
        self.name = "d sharp minor harmonic"


class EFlatMinor(Key):
    def define(self):
        self.root = 'ef'
        self.letters = ['cf', 'df', 'ef', 'f', 'gf', 'af', 'bf']
        self.name = "e flat minor"


class EFlatMinorH(Key):
    def define(self):
        self.root = 'ef'
        self.letters = ['cf', 'd', 'ef', 'f', 'gf', 'af', 'bf']
        self.name = "e flat minor harmonic"


class EMinor(Key):
    def define(self):
        self.root = 'e'
        self.letters = ['c', 'd', 'e', 'fs', 'g', 'a', 'b']
        self.name = "e minor"


class EMinorH(Key):
    def define(self):
        self.root = 'e'
        self.letters = ['c', 'ds', 'e', 'fs', 'g', 'a', 'b']
        self.name = "e minor harmonic"


class FMinor(Key):
    def define(self):
        self.root = 'f'
        self.letters = ['c', 'df', 'ef', 'f', 'g', 'af', 'bf']
        self.name = "f minor"


class FMinorH(Key):
    def define(self):
        self.root = 'f'
        self.letters = ['c', 'df', 'e', 'f', 'g', 'af', 'bf']
        self.name = "f minor harmonic"


class FSharpMinor(Key):
    def define(self):
        self.root = 'fs'
        self.letters = ['cs', 'd', 'e', 'fs', 'gs', 'a', 'b']
        self.name = "f sharp minor"


class FSharpMinorH(Key):
    def define(self):
        self.root = 'fs'
        self.letters = ['cs', 'd', 'es', 'fs', 'gs', 'a', 'b']
        self.name = "f sharp minor harmonic"


class GMinor(Key):
    def define(self):
        self.root = 'g'
        self.letters = ['c', 'd', 'ef', 'f', 'g', 'a', 'bf']
        self.name = "g minor"


class GMinorH(Key):
    def define(self):
        self.root = 'g'
        self.letters = ['c', 'd', 'ef', 'fs', 'g', 'a', 'bf']
        self.name = "g minor harmonic"


class GSharpMinor(Key):
    def define(self):
        self.root = 'gs'
        self.letters = ['cs', 'ds', 'e', 'fs', 'gs', 'as', 'b']
        self.name = "g sharp minor"


class GSharpMinorH(Key):
    def define(self):
        self.root = 'gs'
        self.letters = ['cs', 'ds', 'e', 'fss', 'gs', 'as', 'b']
        self.name = "g sharp minor harmonic"


class AFlatMinor(Key):
    def define(self):
        self.root = 'af'
        self.letters = ['cf', 'df', 'ef', 'ff', 'gf', 'af', 'bf']
        self.name = "a flat minor"


class AFlatMinorH(Key):
    def define(self):
        self.root = 'af'
        self.letters = ['cf', 'df', 'ef', 'ff', 'g', 'af', 'bf']
        self.name = "a flat minor harmonic"


class AMinor(Key):
    def define(self):
        self.root = 'a'
        self.letters = ['c', 'd', 'e', 'f', 'g', 'a', 'b']
        self.name = "a minor"


class AMinorH(Key):
    def define(self):
        self.root = 'a'
        self.letters = ['c', 'd', 'e', 'f', 'gs', 'a', 'b']
        self.name = "a minor harmonic"


class ASharpMinor(Key):
    def define(self):
        self.root = 'as'
        self.letters = ['cs', 'ds', 'es', 'fs', 'gs', 'as', 'bs']
        self.name = "a sharp minor"


class ASharpMinorH(Key):
    def define(self):
        self.root = 'as'
        self.letters = ['cs', 'ds', 'es', 'fs', 'gss', 'as', 'bs']
        self.name = "a sharp minor harmonic"


class BFlatMinor(Key):
    def define(self):
        self.root = 'bf'
        self.letters = ['c', 'df', 'ef', 'f', 'gf', 'af', 'bf']
        self.name = "b flat minor"


class BFlatMinorH(Key):
    def define(self):
        self.root = 'bf'
        self.letters = ['c', 'df', 'ef', 'f', 'gf', 'a', 'bf']
        self.name = "b flat minor harmonic"


class BMinor(Key):
    def define(self):
        self.root = 'b'
        self.letters = ['cs', 'd', 'e', 'fs', 'g', 'a', 'b']
        self.name = "b minor"


class BMinorH(Key):
    def define(self):
        self.root = 'b'
        self.letters = ['cs', 'd', 'e', 'fs', 'g', 'as', 'b']
        self.name = "b minor harmonic"


key_dictionary = {
    "major": {
        "cf": CFlatMajor(),
        "c": CMajor(),
        "cs": CSharpMajor(),
        "df": DFlatMajor(),
        "d": DMajor(),
        "ef": EFlatMajor(),
        "e": EMajor(),
        "f": FMajor(),
        "fs": FSharpMajor(),
        "gf": GFlatMajor(),
        "g": GMajor(),
        "af": AFlatMajor(),
        "a": AMajor(),
        "bf": BFlatMajor(),
        "b": BMajor()
    },
    "minor": {
        "c": CMinor(),
        "cs": CSharpMinor(),
        "df": DFlatMinor(),
        "d": DMinor(),
        "ds": DSharpMinor(),
        "ef": EFlatMinor(),
        "e": EMinor(),
        "f": FMinor(),
        "fs": FSharpMinor(),
        "g": GMinor(),
        "gs": GSharpMinor(),
        "af": AFlatMinor(),
        "a": AMinor(),
        "as": ASharpMinor(),
        "bf": BFlatMinor(),
        "b": BMinor()
    },
    "harmonic": {
        "c": CMinorH(),
        "cs": CSharpMinorH(),
        "d": DMinorH(),
        "df": DFlatMinorH(),
        "ds": DSharpMinorH(),
        "ef": EFlatMinorH(),
        "e": EMinorH(),
        "f": FMinorH(),
        "fs": FSharpMinorH(),
        "g": GMinorH(),
        "gs": GSharpMinorH(),
        "af": AFlatMinorH(),
        "a": AMinorH(),
        "as": ASharpMinorH(),
        "bf": BFlatMinorH(),
        "b": BMinorH()
    }
}


def keyify(key):
    if isinstance(key, Key):
        return key
    elif isclass(key) and issubclass(key, Key):
        return key()
    elif isinstance(key, str):
        try:
            key = key.split(" ")
            letter = key[0].lower()
            mode = " ".join(key[1:]).lower()
            if 'harmonic' in mode:
                mode = 'harmonic'
            return key_dictionary[mode][letter]
        except Exception:
            raise ValueError("{} is not a valid string format for a key".format(key))
    else:
        raise ValueError("{} is not a valid key".format(key))
