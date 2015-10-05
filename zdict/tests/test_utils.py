from ..utils import Color
from pytest import raises


class TestColor:
    def setup_method(self, method):
        self.color = Color()

    def teardown_method(self, method):
        del self.color

    def test_format(self):
        assert '\33[31;1mtest\33[0m', self.color.format('test', 'lred')
        assert '\33[31mtest\33[0m', self.color.format('test', 'red')
        assert '  \33[31mtest\33[0m', self.color.format('test', 'red', indent=2)

    def test_attribute(self):
        self.color.red = '\33[31m'
        self.color.lred = '\33[31;1m'
        with raises(AttributeError):
            self.color.test
