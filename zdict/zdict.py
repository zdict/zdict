import getopt
import locale
import shelve
import os
import random
import configparser
import readline

from optparse import OptionParser
from multiprocessing import Process, Queue, Pool

from . import constants
from .completer import DictCompleter
from .dictionaries import DictBase
from .plugins.yahoo_dict import YahooDict


playback = ""
prefetch = ""


if not os.path.isdir(constants.BASE_DIR):
    os.mkdir(constants.BASE_DIR)

db = shelve.open(os.path.join(constants.BASE_DIR, 'shelve'), "c")

try:
    config = ConfigParser.ConfigParser()
    config.readfp(open(os.path.join(constants.BASE_DIR, 'rc')))
    playback = config.get('zdict', 'playback')
    prefetch = config.get('zdict', 'prefetch')
except:
    pass

if prefetch == "":
    prefetch = "5"


def cleanup():
    db.sync()
    exit()


def importfile(file):
    fp = open(file)
    for line in fp:
        newword = line.split(" ")[0]
        newword = newword.split("\n")[0]
        if (newword in db) == 0:
            db[newword] = 0
    print("File imported!")


def result(count, total):
    if total == 0:
        print("")
        exit()
    print("\nScore: ", int(count), "/", int(total), "(", count/total, ")")
    exit()


def seckey(x):
        return x[1]


# XXX don't use system
def speak(result):
    if playback == "" or result is None:
        return
    k = result.key.text
    os.system(playback + " '" +
              result.ogg.attrib['data-src'] +
              "' >/dev/null 2>&1 &")


def answers(iq, oq):
    while(1):
        key = iq.get()
        result = dict(key, False)
        if result is None:
            result = dict(key, True)
        oq.put(result)


def browse():
    wordlist = list(db.items())
    size = len(wordlist)
    totalcount = 0.0
    right = 0.0
    lookup = Queue(maxsize=int(prefetch))
    answer = Queue(maxsize=int(prefetch))
    lookuper = Process(target=answers, args=(lookup, answer))
    lookuper.daemon = True
    lookuper.start()

    if size <= 1:
        print("There must be at least two words needed in the list.")
        exit()
    i = 0
    while(1):
        while(not lookup.full()):
            k = wordlist[i][0]
            i = i + 1
            if i >= size:
                i = 0
            k = k.lower()
            lookup.put(k)
        result = answer.get()
        k = result.key.text
        if k not in db:
            continue
        print(result.show())
        speak(result)

        try:
            word = input("(d) Delete, (enter) Continue: ")
            if word == "d":
                del db[k]
                wordlist = list(db.items())
                size = len(wordlist)
                if size <= 1:
                    print("There must be at least two words "
                          "needed in the list.")
                    exit()
        except KeyboardInterrupt:
            result(right, totalcount)


def wordlearn():
    wordlist = list(db.items())
    wordlist.sort(key=seckey)
    size = len(wordlist)
    totalcount = 0.0
    right = 0.0
    lookup = Queue(maxsize=5)
    answer = Queue(maxsize=5)
    lookuper = Process(target=answers, args=(lookup, answer))
    lookuper.daemon = True
    lookuper.start()

    if size <= 1:
        print("There must be at least two words needed in the list.")
        exit()

    while(1):
        while(not lookup.full()):
            k = wordlist[int(random.triangular(0, size-1, 0))][0]
            k = k.lower()
            lookup.put(k)
        result = answer.get()
        if result is None:
            continue
        k = result.key.text
        if k not in db:
            continue
        s = result.show()
        s = s.replace(k, "####")
        s = s.replace(k.upper(), "####")
        s = s.replace(k[0].swapcase() + k[1:].lower(), "####")
        print(s)
        speak(result)
        word = input("Input :")

        if word == k.lower():
            print("Bingo!")
            right += 1
            db[k] += 1
            if db[k] >= 100:
                db[k] = 100
        else:
            db[k] -= 3
            if db[k] < 0:
                db[k] = 0
            print("WRONG! Correct answer is : ", k)
            try:
                word = input("(d) Delete, (enter) Continue: ")
                if word == "d":
                    del db[k]
                    wordlist = list(db.items())
                    wordlist.sort(key=seckey)
                    size = len(wordlist)
                    if size <= 1:
                        print("There must be at least two words "
                              "needed in the list.")
                        exit()
            except KeyboardInterrupt:
                result(right, totalcount)

        totalcount += 1
        if totalcount % (int(size/4) + 1) == 0:
            wordlist = list(db.items())
            wordlist.sort(key=seckey)


def wordlist():
    for k, v in sorted(db.items(), key=lambda x: x[1]):
        print(k, v)


def main():
    # Check user's encoding settings
    try:
        (lang, enc) = locale.getdefaultlocale()
    except ValueError:
        print("Didn't detect your LC_ALL environment variable.")
        print("Please export LC_ALL with some UTF-8 encoding.")
        cleanup()
    else:
        if enc != "UTF-8":
            print("zdict only works with encoding=UTF-8, ")
            print("but you encoding is: {} {}".format(lang, enc))
            print("Please export LC_ALL with some UTF-8 encoding.")
            cleanup()

    # parse options
    parser = OptionParser(usage="Usage: zdict [options] word1 word2 ......")
    parser.add_option("-e", "--exp",
                      dest="more_exp",
                      help="Show more explanation.",
                      default=False,
                      action="store_true")
    parser.add_option("-c", "--nocolor",
                      dest="nocolor",
                      help="force no color code",
                      default=False,
                      action="store_true")
    parser.add_option("-v", "--version",
                      dest="version",
                      help="show version.",
                      default=False,
                      action="store_true")
    parser.add_option("-l", "--learn",
                      dest="learnmode",
                      help="start learning mode.",
                      default=False,
                      action="store_true")
    parser.add_option("-b", "--browse",
                      dest="browsemode",
                      help="start browse mode.",
                      default=False,
                      action="store_true")
    parser.add_option("-a", "--list",
                      dest="listall",
                      help="list all word in list.",
                      default=False,
                      action="store_true")
    parser.add_option("-i", "--import",
                      dest="importfile",
                      type="string",
                      help="import a word list",
                      default=False,
                      action="store")

    (options, args) = parser.parse_args()

    if options.nocolor:
        pass

    if options.importfile:
        importfile(options.importfile)
        cleanup()

    if options.version is True:
        print(constants.VERSION)
        cleanup()

    if options.browsemode is True:
        try:
            browse()
        except KeyboardInterrupt:
            print("")
            cleanup()
        except EOFError:
            print("")
            cleanup()
    elif options.learnmode:
        try:
            wordlearn()
        except KeyboardInterrupt:
            print("")
            cleanup()
        except EOFError:
            print("")
            cleanup()
        cleanup()
    elif options.listall:
        wordlist()
        cleanup()
    elif len(args) >= 1:
        ydict = YahooDict()

        for w in args:
            ydict.lookup(w)
        cleanup()
    else:
        ydict = YahooDict()
        # configure readline and completer
        readline.parse_and_bind("tab: complete")
        readline.set_completer(DictCompleter().complete)
        # for x in db.keys():
        #     readline.add_history(x)

        ydict.loop_prompt()
