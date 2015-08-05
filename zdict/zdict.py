import configparser
import locale
import os
import readline

from argparse import ArgumentParser

from . import constants
from .completer import DictCompleter
from .dictionaries import DictBase
from .plugins.yahoo_dict import YahooDict


if not os.path.isdir(constants.BASE_DIR):
    os.mkdir(constants.BASE_DIR)

if not os.path.exists(constants.DB_FILE):
    open(constants.DB_FILE, 'a').close()

try:
    config = configparser.ConfigParser()
    config.readfp(open(os.path.join(constants.BASE_DIR, 'rc')))
    playback = config.get('zdict', 'playback')
    prefetch = config.get('zdict', 'prefetch')
except:
    pass


def interactive_mode(zdict, args):
    # configure readline and completer
    readline.parse_and_bind("tab: complete")
    readline.set_completer(DictCompleter().complete)
    zdict.loop_prompt(args)


def main():
    # Check user's encoding settings
    try:
        (lang, enc) = locale.getdefaultlocale()
    except ValueError:
        print("Didn't detect your LC_ALL environment variable.")
        print("Please export LC_ALL with some UTF-8 encoding.")
        exit()
    else:
        if enc != "UTF-8":
            print("zdict only works with encoding=UTF-8, ")
            print("but you encoding is: {} {}".format(lang, enc))
            print("Please export LC_ALL with some UTF-8 encoding.")
            exit()

    # parse args
    parser = ArgumentParser()

    parser.add_argument('words',
                        metavar='word',
                        type=str,
                        nargs='*',
                        help='Words for searching its translation')

    parser.add_argument("-v", "--version",
                      dest="version",
                      help="Show zdict version number.",
                      default=False,
                      action="store_true")

    parser.add_argument("-d", "--disable-db-cache",
                      dest="disable_db_cache",
                      help="Temporarily not using the result from db cache.\
                            (still save the result into db)",
                      default=False,
                      action="store_true")

    parser.add_argument("-t", "--query-timeout",
                      type=float,
                      dest="query_timeout",
                      help="Set timeout for every query. default is 5 seconds.",
                      default=5.0,
                      action="store")

    parser.add_argument("-sp", "--show-provider",
                      dest="show_provider",
                      help="Show the dictionary provider of the queried word",
                      default=False,
                      action="store_true")

    parser.add_argument("-su", "--show-url",
                      dest="show_url",
                      help="Show the url of the queried word",
                      default=False,
                      action="store_true")

    args = parser.parse_args()

    if args.version:
        print(constants.VERSION)
        exit()

    zdict = YahooDict()

    if not args.words:
        interactive_mode(zdict, args)
    else:
        for w in args.words:
            zdict.lookup(w, args)
        exit()
