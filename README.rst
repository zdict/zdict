========================================
zdict
========================================

|license| |version| |python version| |month download|

|stars| |forks| |contributors| |pull requests| |issues|

|github_actions| |circleci| |coveralls|

|docker automated build| |docker build status|

|gitter|

|pyup status|

**[ ~ Dependencies scanned by PyUp.io ~ ]**

----

zdict is a CLI dictionary framework mainly focus on any kind of online dictionary.
This project originally forked from https://github.com/chenpc/ydict, which is a CLI tool for the Yahoo! online dictionary.
After heavily refactoring the original project including:

1. Change from Python 2 to Python 3
2. Focus on being a flexible framework for any kind online dicitionaries, not only just a CLI tool for querying Yahoo! online dictionary.
3. Based on an open source project skeleton.

So, we decided to create a new project.


----

.. contents:: Table of Contents

----


Installation
------------------------------

from `PyPI <https://pypi.org/project/zdict/>`_ :

.. code-block:: sh

    pip install zdict


from `GitHub <https://github.com/zdict/zdict.git>`_ :

.. code-block:: sh

    pip install git+https://github.com/zdict/zdict.git


from `Docker Hub <https://hub.docker.com/r/zdict/zdict/>`_ :

.. code-block:: sh

    # Pull the image of latest commit of master branch from Docker Hub
    docker pull zdict/zdict

    # Pull the image of latest release from Docker Hub
    docker pull zdict/zdict:release

    # Pull the image of specific release version from Docker Hub
    docker pull zdict/zdict:${version}
    docker pull zdict/zdict:v0.10.0


How to run the zdict docker image

.. code-block:: sh

    # Run interactive mode
    docker run -it --rm zdict/zdict         # latest commit
    docker run -it --rm zdict/zdict:release # latest release
    docker run -it --rm zdict/zdict:v0.10.0 # use zdict v0.10.0
    docker run -it --rm zdict/zdict:$tag    # with specific tag

    # Run normal mode
    docker run -it --rm zdict/zdict apple bird         # latest commit
    docker run -it --rm zdict/zdict:release apple bird # latest release
    docker run -it --rm zdict/zdict:v0.10.0 apple bird # use zdict v0.10.0
    docker run -it --rm zdict/zdict:$tag apple bird    # with specific tag

    # You can also add the options while using docker run either interactive mode or normal mode
    docker run -it --rm zdict/zdict:v0.10.0 -dt moe    # use moe dict in interactive mode
    docker run -it --rm zdict/zdict:v0.10.0 -dt moe 哈 # use moe dict in normal mode

Usage
------------------------------

::

	usage: zdict [-h] [-v] [-d] [-t QUERY_TIMEOUT] [-j [JOBS]] [-sp] [-su]
				 [-dt itaigi,moe,moe-taiwanese,spanish,oxford,jisho,yahoo,naer,wiktionary,urban,yandex,all]
				 [-ld] [-V] [-c] [--dump [PATTERN]] [-D]
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
	  -j [JOBS], --jobs [JOBS]
							Allow N jobs at once. Do not pass any argument to use
							the number of CPUs in the system.
	  -sp, --show-provider  Show the dictionary provider of the queried word
	  -su, --show-url       Show the url of the queried word
	  -dt itaigi,moe,moe-taiwanese,spanish,oxford,jisho,yahoo,naer,wiktionary,urban,yandex,all, --dict itaigi,moe,moe-taiwanese,spanish,oxford,jisho,yahoo,naer,wiktionary,urban,yandex,all
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
	  --dump [PATTERN]      Dump the querying history, can be filtered with regex
	  -D, --debug           Print raw html prettified by BeautifulSoup for
							debugging.


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


`SpanishDict <http://www.spanishdict.com/>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. image:: http://i.imgur.com/Ld2QVvP.png

.. image:: http://i.imgur.com/HJ9h5JO.png


`Jisho Japanese Dictionary <http://jisho.org/>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. image:: http://i.imgur.com/63n3qmH.png

.. image:: http://i.imgur.com/UMP8k4e.png


`Yandex Translate <https://translate.yandex.com/>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. image:: https://user-images.githubusercontent.com/2716047/29741879-ca1a3826-8a3a-11e7-9701-4a7e9a15971a.png


`Oxford Dictionary <https://en.oxforddictionaries.com/>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. image:: http://i.imgur.com/VkPEfKh.png

To use this source, you should first `apply <https://developer.oxforddictionaries.com/>`_ an API key and place it under ``~/.zdict/oxford.key`` in the format::

    app_id, app_key


`Wiktionary <https://en.wiktionary.org/>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. image:: https://i.imgur.com/5OzIFU3.png

.. image:: https://i.imgur.com/UO5nQjU.png


`iTaigi-愛台語 <https://itaigi.tw/>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. image:: https://user-images.githubusercontent.com/1645228/55309799-656acd00-5491-11e9-9d79-4ae578c83f8b.jpg

