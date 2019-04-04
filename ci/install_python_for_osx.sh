#!/usr/bin/sh

set -ev

curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash

# print openssl path
brew --prefix openssl@1.1

# Install specific version of Python via pyenv
LDFLAGS="-L$(brew --prefix openssl@1.1)/lib" \
CPPFLAGS="-I$(brew --prefix openssl@1.1)/include" \
CFLAGS="-I$(brew --prefix openssl@1.1)/include" \
~/.pyenv/bin/pyenv install -v $PYTHON_VERSION

# Create venv with the specific Python version
~/.pyenv/versions/$PYTHON_VERSION/bin/python3 -m venv ~/venv
