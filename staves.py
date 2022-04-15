class Stave:
    """ A musical stave. It has a clef, and optionally a name (for if multiple staves have the same clef). """

    def __init__(self, clef, name=None, extra_text='', _with=''):
        if clef not in ['treble', 'bass', 'G', '"G2"', 'french', 'GG', 'tenorG', 'soprano', 'mezzosoprano', 'C', 'alto', 'tenor', 'baritone', 'dynamics']:
            raise ValueError('{} is not a permitted clef'.format(clef))

        self.clef = clef
        if name:
            self.name = name
        else:
            self.name = clef

        self.extra_text = extra_text
        self._with = _with

    @property
    def start(self):
        return '<< \\new Staff = "{}" \\with {{\n{}\n}}{{\n{}\n\\clef {}\n'.format(self.name, self._with, self.extra_text, self.clef)

    @property
    def end(self):
        return '} >>\n'


class Treble(Stave):

    def __init__(self, name=None, extra_text='', _with=''):
        super().__init__("treble", name, extra_text, _with)


class Bass(Stave):

    def __init__(self, name=None, extra_text='', _with=''):
        super().__init__("bass", name, extra_text, _with)


class Super(Stave):

    def __init__(self, name=None, extra_text='', _with=''):
        super().__init__("treble", name, extra_text, _with)
        self.extra_text += " \\override Staff.StaffSymbol.line-count = #10 \n \\override Staff.StaffSymbol.line-positions = #'(-16 -14 -12 -10 -8 -4 -2 0 2 4)"


class Dynamics(Stave):

    def __init__(self, name=None):
        super().__init__("dynamics", name)

    @property
    def start(self):
        return '<< \\new Dynamics {{'.format(self.name, self._with, self.extra_text, self.clef)
