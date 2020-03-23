#! /bin/bash
# initialize python virtual environment
python3.7 -m venv ./venv
source venv/bin/activate
# install required packages
pip install --upgrade pip
pip install -r requirements.txt
# compile cython code
python setup.py build_ext --inplace
# create empty user table
mkdir app/data
echo '[]' > app/data/userdata.json
