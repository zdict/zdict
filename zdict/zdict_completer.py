import sys

from itertools import count

from .completer import DictCompleter


def main():
    if len(sys.argv) > 1:
        text = sys.argv[1]
        completer = DictCompleter().complete
        output_set = set()
        try:
            for i in count():
                word = completer(text, i)
                if word not in output_set:
                    print(word)
                    output_set.add(word)
        except IndexError:
            pass
