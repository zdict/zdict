from ...dictionaries.moe import MoeDict


class TestyDict:
    def setup_method(self, method):
        self.dict = MoeDict()

    def teardown_method(self, method):
        del self.dict

    def test__get_url(self):
        assert 'https://www.moedict.tw/uni/萌', self.dict._get_url('萌')
