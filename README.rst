*************
zdict |test|
*************

.. image:: https://badges.gitter.im/Join%20Chat.svg
   :alt: Join the chat at https://gitter.im/M157q/zdict
   :target: https://gitter.im/M157q/zdict?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge
*Note: This project is working in progress.*

zdict is a CLI dictionay framework mainly focus on any kind of online dictionary.
This project originly forked from https://github.com/chenpc/ydict, which is a CLI tool for the Yahoo! online dictionary.
After heavily refactoring the original project including:

1. Change from Python 2 to Python 3
2. Focus on being a flexible framework for any kind online dicitionaries, not only just a CLI tool for querying Yahoo! online dictionay.
3. Based on an open source project skeleton.

So, we decided to create a new project.


Installation
------------
``pip install git+https://github.com/M157q/zdict.git``


Usage
-----

* Normal Mode
``zdict hello``
.. image:: http://i.imgur.com/iFTysUz.png

* Interactive Mode
``zdict``
.. image:: http://i.imgur.com/NtbWXKH.png


Testing
-------
``python3 -m unittest discover``


.. |test| image:: https://img.shields.io/github/issues/M157q/zdict.svg
   :target: https://github.com/badges/shields/issues
