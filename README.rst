========================================
zdict
========================================

|issues| |travis| |license|
|gitter| |coveralls|

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

Yahoo
++++++++++++++++++++

* Normal Mode

``zdict hello``

.. image:: http://i.imgur.com/iFTysUz.png


* Interactive Mode

``zdict``

.. image:: http://i.imgur.com/NtbWXKH.png


萌典
++++++++++++++++++++

.. image:: http://i.imgur.com/FZD4HBS.png

.. image:: http://i.imgur.com/tF2S98h.png


Urban
++++++++++++++++++++

.. image:: http://i.imgur.com/KndSJqz.png

.. image:: http://i.imgur.com/nh62wi1.png


Testing
------------------------------

During development, you can install our project as *editable*::

    $ pip install -e .

We use ``py.test``::

    $ pip install pytest pytest-cov coverage
    $ python setup.py test

Also, there is some configs for ``py.test`` in ``setup.cfg``.
Change it if you need.


.. |issues| image:: https://img.shields.io/github/issues/zdict/zdict.svg
   :target: https://github.com/zdict/zdict/issues

.. |travis| image:: https://img.shields.io/travis/zdict/zdict.svg
   :target: https://travis-ci.org/zdict/zdict

.. |license| image:: https://img.shields.io/github/license/zdict/zdict.svg
   :target: https://github.com/zdict/zdict/blob/master/LICENSE.md

.. |gitter| image:: https://badges.gitter.im/Join%20Chat.svg
   :alt: Join the chat at https://gitter.im/zdict/zdict
   :target: https://gitter.im/zdict/zdict

.. |coveralls| image:: https://img.shields.io/coveralls/zdict/zdict.svg
   :target: https://coveralls.io/github/zdict/zdict
