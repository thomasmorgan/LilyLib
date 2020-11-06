from models import Key


class CFlatMajor(Key):
    def define(self):
        self.root = 'cf'
        self.letters = ['cf', 'fd', 'ef', 'ff', 'gf', 'af', 'bf']
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
