from pytest import raises
from unittest.mock import Mock, patch

from zdict.exceptions import NotFoundError
from zdict.dictionaries.yahoo import YahooDict
from zdict.zdict import get_args


class TestyDict:
    @classmethod
    def setup_class(cls):
        cls.dict = YahooDict(get_args())
        cls.words = ['style', 'metadata', 'apples', 'google', 'hold on']
        cls.records = [cls.dict.query(word) for word in cls.words]

    @classmethod
    def teardown_class(cls):
        del cls.dict
        del cls.words
        del cls.records

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

        for record in self.records:
            self.dict.show(record)

    def test_show_verbose(self):
        # god bless this method, hope that it do not raise any exception
        self.dict.args.verbose = True

        for record in self.records:
            self.dict.show(record)

    @patch('zdict.dictionaries.yahoo.Record')
    def test_query_normal(self, Record):
        self.dict.args.verbose = False

        for i, word in enumerate(self.words):
            self.dict.query(word)
            Record.assert_called_with(
                word=word,
                content=self.records[i].content,
                source='yahoo',
            )

    @patch('zdict.dictionaries.yahoo.Record')
    def test_query_verbose(self, Record):
        self.dict.args.verbose = True

        for i, word in enumerate(self.words):
            self.dict.query(word)
            Record.assert_called_with(
                word=word,
                content=self.records[i].content,
                source='yahoo',
            )

    def test_query_not_found(self):
        self.dict._get_raw = Mock(return_value='{"data": []}')
        with raises(NotFoundError):
            self.dict.query(self.words[0])
        self.dict._get_raw.assert_called_with(self.words[0])
