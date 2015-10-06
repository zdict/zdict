from ...dictionaries.moe import MoeDict
from ...exceptions import NotFoundError, QueryError
from ...models import Record

from pytest import raises
from unittest.mock import Mock, patch


class TestyDict:
    def setup_method(self, method):
        self.dict = MoeDict()

    def teardown_method(self, method):
        del self.dict

    def test__get_url(self):
        assert 'https://www.moedict.tw/uni/萌' == self.dict._get_url('萌')

    def test_provider(self):
        assert self.dict.provider == 'moe'

    def test_query_timeout(self):
        self.dict._get_raw = Mock(side_effect=QueryError('萌', 1))

        with raises(NotFoundError):
            self.dict.query('萌', timeout=666)

        self.dict._get_raw.assert_called_with('萌', 666)

    @patch('zdict.dictionaries.moe.Record')
    def test_query_normal(self, Record):
        self.dict._get_raw = Mock(return_value='{}')

        record = self.dict.query('萌', timeout=666)

        Record.assert_called_with(word='萌', content='{}', source='moe')


    def test_show(self):
        content = '''
        {
            "heteronyms": [{
                "bopomofo": "ㄧㄢˋ",
                "bopomofo2": "yàn",
                "definitions": [{
                    "def": "假的、偽造的。",
                    "example": ["如：「贗品」。"],
                    "quote": ["..."],
                    "type": "形",
                    "synonyms": "尛",
                    "antonyms": "萌"
                }], 
                "pinyin": "yàn"
            }],
            "non_radical_stroke_count": 15,
            "radical": "貝",
            "stroke_count": 22,
            "title": "贗"
        }
        '''
        r = Record(word='贗', content=content, source=self.dict.provider)

        # god bless this method, hope that it do not raise any exception
        self.dict.show(r)
