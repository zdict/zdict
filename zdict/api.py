import re

from zdict.models import Record


def dump(pattern=r'^.*$'):
    return [r.word for r in Record.select() if re.fullmatch(pattern, r.word)]
