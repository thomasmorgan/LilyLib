class Stave:
    """ A musical stave. It has a clef, and optionally a name
    (to distinguish multiple staves with the same clef). """

    def __init__(self, clef, name=None, extra_text='', _with=''):
        if clef not in (['treble', 'bass', 'G', '"G2"', 'french', 'GG',
                         'tenorG', 'soprano', 'mezzosoprano', 'C', 'alto',
                         'tenor', 'baritone', 'dynamics']):
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
        start = '<< \\new Staff = "{}" '.format(self.name)
        if self._with:
            start += '\\with {{\n{}\n}}'.format(self._with)
        start += '{'
        if self.extra_text:
            start += '\n{}\n'.format(self.extra_text)
        start += '\n\\clef {}\n'.format(self.clef)
        return start

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
        self.extra_text += (
            " \\override Staff.StaffSymbol.line-count = #10 \n" +
            " \\override Staff.StaffSymbol.line-positions = #'" +
            "(-16 -14 -12 -10 -8 -4 -2 0 2 4)")


class Dynamics(Stave):

    def __init__(self, name=None, extra_text='', _with=''):
        super().__init__("dynamics", name)

    @property
    def start(self):
        return '<< \\new Dynamics {{'.format(
            self.name, self._with, self.extra_text, self.clef)
