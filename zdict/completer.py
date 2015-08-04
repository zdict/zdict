from .models import Record, db


class DictCompleter:
    def __init__(self):
        self.db = db
        self.db.connect()

    def __del__(self):
        self.db.close()

    def complete(self, text, state):
        match = []

        for record in Record.select():
            word = record.word
            if word.startswith(text):
                match.append(word)
        return match[state]
