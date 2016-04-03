import json
import os

from pytest import raises
from unittest.mock import Mock, patch

from zdict.dictionaries.spanish import SpanishDict
from zdict.exceptions import NotFoundError
from zdict.models import Record


RAW_HTML_TEST_DATA = os.path.join(os.path.dirname(__file__), 'testdata.html')
CONTENT_TEST_DATA = os.path.join(os.path.dirname(__file__), 'content.json')


class TestSpansishDict:
    def setup_method(self, method):
        self.dict = SpanishDict()
        self.word = 'Spanish'
        self.timeout = 5
        with open(CONTENT_TEST_DATA, 'r') as f:
            self.content = f.read()
        with open(RAW_HTML_TEST_DATA, 'r') as f:
            self.raw_html = f.read()

    def teardown_method(self, method):
        del self.dict

    def test_provider(self):
        assert self.dict.provider == 'spanish'

    def test_title(self):
        assert self.dict.title == 'SpanishDict'

    def test__get_url(self):
        url = 'http://www.spanishdict.com/translate/{}'.format(self.word)
        assert url == self.dict._get_url(self.word)

    def test_show(self):
        content = self.content
        r = Record(word=self.word, content=content, source=self.dict.provider)

        # god bless this method, hope that it do not raise any exception
        self.dict.show(r)

    @patch('zdict.dictionaries.spanish.Record')
    def test_query_normal(self, Record):
        self.dict._get_raw = Mock(return_value=self.raw_html)
        self.dict.query(self.word, self.timeout)
        Record.assert_called_with(
            word=self.word,
            content=json.dumps(json.loads(self.content)),
            source='spanish',
        )

    def test_query_not_found(self):
        self.dict._get_raw = Mock(return_value='<div class="card"><div/>')
        with raises(NotFoundError):
            self.dict.query(self.word, self.timeout)
        self.dict._get_raw.assert_called_with(self.word, self.timeout)
