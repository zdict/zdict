import json

from ..dictionary import DictBase
from ..exceptions import QueryError, NotFoundError
from ..models import Record
from ..utils import pyjokes


class PyjokesDict(DictBase):

    API = 'https://github.com/pyjokes/pyjokes'

    @property
    def provider(self):
        return 'pyjokes'

    @property
    def title(self):
        return 'pyjokes'

    def _get_url(self, word) -> str:
        return self.API

    def show(self, record: Record, verbose=False):
        self.color.print(record.word, 'yellow')
        import re
        for i,s in enumerate(re.split(r'\b({})\b'.format(record.word), record.content)):
            self.color.print(
                s,
                'lindigo' if i % 2 else 'indigo',
                end=''
            )

        print('\n\n', end='')


    def query(self, word: str, timeout: float, verbose=False):
        if not pyjokes:
            return

        import random
        try:
            # very basic string searching in jokes
            r = random.choice(
                list(filter(
                    lambda j: word in map(
                        lambda x: ''.join(c for c in x if c.isalnum()),
                        j.split()
                    ),
                    pyjokes.get_jokes()
                ))
            )
            return Record(word=word, content=r, source=self.provider)
        except IndexError:
            return

    def lookup(self, word: str, args):
        '''
        Overriding DictBase.lookup as pyjokes is not a real online dictionary.
        Result should not being saved into database.
        '''

        word = word.lower()

        if isinstance(word, Record):
            record = word
        else:
            record = self.query(word, args.query_timeout, args.verbose)

        self.output(record, args)

        return

    def output(self, record: Record, args):
        if args.show_provider:
            self.show_provider()

        if args.show_url:
            self.show_url(word)

        if record:
            self.show(record, args.verbose)
