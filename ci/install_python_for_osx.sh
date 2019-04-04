#!/usr/bin/sh

set -ev

curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash

# Make it use openssl only
brew uninstall openssl@1.1

# print openssl path
brew --prefix openssl

# Install specific version of Python via pyenv
~/.pyenv/bin/pyenv install -v $PYTHON_VERSION

# Create venv with the specific Python version
~/.pyenv/versions/$PYTHON_VERSION/bin/python3 -m venv ~/venv
