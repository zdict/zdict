import locale
import readline

from argparse import ArgumentParser

from . import constants
from . import dictionaries
from . import utils
from .completer import DictCompleter


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
        default=["yahoo"],
        action="store",
        choices=dictionary_list + ['all'],
        nargs = '+',
        help="""
            Choose the dictionary you want. (default: yahoo)
            Use 'all' for qureying all dictionaries.
            If 'all' has been chosen,
            --show-provider will be set to True in order to
            provide more understandable output.
        """
    )

    return parser.parse_args()


def set_args():
    if 'all' in args.dict:
        args.dict = dictionary_list
    else:
        args.dict = list(set(args.dict))

    if len(args.dict) > 1:
        args.show_provider = True


def normal_mode():
    for word in args.words:
        for d in args.dict:
            zdict = getattr(dictionaries, d)()
            zdict.lookup(word, args)


class MetaInteractivePrompt():
    def __init__(self, dict_list):
        self.dict_list = [getattr(dictionaries, d)() for d in dict_list]

    def __del__(self):
        del self.dict_list

    def prompt(self, args):
        user_input = input('[zDict]: ').strip()

        if user_input:
            for dictionary_instance in self.dict_list:
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
    if user_set_encoding_and_is_utf8():
        check_zdict_dir_and_db()

        global dictionary_list
        dictionary_list = sorted(list(
            filter(lambda attr: not attr.startswith('_'), dir(dictionaries))
        ))

        global args
        args = get_args()
        set_args()

        execute_zdict()
    else:
        exit()
