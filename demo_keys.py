from piece import Piece
from models import Note
from keys import major_keys, minor_keys, harmonic_keys


class AllKeys(Piece):

    def details(self):
        self.title = "Root notes in every key"
        self.key = ""

    def write_score(self):
        self.score["treble"] = ["\\set Staff.printKeyCancellation = ##f "]
        self.score["bass"] = ["\\set Staff.printKeyCancellation = ##f "]

        for key_set in [major_keys(), minor_keys(), harmonic_keys()]:
            for key in key_set:
                self.score["treble"].extend([key, Note(key.root + "`", 1, ornamentation=self.annotation(key.name))])
                self.score["bass"].extend([key, Note(key.root, 1)])


AllKeys()
