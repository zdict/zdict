import re
import os

from inspect import getmembers
from importlib import find_loader, import_module
from itertools import chain

from . import dictionaries
from .dictionary import DictBase


def get_dictionary_map():
    '''
    Auto discover dictionaries in package ``dictionaries``.
    Each dictionary class MUST be the subclass of ``DictBase``

    :return: a dict with {provider_name: cls}
        SomeDict.provider as key, the class as value
    '''
    package = 'zdict.dictionaries'
    exclude_files = ('template.py',)

    return {
        cls().provider: cls
            for _, cls in (chain.from_iterable(
                getmembers(mod, predicate=_is_dict)
                for mod in (
                    import_module(
                        '{}.{}'.format(package, f.partition('.py')[0]))
                    for f in os.listdir(dictionaries.__path__[0])
                        if not f.startswith('_')
                               and
                           f.endswith('.py')
                               and
                           f not in exclude_files
                )
            )
        )
    }




def _is_dict(cls):
    try:
        return issubclass(cls, DictBase) and not (cls is DictBase)
    except:
        return False
