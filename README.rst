========================================
zdict
========================================

|issues| |travis| |coveralls|

|license|

|gitter|

*Note: This project is working in progress.*

zdict is a CLI dictionay framework mainly focus on any kind of online dictionary.
This project originly forked from https://github.com/chenpc/ydict, which is a CLI tool for the Yahoo! online dictionary.
After heavily refactoring the original project including:

1. Change from Python 2 to Python 3
2. Focus on being a flexible framework for any kind online dicitionaries, not only just a CLI tool for querying Yahoo! online dictionay.
3. Based on an open source project skeleton.

So, we decided to create a new project.


Installation
------------------------------

``pip install git+https://github.com/zdict/zdict.git``


Usage
------------------------------

::

  usage: zdict [-h] [-v] [-d] [-t QUERY_TIMEOUT] [-sp] [-su]
              [-dt urban,yahoo,moe,all] [-ld] [-V] [-c]
              [word [word ...]]

  positional arguments:
    word                  Words for searching its translation

  optional arguments:
    -h, --help            show this help message and exit
    -v, --version         show program's version number and exit
    -d, --disable-db-cache
                          Temporarily not using the result from db cache. (still
                          save the result into db)
    -t QUERY_TIMEOUT, --query-timeout QUERY_TIMEOUT
                          Set timeout for every query. default is 5 seconds.
    -sp, --show-provider  Show the dictionary provider of the queried word
    -su, --show-url       Show the url of the queried word
    -dt urban,yahoo,moe,all, --dict urban,yahoo,moe,all
                          Must be seperated by comma and no spaces after each
                          comma. Choose the dictionary you want. (default:
                          yahoo) Use 'all' for qureying all dictionaries. If
                          'all' or more than 1 dictionaries been chosen, --show-
                          provider will be set to True in order to provide more
                          understandable output.
    -ld, --list-dicts     Show currently supported dictionaries.
    -V, --verbose         Show more information for the queried word. (If the
                          chosen dictionary have implemented verbose related
                          functions)
    -c, --force-color     Force color printing (zdict automatically disable
                          color printing when output is not a tty, use this
                          option to force color printing)


Screenshots
------------------------------

`Yahoo Dictionary <http://tw.dictionary.search.yahoo.com/>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Normal Mode

``zdict hello``

.. image:: http://i.imgur.com/iFTysUz.png


* Interactive Mode

``zdict``

.. image:: http://i.imgur.com/NtbWXKH.png


`Moe Dictionary 萌典 <https://www.moedict.tw>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. image:: http://i.imgur.com/FZD4HBS.png

.. image:: http://i.imgur.com/tF2S98h.png


`Urban Dictionary <http://www.urbandictionary.com/>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. image:: http://i.imgur.com/KndSJqz.png

.. image:: http://i.imgur.com/nh62wi1.png


Development & Contributing
---------------------------

Testing
^^^^^^^^

During development, you can install our project as *editable*.
If you use `virtualenv`, you may want to create a new enviroment for `zdict`::

    $ git clone https://github.com/zdict/zdict.git
    $ cd zdict
    $ pip install -e .

Once you installed it with the command above,
just execute `zdict` after modification.
Don't need to install it again.

We use ``py.test``::

    $ pip install pytest pytest-cov coverage
    $ python setup.py test

or::

    $ py.test

After runing testing, we will get a coverage report in html.
We can browse around it::

    $ cd htmlcov
    $ python -m http.server

Also, there is some configs for ``py.test`` in ``setup.cfg``.
Change it if you need.


Debugging
^^^^^^^^^^

``py.test`` can prompt ``pdb`` shell when your test case failed::

    $ python setup.py test -a "--pdb"

or::

    $ py.test --pdb


Related Projects
------------------------------

* `zdict.vim <https://github.com/zdict/zdict.vim>`_
    * A vim plugin for `zdict`


.. |issues| image:: https://img.shields.io/github/issues/zdict/zdict.svg
   :target: https://github.com/zdict/zdict/issues

.. |travis| image:: https://img.shields.io/travis/zdict/zdict.svg
   :target: https://travis-ci.org/zdict/zdict

.. |license| image:: https://img.shields.io/github/license/zdict/zdict.svg
   :target: https://github.com/zdict/zdict/blob/master/LICENSE.md

.. |gitter| image:: https://badges.gitter.im/Join%20Chat.svg
   :alt: Join the chat at https://gitter.im/zdict/zdict
   :target: https://gitter.im/zdict/zdict

.. |coveralls| image:: https://coveralls.io/repos/zdict/zdict/badge.svg
   :target: https://coveralls.io/github/zdict/zdict
