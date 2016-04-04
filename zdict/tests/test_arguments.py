import sys

from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

from zdict.zdict import main


def test_multiprocessing():
    testargs = ['', '-j', '2', '-d', '-dt', 'yahoo', 'test']
    with patch.object(sys, 'argv', new=testargs):
        f1 = StringIO()
        with redirect_stdout(f1):
            main()

    testargs = ['', '-j', '-d', '-dt', 'yahoo', 'test']
    with patch.object(sys, 'argv', new=testargs):
        f2 = StringIO()
        with redirect_stdout(f2):
            main()

    testargs = ['', '-d', '-dt', 'yahoo', 'test']
    with patch.object(sys, 'argv', new=testargs):
        f3 = StringIO()
        with redirect_stdout(f3):
            main()

    result1 = f1.getvalue().strip()
    result2 = f2.getvalue().strip()
    result3 = f3.getvalue().strip()

    assert result1 == result2 == result3
