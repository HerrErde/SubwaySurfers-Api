@echo off

echo Setting up...
rmdir /s /q .venv
python -m venv .venv

echo Installing packages...
call .venv\Scripts\activate
echo Upgrade Pip...
python.exe -m pip install --upgrade pip > nul
pip install -r requirements.txt
call deactivate

echo Finished...

exit