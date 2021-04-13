#!/bin/bash
set -e

pipenv run coverage run -m pytest $@
pipenv run coverage report
pipenv run coverage html
open htmlcov/index.html
