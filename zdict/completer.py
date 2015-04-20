from .models import Record, db


class DictCompleter:
    def __init__(self):
        self.db = db
        self.db.connect()

    def __del__(self):
        self.db.close()

    def complete(self, text, state):
        match = []
        n = len(text)

        for record in Record.select():
            word = record.word
            if word[:n] == text[:n]:
                match.append(word)
        return match[state]
