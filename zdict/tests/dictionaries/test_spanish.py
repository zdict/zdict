from pytest import raises
from unittest.mock import Mock, patch

from zdict.dictionaries.spanish import SpanishDict
from zdict.exceptions import NotFoundError


class TestSpansishDict:
    @classmethod
    def setup_class(cls):
        cls.d = SpanishDict()
        cls.word = 'Spanish'
        cls.timeout = 5
        cls.record = cls.d.query(cls.word, cls.timeout)

    @classmethod
    def teardown_class(cls):
        del cls.d
        del cls.word
        del cls.timeout
        del cls.record

    def test_provider(self):
        assert self.d.provider == 'spanish'

    def test_title(self):
        assert self.d.title == 'SpanishDict'

    def test__get_url(self):
        url = 'http://www.spanishdict.com/translate/{}'.format(self.word)
        assert url == self.d._get_url(self.word)

    def test_show(self):
        # god bless this method, hope that it do not raise any exception
        self.d.show(self.record)

    @patch('zdict.dictionaries.spanish.Record')
    def test_query_normal(self, Record):
        self.d.query(self.word, self.timeout)
        Record.assert_called_with(
            word=self.word,
            content=self.record.content,
            source='spanish',
        )

    def test_query_not_found(self):
        self.d._get_raw = Mock(return_value='<div class="card"><div/>')
        with raises(NotFoundError):
            self.d.query(self.word, self.timeout)
        self.d._get_raw.assert_called_with(self.word, self.timeout)
