from argparse import ArgumentParser, ArgumentTypeError
from locale import getdefaultlocale
from multiprocessing import Pool
from contextlib import redirect_stdout
from io import StringIO

from zdict import constants, utils, easter_eggs
from zdict.api import dump
from zdict.completer import DictCompleter
from zdict.loader import get_dictionary_map
from zdict.utils import readline, check_zdict_dir_and_db


def user_set_encoding_and_is_utf8():
    # Check user's encoding settings
    try:
        (lang, enc) = getdefaultlocale()
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

    def positive_int_only(value):
        ivalue = int(value)
        if ivalue <= 0:
            raise ArgumentTypeError(
                "%s is an invalid positive int value" % value
            )
        return ivalue

    parser.add_argument(
        "-j", "--jobs",
        type=positive_int_only,
        nargs="?",
        default=0,     # 0: not using, None: auto, N (1, 2, ...): N jobs
        action="store",
        help="""
            Allow N jobs at once.
            Do not pass any argument to use the number of CPUs in the system.
        """
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

    available_dictionaries = list(dictionary_map.keys())
    available_dictionaries.append('all')
    parser.add_argument(
        "-dt", "--dict",
        default="yahoo",
        action="store",
        choices=available_dictionaries,
        metavar=','.join(available_dictionaries),
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

    parser.add_argument(
        '--dump', dest='pattern',
        nargs='?',
        default=None, const=r'^.*$',
        help='Dump the querying history, can be filtered with regex'
    )

    parser.add_argument(
        "-D", "--debug",
        default=False,
        action="store_true",
        help="Print raw html prettified by BeautifulSoup for debugging."
    )

    return parser.parse_args()


def set_args(args):
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

    return args


def lookup_string_wrapper(dict_class, word, args):
    import sys
    if args.force_color:
        utils.Color.set_force_color()
    else:
        utils.Color.set_force_color(sys.stdout.isatty())

    dictionary = dict_class(args)
    f = StringIO()
    with redirect_stdout(f):
        dictionary.lookup(word)
    return f.getvalue()


def init_worker():
    # When -j been used, make subprocesses ignore KeyboardInterrupt
    # for not showing KeyboardInterrupt traceback error message.
    import signal
    signal.signal(signal.SIGINT, signal.SIG_IGN)


def normal_mode(args):
    if args.jobs == 0:
        # user didn't use `-j`
        for word in args.words:
            for d in args.dict:
                zdict = dictionary_map[d](args)
                zdict.lookup(word)
    else:
        # user did use `-j`
        # If processes is None, os.cpu_count() is used.
        pool = Pool(args.jobs, init_worker)

        for word in args.words:
            futures = [
                pool.apply_async(lookup_string_wrapper,
                                 (dictionary_map[d], word, args))
                for d in args.dict
            ]
            results = [i.get() for i in futures]
            print(''.join(results))

    easter_eggs.lookup_pyjokes(word)


class MetaInteractivePrompt():
    def __init__(self, args):
        self.args = args
        self.dicts = tuple(
            dictionary_map[d](self.args) for d in self.args.dict
        )
        self.dict_classes = tuple(dictionary_map[d] for d in self.args.dict)

        if self.args.jobs == 0:
            # user didn't use `-j`
            self.pool = None
        else:
            # user did use `-j`
            # If processes is None, os.cpu_count() is used.
            self.pool = Pool(self.args.jobs, init_worker)

    def __del__(self):
        del self.dicts

    def prompt(self):
        user_input = input('[zDict]: ').strip()

        if user_input:
            if self.pool:
                futures = [
                    self.pool.apply_async(lookup_string_wrapper,
                                          (d, user_input, self.args))
                    for d in self.dict_classes
                ]
                results = [i.get() for i in futures]
                print(''.join(results))
            else:
                for dictionary_instance in self.dicts:
                    dictionary_instance.lookup(user_input)
        else:
            return

    def loop_prompt(self):
        while True:
            self.prompt()


def interactive_mode(args):
    # configure readline and completer
    readline.parse_and_bind("tab: complete")
    readline.set_completer(DictCompleter().complete)

    zdict = MetaInteractivePrompt(args)
    zdict.loop_prompt()


def execute_zdict(args):
    if args.list_dicts:
        for provider in sorted(
            dictionary_map,
            key=lambda x: {'yahoo': 0, 'pyjokes': 2}.get(x, 1)
        ):
            print(
                '{}: {}'.format(
                    provider,
                    dictionary_map[provider](args).title
                )
            )
        exit()

    if args.pattern:
        for word in dump(pattern=args.pattern):
            print(word)
        exit()

    try:
        if args.words:
            normal_mode(args)
        else:
            interactive_mode(args)
    except (KeyboardInterrupt, EOFError):
        print()
        return


def main():
    if user_set_encoding_and_is_utf8():
        check_zdict_dir_and_db()

        global dictionary_map
        dictionary_map = get_dictionary_map()

        args = get_args()
        args = set_args(args)

        execute_zdict(args)
    else:
        exit()
