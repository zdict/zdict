from zdict.models import Record, db


class DictCompleter:
    def __init__(self):
        self.db = db
        self.db.connect()

    def __del__(self):
        self.db.close()

    def complete(self, text, state):
        if state == 0:  # new query
            self.records = iter(
                Record.select().where(Record.word.startswith(text)))

        return next(self.records).word
