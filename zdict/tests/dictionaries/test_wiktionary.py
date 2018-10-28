from pytest import raises
from unittest.mock import Mock, patch
import json

from zdict.dictionaries.wiktionary import WiktionaryDict
from zdict.exceptions import NotFoundError, QueryError
from zdict.models import Record
from zdict.zdict import get_args


class TestWiktionaryDict:
    def setup_method(self, method):
        self.dict = WiktionaryDict(get_args())

    def teardown_method(self, method):
        del self.dict

    def test_provider(self):
        assert self.dict.provider == 'wiktionary'

    def test__get_url(self):
        uri = 'https://en.wiktionary.org/api/rest_v1/page/definition/mock'
        assert self.dict._get_url('mock') == uri

    def test_query_notfound(self):
        self.dict._get_raw = Mock(side_effect=QueryError('mock', 404))

        with raises(NotFoundError):
            self.dict.query('mock')

        self.dict._get_raw.assert_called_with('mock')

    @patch('zdict.dictionaries.wiktionary.Record')
    def test_query_normal(self, Record):
        content = '''
        {"en":[{"partOfSpeech":"part_of_speech",
        "definitions":[{"definition":"definition","examples":["example"]}]}]}
        '''
        self.dict._get_raw = Mock(return_value=content)
        self.dict.query('mock')
        r_content = [{"part_of_speech": "part_of_speech",
                      "definitions": [{"definition": "definition",
                                       "examples": ["example"]}]}]
        Record.assert_called_with(
            word='mock',
            content=json.dumps(r_content),
            source='wiktionary'
        )

    def test_show(self):
        content = '''
        [{"part_of_speech":"part_of_speech",
        "definitions":[{"definition": "definition","examples":["example"]}]}]
        '''

        r = Record(word="string",
                   content=content,
                   source=self.dict.provider)
        self.dict.show(r)
