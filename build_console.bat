@echo off
echo Building standalone console EXE for Windows 11...
echo.
pip install --upgrade pip
pip install -r requirements.txt
echo.
echo Creating standalone executable...
pyinstaller --onefile --console main.py
echo.
echo Done! Check the 'dist' folder for main.exe
echo Run it from command line or double-click to start the bot.
pause
