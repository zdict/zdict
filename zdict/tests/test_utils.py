import unittest

from ..utils import Color


class TestColor(unittest.TestCase):
    def setUp(self):
        self.color = Color()

    def test_format(self):
        self.assertEqual(
            '\33[31;1mtest\33[0m',
            self.color.format('test', 'lred')
        )
        self.assertEqual(
            '\33[31mtest\33[0m',
            self.color.format('test', 'red')
        )
        self.assertEqual(
            '  \33[31mtest\33[0m',
            self.color.format('test', 'red', indent=2)
        )

    def test_attribute(self):
        self.color.red = '\33[31m'
        self.color.lred = '\33[31;1m'
        with self.assertRaises(AttributeError):
            self.color.test
