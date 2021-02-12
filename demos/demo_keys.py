from piece import Piece
from keys import key_dictionary
from points import note
from markup import key_signature


class AllKeys(Piece):

    def details(self):
        self.title = "Root notes in every key"
        self.key = "cf major"

    def write_score(self):
        self.score["treble"] = []
        self.score["bass"] = []

        for mode in key_dictionary:
            for letter in key_dictionary[mode]:
                self.set_key(key_dictionary[mode][letter])
                self.score["treble"] += key_signature(self.key, note(self.key.root + "`", 1, markup=self.key.name))
                self.score["bass"] += key_signature(self.key, note(self.key.root, 1))

        self.score["treble"][0].prefix = "\\set Staff.printKeyCancellation = ##f " + self.score["treble"][0].prefix
        self.score["bass"][0].prefix = "\\set Staff.printKeyCancellation = ##f " + self.score["bass"][0].prefix


if __name__ == "__main__":
    AllKeys()
