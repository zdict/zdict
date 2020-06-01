#!/usr/bin/sh

set -ev

# if $HOME/.pyenv is empty, remove it so it can be installed by pyenv-installer
# because Travis CI cache will create $HOME/.pyenv,
# but pyenv-installer won't install if $HOME/.pyenv exists even if it's empty.
if [ -z "$(ls -A $HOME/.pyenv)" ]; then
    rmdir $HOME/.pyenv;
    curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash;
fi

# Make it use openssl only
brew uninstall --ignore-dependencies openssl@1.1

# print openssl path
brew --prefix openssl

# Install specific version of Python via pyenv if it hasn't be installed.
~/.pyenv/bin/pyenv install --skip-existing -v $PYTHON_VERSION

# Create venv with the specific Python version
~/.pyenv/versions/$PYTHON_VERSION/bin/python3 -m venv ~/venv
