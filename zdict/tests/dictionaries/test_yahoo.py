from pytest import raises
from unittest.mock import Mock, patch

from zdict.exceptions import NotFoundError
from zdict.dictionaries.yahoo import YahooDict
from zdict.zdict import get_args


class TestyDict:
    @classmethod
    def setup_class(cls):
        cls.dict = YahooDict(get_args())
        cls.word = 'style'
        cls.record = cls.dict.query(cls.word)

    @classmethod
    def teardown_class(cls):
        del cls.dict
        del cls.word
        del cls.record

    def test_provider(self):
        assert self.dict.provider == 'yahoo'

    def test_title(self):
        assert self.dict.title == 'Yahoo Dictionary'

    def test__get_url(self):
        url = 'https://tw.dictionary.yahoo.com/dictionary?p=test'
        assert url == self.dict._get_url('test')

    def test_show(self):
        # god bless this method, hope that it do not raise any exception
        self.dict.args.verbose = False
        self.dict.show(self.record)

    def test_show_verbose(self):
        # god bless this method, hope that it do not raise any exception
        self.dict.args.verbose = True
        self.dict.show(self.record)

    @patch('zdict.dictionaries.yahoo.Record')
    def test_query_normal(self, Record):
        self.dict.args.verbose = False
        self.dict.query(self.word)
        Record.assert_called_with(
            word=self.word,
            content=self.record.content,
            source='yahoo',
        )

    @patch('zdict.dictionaries.yahoo.Record')
    def test_query_verbose(self, Record):
        self.dict.args.verbose = True
        self.dict.query(self.word)
        Record.assert_called_with(
            word=self.word,
            content=self.record.content,
            source='yahoo',
        )

    def test_query_not_found(self):
        self.dict._get_raw = Mock(return_value='{"data": []}')
        with raises(NotFoundError):
            self.dict.query(self.word)
        self.dict._get_raw.assert_called_with(self.word)
