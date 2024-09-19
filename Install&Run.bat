@echo off

:: Step 1: Download Python installer
curl -o python-installer.exe https://www.python.org/ftp/python/3.10.4/python-3.10.4-amd64.exe

:: Step 2: Install Python silently
python-installer.exe /quiet InstallAllUsers=1 PrependPath=1

:: Step 3: Install pip (in case it's not installed with Python)
python -m ensurepip --upgrade

:: Step 4: Install necessary dependencies from the Python script
python -c "from install_dependencies import install_packages; install_packages()"

:: Step 5: Run your main Python script
python main.py

:: Step 6: Clean up the installer
del python-installer.exe

:: Step 7: End
echo Installation complete and program is running.
pause
