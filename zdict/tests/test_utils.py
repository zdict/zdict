from ..utils import (Color, create_zdict_db_if_not_exists,
                     create_zdict_dir_if_not_exists)
from pytest import raises
from unittest.mock import patch


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


@patch('zdict.utils.constants')
@patch('os.mkdir')
@patch('os.path.isdir', return_value=False)
def test_create_zdict_dir_if_not_exists(mkdir, isdir, constants):
    constants.BASE_DIR = '/mock'
    create_zdict_dir_if_not_exists()

    isdir.assert_called_with('/mock')
    mkdir.assert_called_with('/mock')


@patch('builtins.open')
@patch('zdict.utils.constants')
@patch('os.path.exists', return_value=False)
def test_create_zdict_db_if_not_exists(exists, constants, open):
    constants.DB_FILE = '/mock'
    create_zdict_db_if_not_exists()

    exists.assert_called_with('/mock')
    assert open.called
