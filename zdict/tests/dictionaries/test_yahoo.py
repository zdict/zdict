import unittest

from ...dictionaries import yahoo


class TestyDict(unittest.TestCase):
    def setUp(self):
        self.dict = yahoo()

    def test__get_url(self):
        self.assertEqual(
            'https://tw.dictionary.yahoo.com/dictionary?p=test',
            self.dict._get_url('test')
        )
