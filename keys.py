from models import Key


class CMajor(Key):
    def define(self):
        self.root = 'c'
        self.letters = ['c', 'd', 'e', 'f', 'g', 'a', 'b']
        self.name = "c major"


class DMajor(Key):
    def define(self):
        self.root = 'd'
        self.letters = ['cs', 'd', 'e', 'fs', 'g', 'a', 'b']
        self.name = "d major"


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


class GMajor(Key):
    def define(self):
        self.root = 'g'
        self.letters = ['c', 'd', 'e', 'fs', 'g', 'a', 'b']
        self.name = "g major"


class AMajor(Key):
    def define(self):
        self.root = 'a'
        self.letters = ['cs', 'd', 'e', 'fs', 'gs', 'a', 'b']
        self.name = "a major"


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
        self.name = "c minor"


class DMinor(Key):
    def define(self):
        self.root = 'd'
        self.letters = ['c', 'd', 'e', 'f', 'g', 'a', 'bf']
        self.name = "g minor"


class DMinorH(Key):
    def define(self):
        self.root = 'd'
        self.letters = ['cs', 'd', 'e', 'f', 'g', 'a', 'bf']
        self.name = "g minor"


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


class AMinor(Key):
    def define(self):
        self.root = 'a'
        self.letters = ['c', 'd', 'e', 'f', 'g', 'a', 'b']
        self.name = "a minor"
