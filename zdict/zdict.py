import locale

from argparse import ArgumentParser

from . import constants, utils
from .completer import DictCompleter
from .loader import get_dictionary_map
from .utils import readline


def check_zdict_dir_and_db():
    utils.create_zdict_dir_if_not_exists()
    utils.create_zdict_db_if_not_exists()


def user_set_encoding_and_is_utf8():
    # Check user's encoding settings
    try:
        (lang, enc) = locale.getdefaultlocale()
    except ValueError:
        print("Didn't detect your LC_ALL environment variable.")
        print("Please export LC_ALL with some UTF-8 encoding.")
        return False
    else:
        if enc != "UTF-8":
            print("zdict only works with encoding=UTF-8, ")
            print("but you encoding is: {} {}".format(lang, enc))
            print("Please export LC_ALL with some UTF-8 encoding.")
            return False
    return True


def get_args():
    # parse args
    parser = ArgumentParser(prog='zdict')

    parser.add_argument(
        'words',
        metavar='word',
        type=str,
        nargs='*',
        help='Words for searching its translation'
    )

    parser.add_argument(
        "-v", "--version",
        action="version",
        version='%(prog)s-' + constants.VERSION
    )

    parser.add_argument(
        "-d", "--disable-db-cache",
        default=False,
        action="store_true",
        help="Temporarily not using the result from db cache.\
              (still save the result into db)"
    )

    parser.add_argument(
        "-t", "--query-timeout",
        type=float,
        default=5.0,
        action="store",
        help="Set timeout for every query. default is 5 seconds."
    )

    parser.add_argument(
        "-sp", "--show-provider",
        default=False,
        action="store_true",
        help="Show the dictionary provider of the queried word"
    )

    parser.add_argument(
        "-su", "--show-url",
        default=False,
        action="store_true",
        help="Show the url of the queried word"
    )

    parser.add_argument(
        "-dt", "--dict",
        default="yahoo",
        action="store",
        metavar=','.join(list(dictionary_map.keys()) + ['all']),
        help="""
            Must be seperated by comma and no spaces after each comma.
            Choose the dictionary you want. (default: yahoo)
            Use 'all' for qureying all dictionaries.
            If 'all' or more than 1 dictionaries been chosen,
            --show-provider will be set to True in order to
            provide more understandable output.
        """
    )

    parser.add_argument(
        "-ld", "--list-dicts",
        default=False,
        action="store_true",
        help="Show currently supported dictionaries."
    )

    parser.add_argument(
        "-V", "--verbose",
        default=False,
        action="store_true",
        help="Show more information for the queried word.\
        (If the chosen dictionary have implemented verbose related functions)"
    )

    parser.add_argument(
        "-c", "--force-color",
        default=False,
        action="store_true",
        help="Force color printing (zdict automatically disable color printing \
        when output is not a tty, use this option to force color printing)"
    )

    return parser.parse_args()


def set_args():
    if args.list_dicts:
        for provider in sorted(
            dictionary_map,
            key=lambda x: x if x != 'yahoo' else ''
        ):
            print('{}: {}'.format(provider, dictionary_map[provider]().title))
        exit()

    if args.force_color:
        utils.Color.set_force_color()

    args.dict = args.dict.split(',')

    if 'all' in args.dict:
        args.dict = tuple(dictionary_map.keys())
    else:
        # Uniq and Filter the dict not in supported dictionary list then sort.
        args.dict = sorted(set(d for d in args.dict if d in dictionary_map))

    if len(args.dict) > 1:
        args.show_provider = True


def normal_mode():
    for word in args.words:
        for d in args.dict:
            zdict = dictionary_map[d]()
            zdict.lookup(word, args)


class MetaInteractivePrompt():
    def __init__(self, dict_list):
        self.dicts = tuple(dictionary_map[d]() for d in dict_list)

    def __del__(self):
        del self.dicts

    def prompt(self, args):
        user_input = input('[zDict]: ').strip()

        if user_input:
            for dictionary_instance in self.dicts:
                dictionary_instance.lookup(user_input, args)
        else:
            return

    def loop_prompt(self, args):
        while True:
            try:
                self.prompt(args)
            except (KeyboardInterrupt, EOFError):
                print()
                return


def interactive_mode():
    # configure readline and completer
    readline.parse_and_bind("tab: complete")
    readline.set_completer(DictCompleter().complete)

    zdict = MetaInteractivePrompt(args.dict)
    zdict.loop_prompt(args)


def execute_zdict():
    if args.words:
        normal_mode()
    else:
        interactive_mode()


def main():
    # import os
    # _ = os.environ.get('VIRTUAL_ENV', None)
    # print(_)
    # import sys
    # print(sys.path)
    # if _:
    #     sys.path = [ _ + '/lib/python3.5/site-packages'] + sys.path
    #
    # import importlib
    # if importlib.util.find_spec('pyjokes'):
    #     print('pyjokes module exists')
    # else:
    #     print('pyjokes module does not exist')
    #
    # exit()

    if user_set_encoding_and_is_utf8():
        check_zdict_dir_and_db()

        global dictionary_map
        dictionary_map = get_dictionary_map()

        global args
        args = get_args()
        set_args()

        execute_zdict()
    else:
        exit()
