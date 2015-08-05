import unittest

from ...plugins import YahooDict


class TestyDict(unittest.TestCase):
    def setUp(self):
        self.ydict = YahooDict()

    def test__get_url(self):
        self.assertEqual(
            'https://tw.dictionary.yahoo.com/dictionary?p=test',
            self.ydict._get_url('test')
        )
