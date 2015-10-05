from ...dictionaries import moe


class TestyDict:
    def setup_method(self, method):
        self.dict = moe()

    def teardown_method(self, method):
        del self.dict

    def test__get_url(self):
        assert 'https://www.moedict.tw/uni/萌', self.dict._get_url('萌')
