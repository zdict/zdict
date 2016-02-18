import re

from .models import Record, db


def dump(pattern=r'^.*$'):
    return [r.word for r in Record.select() if re.fullmatch(pattern, r.word)]
