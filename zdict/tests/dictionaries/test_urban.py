from ...dictionaries.urban import UrbanDict
from ...exceptions import NotFoundError
from ...models import Record

from pytest import raises
from unittest.mock import Mock, patch


class TestUrbanDict:
    def setup_method(self, method):
        self.dict = UrbanDict()

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
            self.dict.query('mock', timeout=666)

        self.dict._get_raw.assert_called_with('mock', 666)

    @patch('zdict.dictionaries.urban.Record')
    def test_query_normal(self, Record):
        self.dict._get_raw = Mock(return_value='{"mock": true}')

        r = self.dict.query('mock', timeout=666)

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
