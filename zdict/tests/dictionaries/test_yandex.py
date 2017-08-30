from pytest import raises
from unittest.mock import Mock, patch

from zdict.dictionaries.yandex import YandexDict, API_KEY
from zdict.exceptions import NotFoundError, QueryError
from zdict.models import Record
from zdict.zdict import get_args


class TestYandexDict:
    def setup_method(self, method):
        self.dict = YandexDict(get_args())

    def teardown_method(self, method):
        del self.dict

    def test__get_url(self):
        url = 'https://translate.yandex.net/api/v1.5/tr.json/translate?' \
              'key={}&text=дом&lang=ru-en'
        assert url.format(API_KEY) == self.dict._get_url('дом')

    def test_provider(self):
        assert self.dict.provider == 'yandex'

    def test_query_timeout(self):
        self.dict._get_raw = Mock(side_effect=QueryError('дом', 404))

        with raises(NotFoundError):
            self.dict.query('дом')

        self.dict._get_raw.assert_called_with('дом')

    @patch('zdict.dictionaries.yandex.Record')
    def test_query_normal(self, Record):
        content = '{"code":200,"lang":"ru-en","text":["house"]}'
        self.dict._get_raw = Mock(return_value=content)
        self.dict.query('дом')
        Record.assert_called_with(word='дом', content=content, source='yandex')

    def test_show(self):
        content = '''
        {
            "code": 200,
            "lang": "ru-en",
            "text": ["house"]
        }
        '''
        r = Record(word='дом', content=content, source=self.dict.provider)

        # god bless this method, hope that it do not raise any exception
        self.dict.show(r)
