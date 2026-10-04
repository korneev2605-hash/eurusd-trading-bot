# EUR/USD Hourly Signal Bot (Windows Standalone EXE)

## Overview
A simple, portable standalone bot that analyzes EUR/USD hourly candlesticks from Yahoo Finance and outputs BUY/SELL/HOLD signals to the console every hour.

**No Python installation required** — everything is bundled into a single `.exe` file.

## Features
- **Data Source**: Yahoo Finance (`EURUSD=X`)
- **Timeframe**: 1-hour candlesticks
- **Indicators**:
  - SMA(20) and SMA(50) — trend confirmation
  - RSI(14) — momentum confirmation
  - MACD — trend strength and direction
- **Signal Types**:
  - 🟢 **BUY** — bullish conditions aligned
  - 🔴 **SELL** — bearish conditions aligned
  - 🟡 **HOLD** — no clear signal
- **Automation**: Checks automatically every hour
- **Output**: Real-time console output with all indicator values

## Download & Run (Windows 11)

### Option 1: Ready-Made EXE (If Available)
Just download `eurusd_signal_bot.exe` and double-click it.

### Option 2: Build Your Own EXE
1. Install Python 3.10+ from [python.org](https://www.python.org/)
2. Download this repo as a ZIP or clone it
3. Extract to a folder
4. Double-click `build_console.bat`
5. Wait for the build to complete (~5-10 minutes)
6. Your EXE will be in the `dist` folder

## Usage
```bash
dist/main.exe
```

The bot will:
1. Fetch the latest 200 hours of EUR/USD data
2. Calculate indicators
3. Output the first signal immediately
4. Wait for the next hour and repeat

**Keep the console window open** for continuous operation.

## Strategy Rules

### BUY Signal
- Price > SMA(20) > SMA(50) (uptrend)
- RSI > 52 (momentum strength)
- MACD > Signal Line (positive momentum)

### SELL Signal
- Price < SMA(20) < SMA(50) (downtrend)
- RSI < 48 (momentum weakness)
- MACD < Signal Line (negative momentum)

### HOLD
- None of the above conditions are met

## Files
- `main.py` — Main bot logic
- `strategy.py` — Signal calculation and indicators
- `requirements.txt` — Python dependencies
- `build_console.bat` — Build script for standalone EXE
- `README.md` — This file

## System Requirements
- Windows 11 (Windows 10 also supported)
- Internet connection (for live data from Yahoo Finance)
- ~200 MB disk space (for the EXE + dependencies)
- ~100 MB RAM while running

## Troubleshooting

### "No data available" error
- Check your internet connection
- Yahoo Finance may be rate-limiting — wait 5 minutes and try again

### EXE won't start
- Try running from Command Prompt to see error details:
  ```bash
  cd dist
  main.exe
  ```

### Build fails
- Make sure Python is installed and added to PATH
- Run Command Prompt as Administrator
- Delete the `build` and `dist` folders before rebuilding

## Disclaimer
This is an educational tool. It is NOT financial advice. Trading carries risk. Test thoroughly before using real money.

## License
Free to use and modify.
