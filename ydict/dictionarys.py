import abc

import pony.orm as pony
import requests

from . import constants


class DictBase(metaclass=abc.ABCMeta):
    def __init__(self):
        self.db = pony.Database('sqlite', constants.DB_FILE, create_db=True)
        self.db.generate_mapping(create_tables=True)

    @abc.abstractmethod
    def _get_prompt(self) -> str:
        '''
        The prompt string is used by prompt()
        '''
        ...

    def prompt(self):
        return self.query(input(self._get_prompt()).strip())

    @abc.abstractclassmethod
    def query(self, word: str):
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
