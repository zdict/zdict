import abc
import json

import requests

from . import constants
from .exceptions import NotFoundError
from .models import Record, db
from .utils import Color


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

    def lookup(self, word):
        try:
            record = self.query(word)
        except NotFoundError as e:
            self.color.print(e, 'yellow')
        else:
            self.show(record)

    def prompt(self):
        user_input = input(self._get_prompt()).strip()

        if user_input:
            self.lookup(user_input)
        else:
            return

    def loop_prompt(self):
        while True:
            try:
                self.prompt()
            except (KeyboardInterrupt, EOFError):
                print()
                return

    @abc.abstractclassmethod
    def query(self, word: str, verbose: bool) -> Record:
        ...

    def _get_raw(self, word) -> str:
        '''
        Get raw data from http request

        :param word: single word
        '''
        res = requests.get(self._get_url(word), timeout=5)
        if res.status_code != 200:
            raise QueryError(word, res.status_code)
        return res.text
