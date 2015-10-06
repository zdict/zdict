from ...dictionaries.yahoo import YahooDict


class TestyDict:
    def setup_method(self, method):
        self.dict = YahooDict()

    def teardown_method(self, method):
        del self.dict

    def test__get_url(self):
        url = 'https://tw.dictionary.search.yahoo.com/search?p=test'
        assert url == self.dict._get_url('test')
