from .. import zdict

from pytest import raises
from unittest.mock import patch


@patch('zdict.zdict.execute_zdict')
@patch('zdict.zdict.user_set_encoding_and_is_utf8', return_value=False)
def test_main_encoding_error(check_encode, execute_zdict):
    with raises(SystemExit):
        zdict.main()

    assert not execute_zdict.called


@patch('zdict.zdict.execute_zdict')
@patch('zdict.zdict.set_args')
@patch('zdict.zdict.get_args')
@patch('zdict.zdict.check_zdict_dir_and_db')
@patch('zdict.zdict.user_set_encoding_and_is_utf8', return_value=True)
def test_main_normal(check_encode, check_zdict_dir_and_db,
                     get_args, set_args, execute_zdict):
    zdict.main()

    assert check_encode.called
    assert check_zdict_dir_and_db.called
    assert get_args.called
    assert set_args.called
    assert execute_zdict.called
