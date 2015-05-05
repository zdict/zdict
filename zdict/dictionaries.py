import abc
import json
from functools import reduce, singledispatch
from itertools import product

import requests

from bs4 import BeautifulSoup

from . import constants
from .exceptions import NotFoundError
from .models import Record, db
from .soup import DictionarySoup
from .utils import Color, sequence


class DictBase(metaclass=abc.ABCMeta):

    REQUIRED_TABLE = (
        Record,
    )

    def __init__(self):
        self.db = db
        self.db.connect()

        for req in self.REQUIRED_TABLE:
            if not req.table_exists():
                req.create_table()

        self.color = Color()


    def __del__(self):
        self.db.close()

    @property
    @abc.abstractmethod
    def provider(self):
        '''
        Return the provider of online dictionary,
        this value is considered as `source` field in Record model.
        '''
        ...

    def show(self, record: Record):
        ...

    @abc.abstractmethod
    def _get_prompt(self) -> str:
        '''
        The prompt string is used by prompt()
        '''
        ...

    def prompt(self):
        user_input = input(self._get_prompt()).strip()

        if not user_input:
            return

        try:
            record = self.query(user_input)
        except NotFoundError as e:
            self.color.print(e, 'yellow')
            return

        # self.show(record)

    def loop_prompt(self):
        while True:
            try:
                self.prompt()
            except (KeyboardInterrupt, EOFError):
                print()
                return

    def query(self, word: str) -> Record:
        '''
        :param word: lookup word
        '''
        keyword = word.lower()

        try:
            record = Record.get(word=keyword, source=self.provider)
        except Record.DoesNotExist as e:
            record = Record(word=keyword, source=self.provider, content=None)
        else:
            return record

        data = BeautifulSoup(self._get_raw(word))

        self._expand_selectors(self.selectors)
        # record.content = json.dumps(self.parse(data))
        # record.save(force_insert=True)
        # return record

    @property
    @abc.abstractmethod
    def selectors(self, data: DictionarySoup) -> dict:
        ...

    def _expand_selectors(self, selectors: dict or sequence or str) -> tuple:
        '''
        Expand selectors
        e.g. {
            'div.a': [
                'span',
                'p',
            ],
            'ul': 'a',
        }
        will return
        (
            'div.a span',
            'div.a p',
            'ul a',
        )
        '''
        @singledispatch
        def f(selectors):
            raise TypeError(
                'selectors "{}" should be dict, sequence or str'.format(
                    selectors
                )
            )

        @f.register(str)
        def _(selectors):
            return (selectors, )

        @f.register(dict)
        def _(selectors):
            return tuple(
                reduce(
                    lambda x, y: tuple(x) + tuple(y),
                    map(
                        lambda key: map(
                            lambda l: ' '.join(l),
                            product((key,), f(selectors.get(key)))
                        ),
                        sorted(selectors.keys())
                    )
                )
            )

        @f.register(sequence)
        def _(selectors):
            return tuple(
                reduce(
                    lambda x, y: x + y,
                    map(lambda x: f(x), selectors)
                )
            )

        return f(selectors)


    def _get_raw(self, word) -> str:
        '''
        Get raw data from http request

        :param word: single word
        '''
        res = requests.get(self._get_url(word), timeout=5)
        if res.status_code != 200:
            raise QueryError(word, res.status_code)
        return res.text
