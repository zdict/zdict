from pytest import raises
from unittest.mock import Mock, patch

from zdict.dictionaries.jisho import JishoDict
from zdict.exceptions import NotFoundError


class TestJishoDict:
    @classmethod
    def setup_class(cls):
        cls.dict = JishoDict()
        cls.word = 'apple'
        cls.timeout = 5
        cls.verbose = True
        cls.record = cls.dict.query(cls.word, cls.timeout, cls.verbose)

    @classmethod
    def teardown_class(cls):
        del cls.dict
        del cls.word
        del cls.timeout
        del cls.verbose
        del cls.record

    def test_provider(self):
        assert self.dict.provider == 'jisho'

    def test_title(self):
        assert self.dict.title == 'Jisho'

    def test__get_url(self):
        url = (
            'http://jisho.org/api/v1/search/words?keyword={}'
        ).format(self.word)
        assert url == self.dict._get_url(self.word)

    def test_show(self):
        # god bless this method, hope that it do not raise any exception
        self.dict.show(self.record)

    def test_show_verbose(self):
        # god bless this method, hope that it do not raise any exception
        self.dict.show(self.record, self.verbose)

    @patch('zdict.dictionaries.jisho.Record')
    def test_query_normal(self, Record):
        self.dict.query(self.word, self.timeout)
        Record.assert_called_with(
            word=self.word,
            content=self.record.content,
            source='jisho',
        )

    @patch('zdict.dictionaries.jisho.Record')
    def test_query_verbose(self, Record):
        self.dict.query(self.word, self.timeout, self.verbose)
        Record.assert_called_with(
            word=self.word,
            content=self.record.content,
            source='jisho',
        )

    def test_query_not_found(self):
        self.dict._get_raw = Mock(return_value='{"data": []}')
        with raises(NotFoundError):
            self.dict.query(self.word, self.timeout)
        self.dict._get_raw.assert_called_with(self.word, self.timeout)
