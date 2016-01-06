import sys

from ..easter_eggs import (import_pyjokes_module, get_pyjoke)

from pytest import raises
from unittest.mock import patch


def test_import_pyjokes_module():
    with patch('importlib.util.find_spec', return_value=None):
        assert import_pyjokes_module() == None

    assert import_pyjokes_module().__name__ == 'pyjokes'


def test_get_pyjoke():
    import pyjokes
    with patch('pyjokes.get_jokes', return_value=['test']):
        assert get_pyjoke(pyjokes, 'test').content == 'test'
