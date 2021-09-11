import time

from pytest import raises
from unittest.mock import Mock

from zdict.exceptions import NotFoundError
from zdict.zdict import get_args

from zdict.dictionaries.naer import NaerDict


class TestNaerDict:
    @classmethod
    def setup_class(cls):
        cls.dict = NaerDict(get_args())

        # You may want to change words to some certain test cases.
        cls.words = ['西爾河', 'spring mass']
        cls.not_found_word = 'dsafwwe'

        # Set query_timeout from 5 seconds to 120 seconds,
        # so it won't timeout that often.
        cls.dict.args.query_timeout = 120

        # Setup normal query data
        cls.dict.args.verbose = False
        cls.records = []
        for word in cls.words:
            record = None
            while True:
                try:
                    record = cls.dict.query(word)
                except Exception:
                    # prevent API 500 error
                    time.sleep(5)
                    continue
                else:
                    cls.records.append(record)
                    break

        cls.records = [cls.dict.query(word) for word in cls.words]

        # Setup verbose query data
        cls.dict.args.verbose = True
        cls.verbose_records = []
        for word in cls.words:
            record = None
            while True:
                try:
                    record = cls.dict.query(word)
                except Exception:
                    # prevent API 500 error
                    time.sleep(5)
                    continue
                else:
                    cls.verbose_records.append(record)
                    break

        # Change back to default verbose config
        cls.dict.args.verbose = False

    @classmethod
    def teardown_class(cls):
        del cls.dict
        del cls.words
        del cls.not_found_word
        del cls.records
        del cls.verbose_records

    def test_provider(self):
        assert self.dict.provider == 'naer'

    def test_title(self):
        assert self.dict.title == (
            '國家教育研究院 - 雙語詞彙、學術名詞暨辭書資訊網'
        )

    def test__get_url(self):
        url = 'https://terms.naer.edu.tw/search?q=test&field=ti&match=smart'
        assert url == self.dict._get_url('test')

    def test_show(self):
        self.dict.args.verbose = False

        for record in self.records:
            self.dict.show(record)

    def test_show_verbose(self):
        self.dict.args.verbose = True

        for record in self.verbose_records:
            self.dict.show(record)

    def test_query_normal(self):
        self.dict.args.verbose = False

        query_record = None
        for i, word in enumerate(self.words):
            while True:
                try:
                    query_record = self.dict.query(word)
                except Exception:
                    # prevent itaigi API 500 error
                    time.sleep(5)
                    continue
                else:
                    assert query_record.content == self.records[i].content
                    break

    def test_query_verbose(self):
        self.dict.args.verbose = True

        query_record = None
        for i, word in enumerate(self.words):
            while True:
                try:
                    query_record = self.dict.query(word)
                except Exception:
                    # prevent itaigi API 500 error
                    time.sleep(5)
                    continue
                else:
                    assert (
                        query_record.content
                        ==
                        self.verbose_records[i].content
                    )
                    break

    def test_query_not_found(self):
        # Trigger NotFoundError intentionally and see if it works.
        self.dict._get_raw = Mock(return_value='')
        with raises(NotFoundError):
            self.dict.query(self.not_found_word)
