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
# create default user if necessary
DEFAULT_USER='[{"login": "root", "passw": "202cb962ac59075b964b07152d234b70"}]'
read -p "Add default user 'root' with password '123'? (Y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo "$DEFAULT_USER" > app/data/userdata.json
fi
