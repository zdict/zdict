import unittest

from ..ydict import yDict


class yDictTestCase(unittest.TestCase):
    def setUp(self):
        self.ydcit = yDict()

    def test__get_url(self):
        self.assertEqual(
            'https://tw.dictionary.yahoo.com/dictionary?p=test',
            self.ydcit._get_url('test')
        )