.. image:: https://user-images.githubusercontent.com/1645228/55309820-7582ac80-5491-11e9-998d-51ebfb183375.jpg


`國家教育研究院 - 雙語詞彙、學術名詞暨辭書資訊網 <https://terms.naer.edu.tw/>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. image:: https://user-images.githubusercontent.com/1645228/86770837-e6951480-c083-11ea-95f2-51b1e6f7e04f.jpg

.. image:: https://user-images.githubusercontent.com/1645228/86770828-e432ba80-c083-11ea-813a-e357f213826a.jpg


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
No need to install it again.

Install the packages for testing::

    $ pip install -r requirements-test.txt

or::

    $ make install-test-deps

Use the command below to execute the tests::

    $ py.test

or::

    $ make test

After runing testing, we will get a coverage report in html.
We can browse around it::

    $ cd htmlcov
    $ python -m http.server

Also, there is some configs for ``py.test`` in ``setup.cfg``.
Change it if you need.


Debugging
^^^^^^^^^^

``py.test`` can prompt ``pdb`` shell when your test case failed::

    $ py.test --pdb

or::

    $ make test-with-pdb


Bug Report
^^^^^^^^^^^

Feel free to send a bug report to https://github.com/zdict/zdict/issues.
Please attach the error message and describe how to reproduce the bug.
PR is also welcome.

Please use the ``-d/--disable-db-cache`` option to query before sending the bug report.
Sometimes we modify the data schema in database for a dictionary,
but the default dictionary query of zdict uses the cache in the database which may be stored within an old schema.
This might cause an error while showing the result.
Just use the ``-d/--disable-db-cache`` to update the cache in database.


Related Projects
------------------------------

* `zdict.vim <https://github.com/zdict/zdict.vim>`_
    * A vim plugin integrates with zdict.
* `zdict.sh <https://github.com/zdict/zdict.sh>`_
    * A collection of shell completion scripts for zdict.
* `zdict_jupyter <https://github.com/zdict/zdict_jupyter>`_
    * Use zdict in Jupyter Notebook.


Stargazers over time
---------------------

|stargazers|

.. |version| image:: https://img.shields.io/pypi/v/zdict.svg
   :target: https://pypi.org/project/zdict

.. |python version| image:: https://img.shields.io/pypi/pyversions/zdict.svg
   :target: https://pypi.org/project/zdict

.. |month download| image:: https://img.shields.io/pypi/dm/zdict.svg
   :target: https://pypi.org/project/zdict

.. |stars| image:: https://img.shields.io/github/stars/zdict/zdict.svg
   :target: https://github.com/zdict/zdict/

.. |forks| image:: https://img.shields.io/github/forks/zdict/zdict.svg
   :target: https://github.com/zdict/zdict/

.. |contributors| image:: https://img.shields.io/github/contributors/zdict/zdict.svg
   :target: https://github.com/zdict/zdict/graphs/contributors

.. |pull requests| image:: https://img.shields.io/github/issues-pr/zdict/zdict.svg
   :target: https://github.com/zdict/zdict/pulls

.. |issues| image:: https://img.shields.io/github/issues/zdict/zdict.svg
   :target: https://github.com/zdict/zdict/issues

.. |github_actions| image:: https://github.com/zdict/zdict/workflows/macOS%20testings/badge.svg
   :target: https://github.com/zdict/zdict/actions

.. |circleci| image:: https://circleci.com/gh/zdict/zdict.svg?style=svg
   :target: https://circleci.com/gh/zdict/zdict

.. |license| image:: https://img.shields.io/github/license/zdict/zdict.svg
   :target: https://github.com/zdict/zdict/blob/master/LICENSE.md

.. |gitter| image:: https://badges.gitter.im/Join%20Chat.svg
   :alt: Join the chat at https://gitter.im/zdict/zdict
   :target: https://gitter.im/zdict/zdict

.. |coveralls| image:: https://coveralls.io/repos/zdict/zdict/badge.svg
   :target: https://coveralls.io/github/zdict/zdict

.. |stargazers| image:: https://starcharts.herokuapp.com/zdict/zdict.svg
   :target: https://starcharts.herokuapp.com/zdict/zdict

.. |docker automated build| image:: https://img.shields.io/docker/automated/zdict/zdict
   :target: https://hub.docker.com/r/zdict/zdict

.. |docker build status| image:: https://img.shields.io/docker/build/zdict/zdict
   :target: https://hub.docker.com/r/zdict/zdict

.. |pyup status| image:: https://pyup.io/repos/github/zdict/zdict/shield.svg
   :target: https://pyup.io/repos/github/zdict/zdict/
   :alt: pyup.io badge
