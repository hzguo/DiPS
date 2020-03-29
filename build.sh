#!/bin/bash

pip install virtualenv
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
cd ./packages/submodopt
python setup.py install
cd ../../