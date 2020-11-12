class Stave:
    """ A musical stave. It has a clef, and optionally a name (for if multiple staves have the same clef). """

    def __init__(self, clef, name=None):
        if clef not in ['treble', 'bass', 'G', '"G2"', 'french', 'GG', 'tenorG', 'soprano', 'mezzosoprano', 'C', 'alto', 'tenor', 'baritone']:
            raise ValueError('{} is not a permitted clef'.format(clef))

        self.clef = clef
        if name:
            self.name = name
        else:
            self.name = clef

        self.start = '<< \\new Staff {{\n\\clef {}\n'.format(self.clef)
        self.end = '} >>\n'


class Treble(Stave):

    def __init__(self, name=None):
        super().__init__("treble", name)


class Bass(Stave):

    def __init__(self, name=None):
        super().__init__("bass", name)
