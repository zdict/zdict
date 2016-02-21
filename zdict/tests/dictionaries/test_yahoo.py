from ...dictionaries.yahoo import YahooDict
from ...utils import check_zdict_dir_and_db


class TestyDict:
    def setup_method(self, method):
        check_zdict_dir_and_db()
        self.dict = YahooDict()

    def teardown_method(self, method):
        del self.dict

    def test__get_url(self):
        url = 'https://tw.dictionary.search.yahoo.com/search?p=test'
        assert url == self.dict._get_url('test')
