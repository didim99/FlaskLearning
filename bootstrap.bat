@echo off
SETLOCAL
REM: initialize python virtual environment
python -m venv .\venv
call .\venv\Scripts\activate
REM: install required packages
pip install --upgrade pip
pip install -r requirements.txt
REM: compile cython code
python setup.py build_ext --inplace
REM: create empty user table
mkdir app\data
echo [] > app\data\userdata.json
REM: create default user if necessary
set DEFAULT_USER=[{"login": "root", "passw": "202cb962ac59075b964b07152d234b70"}]
set reply=n
set /p "reply=Add default user 'root' with password '123'? (y/n): "
if /i not "%reply%" == "y" goto :eof
echo %DEFAULT_USER% > app\data\userdata.json
