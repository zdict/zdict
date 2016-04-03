from zdict.loader import _is_dict, get_dictionary_map
from zdict.dictionary import DictBase

from unittest.mock import MagicMock, Mock, patch


@patch('builtins.issubclass', return_value=True)
def test__is_dict_normal(issubclass_):
    assert _is_dict(Mock) is True
    issubclass_.assert_called_with(Mock, DictBase)


@patch('builtins.issubclass', return_value=True)
def test__is_dict_DictBase(issubclass_):
    assert _is_dict(DictBase) is False
    issubclass_.assert_called_with(DictBase, DictBase)


@patch('builtins.issubclass', side_effect=TypeError)
def test__is_dict_not_class(issubclass_):
    import sys

    assert _is_dict(sys) is False
    issubclass_.called


@patch('zdict.loader.getmembers')
@patch('zdict.loader.import_module', return_value='mock')
@patch('zdict.loader.os.listdir')
def test_get_dictionary_map(listdir, import_module, getmembers):
    # prepare mocked return value
    MockDict = MagicMock(name='MockDict')
    MockDict().provider = 'mock'
    listdir.return_value = [
        '__init__.py',
        '_strange.py',
        'mock.py',
        'template.py',  # the excluded files
        'not_a_py.rst',
    ]
    getmembers.return_value = [('mock', MockDict)]

    dict_map = get_dictionary_map()

    assert dict_map == {'mock': MockDict}
    assert listdir.called
    import_module.assert_called_with('zdict.dictionaries.mock')
    assert import_module.call_count == 1
    getmembers.assert_called_with('mock', predicate=_is_dict)
    assert MockDict.called
