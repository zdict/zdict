from pytest import raises
from unittest.mock import Mock, patch

from ...dictionaries.jisho import JishoDict
from ...exceptions import NotFoundError, QueryError
from ...models import Record


class TestJishoDict:
    def setup_method(self, method):
        self.dict = JishoDict()

    def teardown_method(self, method):
        del self.dict

    def test__get_url(self):
        url = 'http://jisho.org/api/v1/search/words?keyword=辞書'
        assert url == self.dict._get_url('辞書')
