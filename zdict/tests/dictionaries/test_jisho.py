import json
from unittest.mock import Mock

from pytest import raises

from zdict.dictionaries.jisho import JishoDict
from zdict.exceptions import NotFoundError
from zdict.zdict import get_args


class TestJishoDict:
    @classmethod
    def setup_class(cls):
        cls.dict = JishoDict(get_args())
        cls.word = 'bird'
        cls.source = 'jisho'
        cls.record = cls.dict.query(cls.word)

    @classmethod
    def teardown_class(cls):
        del cls.dict
        del cls.source
        del cls.word
        del cls.record

    def test_provider(self):
        assert self.dict.provider == 'jisho'

    def test_title(self):
        assert self.dict.title == 'Jisho'

    def test__get_url(self):
        url = (
            'https://jisho.org/api/v1/search/words?keyword={}'
        ).format(self.word)
        assert url == self.dict._get_url(self.word)

    def test_show(self):
        # god bless this method, hope that it do not raise any exception
        self.dict.args.verbose = False
        self.dict.show(self.record)

    def test_show_verbose(self):
        # god bless this method, hope that it do not raise any exception
        self.dict.args.verbose = True
        self.dict.show(self.record)

    def test_query_normal(self):
        self.dict.args.verbose = False
        record = self.dict.query(self.word)

        cls_record_content_dict = json.loads(self.record.content)
        cls_record_content_dict['data'].sort(
            key=lambda datum: datum.get('slug')
        )
        record_content_dict = json.loads(record.content)
        record_content_dict['data'].sort(key=lambda datum: datum.get('slug'))

        assert record_content_dict == cls_record_content_dict
        assert record.word == self.word
        assert record.source == self.source

    def test_query_verbose(self):
        self.dict.args.verbose = True
        record = self.dict.query(self.word)

        cls_record_content_dict = json.loads(self.record.content)
        cls_record_content_dict['data'].sort(
            key=lambda datum: datum.get('slug')
        )
        record_content_dict = json.loads(record.content)
        record_content_dict['data'].sort(key=lambda datum: datum.get('slug'))
        assert record_content_dict == cls_record_content_dict

        assert record.word == self.word
        assert record.source == self.source

    def test_query_not_found(self):
        self.dict._get_raw = Mock(return_value='{"data": []}')
        with raises(NotFoundError):
            self.dict.query(self.word)
        self.dict._get_raw.assert_called_with(self.word)
