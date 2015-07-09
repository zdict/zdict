import abc
import json

import requests

from . import exceptions
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

    @property
    @abc.abstractmethod
    def provider(self):
        '''
        Return the provider of online dictionary,
        this value is considered as `source` field in Record model.
        '''
        ...

    @abc.abstractmethod
    def _get_url(self, word: str) -> str:
        '''
        Return the result of the current dict web url for the searching word.
        '''
        ...

    @abc.abstractmethod
    def show(self, record: Record):
        '''
        Define how to render the result of the specific dictionary.
        '''
        ...

    @abc.abstractmethod
    def query(self, word: str, timeout: float, verbose: bool) -> Record:
        '''
        Define how to get the information from specific dictionary.
        Should return a record contains word, content and source.
        '''
        ...

    def query_db_cache(self, word: str, verbose=False) -> Record:
        try:
            record = Record.get(word=word, source=self.provider)
        except Record.DoesNotExist as e:
            return None
        else:
            return record

    def save(self, query_record: Record, word: str):
        db_record = self.query_db_cache(word)

        if db_record is None:
            query_record.save(force_insert=True)
        else:
            db_content = json.loads(db_record.content)
            query_content = json.loads(query_record.content)

            if db_content != query_content:
                db_record.content = query_record.content
                db_record.save()

    def lookup(self, word, args):
        '''
        Main workflow for searching a word.
        '''

        word = word.lower()

        if not args.disable_db_cache:
            record = self.query_db_cache(word)

            if record:
                self.show(record)
                return

        try:
            record = self.query(word, args.query_timeout)
        except exceptions.NoNetworkError as e:
            self.color.print(e, 'red')
        except exceptions.TimeoutError as e:
            self.color.print(e, 'red')
        except exceptions.NotFoundError as e:
            self.color.print(e, 'yellow')
        else:
            self.save(record, word)
            self.show(record)
            return

    def _get_prompt(self) -> str:
        '''
        The prompt string used by prompt()
        '''
        return '[zDict]: '

    def prompt(self, args):
        user_input = input(self._get_prompt()).strip()

        if user_input:
            self.lookup(user_input, args)
        else:
            return

    def loop_prompt(self, args):
        while True:
            try:
                self.prompt(args)
            except (KeyboardInterrupt, EOFError):
                print()
                return

    def _get_raw(self, word: str, timeout: float) -> str:
        '''
        Get raw data from http request

        :param word: single word
        '''
        try:
            res = requests.get(self._get_url(word), timeout=timeout)
        except requests.exceptions.ConnectionError as e:
            error_msg = str(e.args)

            errs = {}
            errs["NoNetworkError()"] = \
                "gaierror(8, 'nodename nor servname provided, or not known')"
            errs["TimeoutError()"] = \
                "BlockingIOError(36, 'Operation now in progress')"

            for err, msg in errs.items():
                if msg in error_msg:
                    r = 'exceptions.' + err
                    raise eval(r)

        if res.status_code != 200:
            raise exceptions.QueryError(word, res.status_code)
        return res.text
