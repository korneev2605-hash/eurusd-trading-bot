@echo off
REM Auto-detect Python and run the bot

REM Try to find Python
where python >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    python main.py
    goto :end
)

REM Try portable Python if exists
if exist python_portable\python.exe (
    python_portable\python.exe main.py
    goto :end
)

REM Try to find any installed Python
for /f "delims= " %%A in ('dir /b /s C:\Python* 2^>nul ^| findstr "python.exe" ^| head -1') do (
    %%A main.py
    goto :end
)

echo Error: Python not found!
echo Please run 'install_and_build.bat' first.
pause

:end
