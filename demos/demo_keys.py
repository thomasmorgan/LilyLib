from piece import Piece
from keys import key_dictionary


class AllKeys(Piece):

    def details(self):
        self.title = "Root notes in every key"
        self.key = "cf major"

    def write_score(self):
        self.score["treble"] = ["\\set Staff.printKeyCancellation = ##f "]
        self.score["bass"] = ["\\set Staff.printKeyCancellation = ##f "]

        for mode in key_dictionary:
            for letter in key_dictionary[mode]:
                self.set_key(key_dictionary[mode][letter])
                self.score["treble"] += self.key_signature + self.note(self.key.root + "`", 1, ornamentation=self.annotation(self.key.name))
                self.score["bass"] += self.key_signature + self.note(self.key.root, 1)


if __name__ == "__main__":
    AllKeys()
