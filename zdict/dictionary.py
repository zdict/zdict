import abc
import json

import requests

from zdict import exceptions
from zdict.models import Record, db
from zdict.utils import Color


class DictBase(metaclass=abc.ABCMeta):

    REQUIRED_TABLE = (
        Record,
    )

    def __init__(self, args):
        self.args = args
        self.color = Color()
        self.db = db

        try:
            self.db.connection()
        except Exception:
            self.db = None
            raise
        else:
            for req in self.REQUIRED_TABLE:
                if not req.table_exists():
                    req.create_table()

    def __del__(self):
        del self.args
        del self.color

        if self.db:
            try:
                self.db.close()
            except AttributeError:
                raise RuntimeError('db cannot be closed properly.')
        del self.db

    @property
    @abc.abstractmethod
    def provider(self):
        '''
        Return the provider of online dictionary,
        this value is considered as `source` field in Record model.
        '''
        ...

    @property
    @abc.abstractmethod
    def title(self):
        '''
        Return the brief title of online dictionary,
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
    def query(self, word: str) -> Record:
        '''
        Define how to get the information from specific dictionary.
        Should return a record contains word, content and source.
        '''
        ...

    def query_db_cache(self, word: str) -> Record:
        try:
            record = Record.get(word=word, source=self.provider)
        except Record.DoesNotExist:
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

    def show_provider(self):
        self.color.print('[' + self.provider + ']', 'blue')

    def show_url(self, word):
        self.color.print('(' + self._get_url(word) + ')', 'blue')

    def lookup(self, word):
        '''
        Main workflow for searching a word.
        '''

        word = word.lower()

        if self.args.show_provider:
            self.show_provider()

        if self.args.show_url:
            self.show_url(word)

        if not self.args.disable_db_cache:
            record = self.query_db_cache(word)

            if record:
                self.show(record)
                return

        try:
            record = self.query(word)
        except exceptions.NoNetworkError as e:
            self.color.print(e, 'red')
            print()
        except exceptions.TimeoutError as e:
            self.color.print(e, 'red')
            print()
        except exceptions.APIKeyError as e:
            self.color.print(e, 'red')
            print()
        except exceptions.NotFoundError as e:
            self.color.print(e, 'yellow')
            print()
        except Exception:
            import traceback

            print('='*80)
            traceback.print_exc()
            print()
            print("Dictionary: {} ({})".format(self.title, self.provider))
            print("Word: '{}'".format(word))
            print('='*80)
            print()

            url = "https://github.com/zdict/zdict/issues"
            print("Houston, we got a problem 😢")
            print("Please report the error message above to {}".format(url))

            import sys
            sys.exit(1)
        else:
            self.save(record, word)
            self.show(record)
            return

    def _get_raw(self, word: str, **kwargs) -> str:
        '''
        Get raw data from http request

        :param word: single word
        '''

        try:
            res = requests.get(
                self._get_url(word), timeout=self.args.query_timeout, **kwargs
            )
        except requests.exceptions.ReadTimeout:
            raise exceptions.TimeoutError()
        except requests.exceptions.ConnectionError as e:
            errors = {
                "BlockingIOError(36, 'Operation now in progress')":
                    "exceptions.TimeoutError()",
                "Failed to establish a new connection":
                    "exceptions.NoNetworkError()",
            }
            for error, exception in errors.items():
                if error in str(e.args):
                    raise eval(exception)
            else:
                raise exceptions.UnexpectedError()
        except Exception:
            raise exceptions.UnexpectedError()

        if res.status_code != 200:
            raise exceptions.QueryError(word, res.status_code)

        if self.args.debug:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(res.text, 'html.parser')
            print('=' * 30 + ' Start of debug info ' + '=' * 30)
            print(soup.prettify())
            print('=' * 30 + ' End of debug info ' + '=' * 30)

        return res.text
