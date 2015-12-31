class QueryError(Exception):
    def __init__(self, word, status_code):
        self.word = word
        self.status_code = status_code

    def __str__(self):
        return '"{}" query failed on http[{}].'.format(
            self.word, self.status_code
        )


class NotFoundError(Exception):
    def __init__(self, word):
        self.word = word

    def __str__(self):
        return '"{}" not found!'.format(self.word)


class NoNetworkError(Exception):
    def __str__(self):
        return 'No Network Connection!'


class TimeoutError(Exception):
    def __str__(self):
        return 'Query timeout!'


class UnexpectedError(Exception):
    def __init__(self):
        print(
            '\n'.join((
                '',
                "Unexpected error happened.",
                "Please report the error message below to",
                "https://github.com/zdict/zdict/issues",
                '',
            ))
        )
