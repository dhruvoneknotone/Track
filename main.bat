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

rem Get the directory of the batch file
set "BASE_PATH=%~dp0"

rem Execute Python scripts
python "!BASE_PATH!req.py"
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
python "!BASE_PATH!logger.py"
if errorlevel 1 goto error

python "!BASE_PATH!convert.py"
if errorlevel 1 goto error

timeout /t 5 /nobreak

python "!BASE_PATH!mail.py"
if errorlevel 1 goto error

goto loop

:error
echo An error occurred while executing a Python script.
pause
exit /b 1