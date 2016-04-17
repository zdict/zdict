from pytest import raises
from unittest.mock import Mock, patch

from zdict.dictionaries.spanish import SpanishDict
from zdict.exceptions import NotFoundError
from zdict.zdict import get_args


class TestSpanishDict:
    @classmethod
    def setup_class(cls):
        cls.dict = SpanishDict(get_args())
        cls.word = 'Spanish'
        cls.record = cls.dict.query(cls.word)

    @classmethod
    def teardown_class(cls):
        del cls.dict
        del cls.word
        del cls.record

    def test_provider(self):
        assert self.dict.provider == 'spanish'

    def test_title(self):
        assert self.dict.title == 'SpanishDict'

    def test__get_url(self):
        url = 'http://www.spanishdict.com/translate/{}'.format(self.word)
        assert url == self.dict._get_url(self.word)

    def test_show(self):
        # god bless this method, hope that it do not raise any exception
        self.dict.show(self.record)

    @patch('zdict.dictionaries.spanish.Record')
    def test_query_normal(self, Record):
        self.dict.query(self.word)
        Record.assert_called_with(
            word=self.word,
            content=self.record.content,
            source='spanish',
        )

    def test_query_not_found(self):
        self.dict._get_raw = Mock(return_value='<div class="card"><div/>')
        with raises(NotFoundError):
            self.dict.query(self.word)
        self.dict._get_raw.assert_called_with(self.word)
