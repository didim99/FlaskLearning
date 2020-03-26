@echo off
REM: initialize python virtual environment
python -m venv .\venv
.\venv\Scripts\activate
REM: install required packages
pip install --upgrade pip
pip install -r requirements.txt
REM: compile cython code
python setup.py build_ext --inplace
REM: create empty user table
mkdir app\data
echo [] > app\data\userdata.json
REM: create default user if necessary
set DEFAULT_USER=[{"login": "root", "passw": "202cb962ac59075b964b07152d234b70"}]"
:q
echo.
set /p DEPT1="Add default user 'root' with password '123'? (y/n): "
if /i not defined DEPT1 (cls & goto q)
if /i "%DEPT1%"=="y" (echo yes& goto d)
if /i "%DEPT1%"=="n" (echo no& goto e)
:d
echo %DEFAULT_USER% > app\data\userdata.json
:e
