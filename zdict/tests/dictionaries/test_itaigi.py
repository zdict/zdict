import time
from pytest import raises
from unittest.mock import Mock, patch

from zdict.exceptions import NotFoundError
from zdict.zdict import get_args
from zdict.dictionaries.itaigi import iTaigiDict


class TestiTaigiDict:
    @classmethod
    def setup_class(cls):
        cls.dict = iTaigiDict(get_args())

        cls.words = ['芭樂', '測試']

        # Set query_timeout from 5 seconds to 60 seconds,
        # so it won't timeout that often.
        cls.dict.args.query_timeout = 60
        # Setup normal query data
        cls.dict.args.verbose = False
        cls.records = []
        for word in cls.words:
            record = None
            while True:
                try:
                    record = cls.dict.query(word)
                except Exception:
                    # prevent itaigi API 500 error
                    time.sleep(5)
                    continue
                else:
                    cls.records.append(record)
                    break

        # Setup verbose query data
        cls.dict.args.verbose = True
        cls.verbose_records = []
        for word in cls.words:
            record = None
            while True:
                try:
                    record = cls.dict.query(word)
                except Exception:
                    # prevent itaigi API 500 error
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
        del cls.records
        del cls.verbose_records

    def test_provider(self):
        assert self.dict.provider == 'itaigi'

    def test_title(self):
        assert self.dict.title == 'iTaigi - 愛台語'

    def test__get_url(self):
        # Change url for the new dict and delete this comment
        url = 'https://itaigi.tw/平臺項目列表/揣列表?關鍵字=芭樂'
        assert url == self.dict._get_url('芭樂')

    def test_show(self):
        # god bless this method, hope that it do not raise any exception
        self.dict.args.verbose = False

        for record in self.records:
            self.dict.show(record)

    def test_show_verbose(self):
        # god bless this method, hope that it do not raise any exception
        self.dict.args.verbose = True

        for record in self.verbose_records:
            self.dict.show(record)

    @patch('zdict.dictionaries.itaigi.Record')
    def test_query_normal(self, Record):
        self.dict.args.verbose = False

        for i, word in enumerate(self.words):
            while True:
                try:
                    self.dict.query(word)
                except Exception:
                    # prevent itaigi API 500 error
                    time.sleep(5)
                    continue
                else:
                    Record.assert_called_with(
                        word=word,
                        content=self.records[i].content,
                        source='itaigi',
                    )
                    break

    @patch('zdict.dictionaries.itaigi.Record')
    def test_query_verbose(self, Record):
        self.dict.args.verbose = True

        for i, word in enumerate(self.words):
            while True:
                try:
                    self.dict.query(word)
                except Exception:
                    # prevent itaigi API 500 error
                    time.sleep(5)
                    continue
                else:
                    Record.assert_called_with(
                        word=word,
                        content=self.verbose_records[i].content,
                        source='itaigi',
                    )
                    break

    def test_query_not_found(self):
        self.dict._get_raw = Mock(return_value='{"列表": []}')
        with raises(NotFoundError):
            self.dict.query(self.words[0])
        self.dict._get_raw.assert_called_with(self.words[0])
