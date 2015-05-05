import unittest

from ..dictionaries import DictBase


class MockDict(DictBase):
    @property
    def selectors(self):
        ...

    @property
    def provider(self):
        ...

    @property
    def _get_prompt(self):
        ...


class TestDict(unittest.TestCase):
    def setUp(self):
        self.dictionary = MockDict()

    def test__expand_selectors(self):
        d = {
            'div.a': [
                'span',
                'p',
            ],
            'ul': 'a',
        }
        res = self.dictionary._expand_selectors(d)
        self.assertEqual(res, ('div.a span', 'div.a p', 'ul a'))

        l = ['div', 'span', 'p']
        res = self.dictionary._expand_selectors(l)
        self.assertEqual(res, tuple(l))

        l = [{'div': 'p'}]
        res = self.dictionary._expand_selectors(l)
        self.assertEqual(res, ('div p',))
