from pytest import raises
from unittest.mock import patch, Mock

from zdict.completer import DictCompleter


@patch('zdict.completer.db')
def test_DictCompleter_db_connect(db):
    '''
    Test case for DictCompleter init/del

    DictCompleter will connect to db when __init__,
    and close db when __del__.
    '''
    # init
    completer = DictCompleter()
    assert db.connect.called

    # del
    del completer
    assert db.close.called


@patch('zdict.completer.Record')
@patch('zdict.completer.db')
def test_DictCompleter_complete(db, Record):
    '''
    Test case for DictCompleter.complete implemented with iterator
    '''
    # Assume our db contains following words
    Record.select().where.return_value = [
        Mock(word='apple'),
        Mock(word='apply')]

    completer = DictCompleter()

    # init query
    ret = completer.complete('a', state=0)
    assert ret == 'apple'

    ret = completer.complete('a', state=1)
    assert ret == 'apply'

    with raises(StopIteration):
        completer.complete('a', state=2)
