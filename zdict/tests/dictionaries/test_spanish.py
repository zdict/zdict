from pytest import raises
from unittest.mock import patch

from zdict.dictionaries.spanish import SpanishDict
from zdict.exceptions import NotFoundError
from zdict.zdict import get_args


class TestSpanishDict:
    @classmethod
    def setup_class(cls):
        cls.dict = SpanishDict(get_args())
        cls.en_word = 'Spanish'
        cls.en_record = cls.dict.query(cls.en_word)
        cls.es_word = 'tranquilo'
        cls.es_record = cls.dict.query(cls.es_word)
        cls.not_found_word = 'asdfsdf'

    @classmethod
    def teardown_class(cls):
        del cls.dict
        del cls.en_word
        del cls.en_record
        del cls.es_word
        del cls.es_record
        del cls.not_found_word

    def test_provider(self):
        assert self.dict.provider == 'spanish'

    def test_title(self):
        assert self.dict.title == 'SpanishDict'

    def test__get_url(self):
        url = 'https://www.spanishdict.com/translate/{}'.format(self.en_word)
        assert url == self.dict._get_url(self.en_word)

        url = 'https://www.spanishdict.com/translate/{}'.format(self.es_word)
        assert url == self.dict._get_url(self.es_word)

    def test_show(self):
        # god bless this method, hope that it do not raise any exception
        self.dict.show(self.en_record)
        self.dict.show(self.es_record)

    @patch('zdict.dictionaries.spanish.Record')
    def test_query_normal(self, Record):
        self.dict.query(self.en_word)
        Record.assert_called_with(
            word=self.en_word,
            content=self.en_record.content,
            source='spanish',
        )

        self.dict.query(self.es_word)
        Record.assert_called_with(
            word=self.es_word,
            content=self.es_record.content,
            source='spanish',
        )

    def test_query_not_found(self):
        with raises(NotFoundError):
            self.dict.query(self.not_found_word)
