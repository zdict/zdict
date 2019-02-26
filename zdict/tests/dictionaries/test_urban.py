from pytest import raises
from unittest.mock import patch

from zdict.dictionaries.urban import UrbanDict
from zdict.exceptions import NotFoundError
from zdict.zdict import get_args


class TestUrbanDict:
    @classmethod
    def setup_class(cls):
        cls.dict = UrbanDict(get_args())
        cls.not_found_word = 'some_not_existing_word'
        cls.word = 'urban'
        cls.record = cls.dict.query(cls.word)

    @classmethod
    def teardown_class(cls):
        del cls.dict
        del cls.not_found_word
        del cls.word
        del cls.record

    def test_provider(self):
        assert self.dict.provider == 'urban'

    def test__get_url(self):
        uri = 'http://api.urbandictionary.com/v0/define?term=mock'
        assert self.dict._get_url('mock') == uri

    def test_query_not_found(self):
        with raises(NotFoundError):
            self.dict.query(self.not_found_word)

    @patch('zdict.dictionaries.urban.Record')
    def test_query_normal(self, Record):
        self.dict.query(self.word)
        Record.assert_called_with(
            word=self.word,
            content=self.record.content,
            source='urban',
        )

    def test_show(self):
        # god bless this method, hope that it do not raise any exception
        self.dict.show(self.record)
