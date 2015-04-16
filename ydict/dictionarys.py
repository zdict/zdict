import abc
import json

import requests

from . import constants
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

    @abc.abstractmethod
    def _get_prompt(self) -> str:
        '''
        The prompt string is used by prompt()
        '''
        ...

    def prompt(self):
        self.show(
            self.query(input(self._get_prompt()).strip())
        )

    @abc.abstractclassmethod
    def query(self, word: str) -> Record:
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

    def show(self, record: Record):
        content = json.loads(record.content)
        # print keyword
        self.color.print(record.word, 'yellow')
        # print pronounce
        for k, v in content.get('pronounce', []):
            self.color.print(k, end='')
            self.color.print(v, 'lwhite', end=' ')
        print()
        # print explain
        explain = content.get('explain')
        for speech in explain:
            self.color.print(speech[0], 'lred')
            for index, meaning in enumerate(speech[1:], start=1):
                self.color.print(
                    '{num}. {text}'.format(num=index, text=meaning[0]),
                    'org',
                    indent=2
                )
                for sentence in meaning[1:]:
                    print(' ' * 4, end='')
                    for i, s in enumerate(sentence[0].split('*')):
                        self.color.print(
                            s, 
                            'lindigo' if i == 1 else 'indigo',
                            end=''
                        )
                    print()
                    self.color.print(sentence[1], 'green', indent=4)


    @property
    @abc.abstractmethod
    def provider(self):
        '''
        Return the provider of online dictionary,
        this value is considered as `source` field in Record model.
        '''
        ...
