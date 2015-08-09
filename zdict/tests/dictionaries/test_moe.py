import unittest

from ...dictionaries import moe


class TestyDict(unittest.TestCase):
    def setUp(self):
        self.dict = moe()

    def test__get_url(self):
        self.assertEqual(
            'https://www.moedict.tw/uni/萌',
            self.dict._get_url('萌')
        )
