#!/usr/bin/env zsh

pipenv install --quiet
pipenv run python3 import.py
pipenv run python3 classify.py

#deactivate
pipenv --rm
