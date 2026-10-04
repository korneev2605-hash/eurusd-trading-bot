@echo off
echo Building standalone EXE for Windows 11...
echo.
pip install --upgrade pip
pip install -r requirements.txt
echo.
echo Creating standalone executable...
pyinstaller --onefile --windowed --icon=icon.ico --add-data="." main.py
echo.
echo Done! Check the 'dist' folder for eurusd_signal_bot.exe
pause
