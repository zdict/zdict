import argparse
import locale
import sys

from .exceptions import EncodingError


__all__ = ('main',)


def load_option() -> dict:
    '''
    Option source has following priority:
        1. command line args
            ``parse_option``
        2. user config file
            ``get_default_config``
        3. default option
            ``get_default_config``
    '''
    cl_args = parse_option()
    user_conf = get_user_config()
    default_conf = get_default_config()

    def merge(*args) -> dict:
        '''
        Note the position is treated as the priority.
        '''
        ...

    return merge(cl_args, user_conf, default_conf)


def parse_option() -> dict:
    ...


def get_default_config() -> dict:
    ...


def get_user_config() -> dict:
    ...


def dispatcher(options: dict, db):
    ...


def init_db():
    ...


def close_db(db):
    ...


def main():
    '''
    Basic task:
        1. check environment encoding
        #. load option
        #. init sqlite db
        #. dispatch
    '''
    # Check user's encoding
    try:
        lang, enc = locale.getdefaultlocale()
        if enc != "UTF-8":
            raise EncodingError()
    except ValueError as e:
        print("Didn't detect your LC_ALL environment variable.")
        print("Please export LC_ALL with some UTF-8 encoding.")
        sys.exit(-1)
    except EncodingError as e:
        print("zdict only works with encoding=UTF-8, ")
        print("but you encoding is: {} {}".format(lang, enc))
        print("Please export LC_ALL with some UTF-8 encoding.")
        sys.exit(e.errno)

    dispatcher(load_option(), init_db())
