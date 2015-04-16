#!/usr/bin/env python3

import getopt
import sys
import string
import http.client
import urllib.request
import urllib.parse
import urllib.error
import string
import sys
import locale
import shelve
import os
import random
import configparser
import xml.etree.ElementTree as ET
import readline
import ssl

from codecs import EncodedFile
from optparse import OptionParser
from multiprocessing import Process, Queue, Pool

from . import constants
from .completer import DictCompleter
from .dictionarys import DictBase


playback = ""
prefetch = ""

red = "\33[31;1m"
lindigo = "\33[36;1m"
indigo = "\33[36m"
green = "\33[32m"
yellow = "\33[33;1m"
blue = "\33[34;1m"
org = "\33[0m"
light = "\33[0;1m"


if not os.path.isdir(constants.BASE_DIR):
    os.mkdir(constants.BASE_DIR)

db = shelve.open(os.path.join(constants.BASE_DIR, 'shelve'), "c")

try:
    config = ConfigParser.ConfigParser()
    config.readfp(open(os.path.join(constants.BASE_DIR, 'ydictrc')))
    playback = config.get('ydict', 'playback')
    prefetch = config.get('ydict', 'prefetch')
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


def htmlspcahrs(content):
    content = content.replace(b"&", b"")
    content = content.replace(b"#39;", b"\'")
    content = content.replace(b"quot;", b"\"")
    return content


def http_postconn(word):
    yahoourl = "tw.dictionary.yahoo.com"
    params = urllib.parse.urlencode({'p': word})
    context = ssl._create_unverified_context()
    return urllib.request.urlopen(
        "https://{}/dictionary?{}".format(yahoourl, params),
        context=context
    )


class explan_node:
    pass


class explanation_node:
    pass


# Color print
def cprint(data, color, newline=1, indent=0, num=0):
    if newline == 1:
        nl = "\n"
    else:
        nl = ""
    if num != 0:
        nu = str(num) + ". "
    else:
        nu = ""
    idn = " " * indent
    if data is not None:
        if isinstance(data, str) or isinstance(data, str):
            return (idn + nu + color + data + org + nl)
        elif data.text is not None:
            return (idn + nu + color + data.text + org + nl)
    return None


class explan_word:
    def show(self):
        ret = ""
        res = []
        res.append(cprint(self.key, yellow))
        if self.kk is not None:
            res.append(cprint("KK", org, 0))
            res.append(cprint(self.kk, light, 0))
        if self.dj is not None:
            res.append(cprint(" DJ", org, 0))
            res.append(cprint(self.dj, light))

        for explan_entry in self.explan_list:
            res.append(cprint(explan_entry.pos_abbr, red, 0))
            res.append(cprint(explan_entry.pos_desc, red, 0))
            res.append(cprint("", org, 1))
            i = 1
            for explanation_ol_entry in explan_entry.explanation:
                res.append(cprint("", org, 0, 2, i))
                for explanation in explanation_ol_entry.explanation.iter():
                    res.append(cprint(explanation, org, 0))
                    res.append(cprint(explanation.tail, org, 0))
                res.append(cprint("", org))

                if explanation_ol_entry.example_sentence is not None:
                    res.append(cprint("    ", indigo, 0, 0))
                    for text in explanation_ol_entry.example_sentence.iter():
                        if text.tag == 'b':
                            res.append(cprint(text.text, lindigo, 0))
                            res.append(cprint(text.tail, indigo, 0))
                        else:
                            res.append(cprint(text, indigo, 0, 0))
                    res.append(cprint("", org, 1))
                res.append(cprint(explanation_ol_entry.samp, green, 1, 4))
                i += 1
        for line in res:
            if line is not None:
                ret = ret + line    # XXX bad code
        return ret


def dict(word, more_exp):
    output = ""
    word = word.strip()
    if len(word) <= 0:
        return None
    r1 = http_postconn(word)
    data1 = r1.read()
    try:
        summary = data1[data1.index(b'<div id="left">'):]
        summary = summary[:summary.index(b'<div id="right">')]
    except ValueError:
        return None

    summary = htmlspcahrs(summary)
    root = ET.XML(summary)
    exp_word = explan_word()
    exp_word.key = root.find(".//*/span[@class='yschttl']")
    exp_word.kk = root.find(".//*/span[@class='proun_value'][2]")
    exp_word.dj = root.find(".//*/span[@class='proun_value'][4]")
    exp_word.mp3 = root.find(".//*/span[@class='source']"
                             "[@data-type='audio/mpeg']")
    exp_word.ogg = root.find(".//*/span[@class='source']"
                             "[@data-type='audio/ogg']")
    if more_exp:
        search_exp = ".//*/li[@class='explanation_pos_wrapper']"
    else:
        search_exp = (".//*/li[@class='result_cluster_first res']"
                      "/*/li[@class='explanation_pos_wrapper']")

    explan_list = list()
    for explan in root.findall(search_exp):
        explanation_ol_list = list()
        explan_entry = explan_node()
        explan_entry.pos_abbr = explan.find("./h5/span[@class='pos_abbr']")
        explan_entry.pos_desc = explan.find("./h5/span[@class='pos_desc']")

        for explanation_ol in explan.findall(
            "./ol[@class='explanation_ol']/li"
        ):
            explanation_ol_entry = explanation_node()
            explanation_ol_entry.explanation = explanation_ol.find(
                "./p[@class='explanation']"
            )
            explanation_ol_entry.example_sentence = explanation_ol.find(
                "./p[@class='sample']/samp[@class='example_sentence']"
            )
            explanation_ol_entry.samp = explanation_ol.find(
                "./p[@class='sample']/samp[2]"
            )
            explanation_ol_list.append(explanation_ol_entry)
        explan_entry.explanation = explanation_ol_list
        explan_list.append(explan_entry)
    exp_word.explan_list = explan_list
    db[exp_word.key.text] = 1
    return exp_word


class yDict(DictBase):
    def get_prompt(self) -> str:
        return '[yDict]: '

    def query(self):
        ...


def main():
    ydict = yDict()

    parser = OptionParser(usage="Usage: ydict [options] word1 word2 ......")
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

    try:
        (lang, enc) = locale.getdefaultlocale()
    except ValueError:
        print("Didn't detect your LC_ALL environment variable.")
        print("Please export LC_ALL with some UTF-8 encoding.")
        cleanup()
    else:
        if enc != "UTF-8":
            print("ydict only works with encoding=UTF-8, ")
            print("but you encoding is: {} {}".format(lang, enc))
            print("Please export LC_ALL with some UTF-8 encoding.")
            cleanup()

    if options.nocolor:
        red = ""
        lindigo = ""
        indigo = ""
        green = ""
        yellow = ""
        blue = ""
        org = ""
        light = ""

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

    if len(args) >= 1:
        for w in args:
            result = dict(w, options.more_exp)
            if result is None:
                print(cprint("[" + w + "] Not found", yellow, 0))
                continue
            speak(result)
            print(result.show())
        cleanup()

    if options.learnmode:
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

    
    # configure readline and completer
    readline.parse_and_bind("tab: complete")
    readline.set_completer(DictCompleter(db).complete)
    for x in db.keys():
        readline.add_history(x)

    while(1):
        try:
            word = ydict.prompt()
        except KeyboardInterrupt:
            print("")
            cleanup()
        except EOFError:
            print("")
            cleanup()

        result = dict(word, options.more_exp)
        if result is None:
            print(cprint("[" + word + "] Not found", yellow, 0))
            continue
        else:
            speak(result)
            print(result.show())
