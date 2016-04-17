from pytest import raises
from unittest.mock import Mock, patch

from zdict.dictionaries.urban import UrbanDict
from zdict.exceptions import NotFoundError
from zdict.models import Record
from zdict.zdict import get_args


class TestUrbanDict:
    def setup_method(self, method):
        self.dict = UrbanDict(get_args())

    def teardown_method(self, method):
        del self.dict

    def test_provider(self):
        assert self.dict.provider == 'urban'

    def test__get_url(self):
        uri = 'http://api.urbandictionary.com/v0/define?term=mock'
        assert self.dict._get_url('mock') == uri

    def test_query_notfound(self):
        notfound_payload = '''
            {"tags":[],"result_type":"no_results","list":[],"sounds":[]}
        '''
        self.dict._get_raw = Mock(return_value=notfound_payload)

        with raises(NotFoundError):
            self.dict.query('mock')

        self.dict._get_raw.assert_called_with('mock')

    @patch('zdict.dictionaries.urban.Record')
    def test_query_normal(self, Record):
        self.dict._get_raw = Mock(return_value='{"mock": true}')
        self.dict.query('mock')
        Record.assert_called_with(
            word='mock',
            content='{"mock": true}',
            source='urban'
        )

    def test_show(self):
        content = '''
        {
            "list": [
                {
                    "word": "mock",
                    "definition": "Mock",
                    "example": "..."
                }
            ]
        }
        '''
        r = Record(word='mock', content=content, source='urban')

        # god bless this method, hope that it do not raise any exception
        self.dict.show(r)
