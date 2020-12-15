import re
import random
import importlib
import importlib.util

from zdict.models import Record
from zdict.utils import Color


def import_pyjokes_module():
    if importlib.util.find_spec('pyjokes'):
        return importlib.import_module('pyjokes')


def get_pyjoke(pyjokes, word: str):
    if not pyjokes:
        return

    try:
        # very basic string searching in jokes
        r = random.choice(
            list(filter(
                lambda j: word in map(
                    lambda x: ''.join(c for c in x if c.isalnum()),
                    j.split()
                ),
                pyjokes.get_jokes()
            ))
        )
    except IndexError:
        return
    else:
        return Record(word=word, content=r, source='pyjokes')


def show_pyjoke(record: Record):
    if not record:
        return

    for i, s in enumerate(
        re.split(r'\b({})\b'.format(record.word), record.content)
    ):
        Color.print(
            s,
            'lindigo' if i % 2 else 'indigo',
            end=''
        )

    print('\n\n', end='')


def lookup_pyjokes(word: str):
    pyjokes = import_pyjokes_module()

    if not pyjokes:
        return

    record = get_pyjoke(pyjokes, word)
    if record:
        Color.print('[pyjokes]', 'blue')
        show_pyjoke(record)
