from pytest import raises
from unittest.mock import Mock, patch

from zdict.dictionaries.moe import MoeDict, MoeDictTaiwanese
from zdict.exceptions import NotFoundError, QueryError
from zdict.models import Record
from zdict.zdict import get_args


class TestMoeDict:
    def setup_method(self, method):
        self.dict = MoeDict(get_args())

    def teardown_method(self, method):
        del self.dict

    def test__get_url(self):
        assert 'https://www.moedict.tw/uni/萌' == self.dict._get_url('萌')

    def test_provider(self):
        assert self.dict.provider == 'moe'

    def test_query_timeout(self):
        self.dict._get_raw = Mock(side_effect=QueryError('萌', 404))

        with raises(NotFoundError):
            self.dict.query('萌')

        self.dict._get_raw.assert_called_with('萌')

    @patch('zdict.dictionaries.moe.Record')
    def test_query_normal(self, Record):
        self.dict._get_raw = Mock(return_value='{}')
        self.dict.query('萌')
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


class TestMoeDictTaiwanese:
    def setup_method(self, method):
        self.dict = MoeDictTaiwanese(get_args())

    def teardown_method(self, method):
        del self.dict

    def test__get_url(self):
        assert 'https://www.moedict.tw/t/木耳.json' == self.dict._get_url('木耳')

    def test_provider(self):
        assert self.dict.provider == 'moe-taiwanese'

    def test_query_timeout(self):
        self.dict._get_raw = Mock(side_effect=QueryError('木耳', 404))

        with raises(NotFoundError):
            self.dict.query('木耳')

        self.dict._get_raw.assert_called_with('木耳')

    @patch('zdict.dictionaries.moe.Record')
    def test_query_normal(self, Record):
        self.dict._get_raw = Mock(return_value='{}')
        self.dict.query('木耳')
        Record.assert_called_with(word='木耳',
                                  content='{}',
                                  source='moe-taiwanese')

    def test_show(self):
        content = '''
        {
            "h": [{
                "T": "bo̍k-ní",
                "_": "928",
                "d": [{
                    "f": "蕈`菇~`類~。`生長~`在~`朽~`腐~`的~`樹~`幹~`上~ ...",
                    "type": "`名~"
                }]
            }],
            "t": "`木~`耳~"
        }
        '''
        r = Record(word='木耳', content=content, source=self.dict.provider)

        # god bless this method, hope that it do not raise any exception
        self.dict.show(r)
