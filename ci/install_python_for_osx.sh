#!/usr/bin/sh

curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash
~/.pyenv/bin/pyenv install $PYTHON_VERSION
~/.pyenv/versions/$PYTHON_VERSION/bin/python3 --version
~/.pyenv/versions/$PYTHON_VERSION/bin/python3 -m venv ~/venv
