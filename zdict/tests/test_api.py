from unittest.mock import patch, Mock

from zdict.api import dump


@patch('zdict.api.Record')
def test_dump(Record):
    # Assume our db contains following words
    Record.select.return_value = [
        Mock(word='apple'),
        Mock(word='apply')]

    # init query
    ret = dump()
    assert ret == ['apple', 'apply']

    ret = dump(pattern='^.*e$')
    assert ret == ['apple']
