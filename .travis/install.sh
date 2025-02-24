#!/bin/bash

# SPDX-FileCopyrightText: 2022 Albert Meroño, Rinke Hoekstra, Carlos Martínez
#
# SPDX-License-Identifier: MIT

if [[ $TRAVIS_OS_NAME == 'osx' ]]; then
  pyenv global $PYENV_VERSION
  if [[ $PYENV_VERSION == 2* ]]; then
    alias pip=pip2
  fi
  if [[ $PYENV_VERSION == 3* ]]; then
    alias pip=pip3
  fi
  export PATH="/Users/travis/.pyenv/shims:${PATH}"
elif [[ $TRAVIS_OS_NAME == 'windows' ]]; then
  alias pip="pip --user"
fi

if [[ $TRAVIS_BUILD_STAGE_NAME == 'Deploy' ]]; then
  virtualenv venv -p python$PYENV_VERSION
  source venv/bin/activate
fi

pip install --upgrade pip
pip install docutils==0.17.1
pip install .
pip install -r requirements-test.txt
