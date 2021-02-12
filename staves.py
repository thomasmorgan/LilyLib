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

        self.extra_text = ''

    @property
    def start(self):
        return '<< \\new Staff {{\n{}\n\\clef {}\n'.format(self.extra_text, self.clef)

    @property
    def end(self):
        return '} >>\n'


class Treble(Stave):

    def __init__(self, name=None):
        super().__init__("treble", name)


class Bass(Stave):

    def __init__(self, name=None):
        super().__init__("bass", name)


class Super(Stave):

    def __init__(self, name=None):
        super().__init__("treble", name)
        self.extra_text = "\\override Staff.StaffSymbol.line-count = #10 \n \\override Staff.StaffSymbol.line-positions = #'(-16 -14 -12 -10 -8 -4 -2 0 2 4)"
