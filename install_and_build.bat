@echo off
CLS
echo.
echo ============================================================================
echo EUR/USD Bot - Portable Installer for Windows 11
echo ============================================================================
echo.
echo This script will download and bundle everything into one standalone EXE.
echo No Python installation needed!
echo.
echo Step 1: Checking for Python 3.11...
echo.

REM Check if Python is already in PATH
python --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo Python found in system PATH.
    goto :build
) else (
    echo Python not found. Downloading portable Python 3.11...
    goto :download_python
)

:download_python
echo.
echo Downloading Python 3.11 portable...
set PYTHON_URL=https://www.python.org/ftp/python/3.11.9/python-3.11.9-embed-amd64.zip
set PYTHON_ZIP=python-3.11.9-embed-amd64.zip

REM Use curl if available, otherwise use powershell
curl --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    curl -L -o %PYTHON_ZIP% %PYTHON_URL%
) else (
    powershell -Command "[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; Invoke-WebRequest -Uri '%PYTHON_URL%' -OutFile '%PYTHON_ZIP%'"
)

if exist %PYTHON_ZIP% (
    echo Extracting Python...
    powershell -Command "Expand-Archive -Path '%PYTHON_ZIP%' -DestinationPath 'python_portable' -Force"
    del %PYTHON_ZIP%
    set PYTHON_PATH=%CD%\python_portable\python.exe
    echo Python extracted successfully.
) else (
    echo Failed to download Python. Please check your internet connection.
    pause
    exit /b 1
)

:build
echo.
echo Step 2: Installing dependencies...
echo.

if defined PYTHON_PATH (
    %PYTHON_PATH% -m pip install --upgrade pip --quiet
    %PYTHON_PATH% -m pip install -r requirements.txt --quiet
    %PYTHON_PATH% -m pip install pyinstaller --quiet
) else (
    python -m pip install --upgrade pip --quiet
    python -m pip install -r requirements.txt --quiet
    python -m pip install pyinstaller --quiet
)

echo.
echo Step 3: Building standalone EXE...
echo.

if defined PYTHON_PATH (
    %PYTHON_PATH% -m PyInstaller --onefile --console --name eurusd_bot main.py
) else (
    pyinstaller --onefile --console --name eurusd_bot main.py
)

echo.
echo ============================================================================
echo Build complete!
echo ============================================================================
echo.
echo Your standalone EXE is ready in the 'dist' folder:
    echo   dist/eurusd_bot.exe
echo.
echo Double-click or run it anytime - no Python needed!
echo.
echo To clean up build files, run: rmdir /s build && del eurusd_bot.spec
echo.
pause
