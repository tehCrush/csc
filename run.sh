#!/bin/bash
package_file=csc
BASEDIR=$PWD
VENV=$(pipenv --venv)
pipenv requirements > requirements.txt
cd app
./main.py
