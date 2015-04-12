class DictCompleter:
    def __init__(self, db):
        self.db = db

    def complete(self, text, state):
        match = []
        n = len(text)

        for word in self.db.keys():
            if word[:n] == text[:n]:
                match.append(word)
        return match[state]
