

class QueryError(Exception):
    def __init__(self, word, status_code):
        self.word = word
        self.status_code = status_code

    def __str__(self):
        return '"{}" query failed on http[{}].'.format(self.word, self.status_code)
