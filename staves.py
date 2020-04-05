from models import Stave


class Treble(Stave):

    def __init__(self, name=None):
        super().__init__("treble", name)


class Bass(Stave):

    def __init__(self, name=None):
        super().__init__("bass", name)
