# EUR/USD Hourly Signal Bot - Standalone EXE for Windows

## Quick Start (No Python Installation Needed!)

### Option 1: One-Click Build
1. Download this project as ZIP
2. Extract to a folder
3. **Double-click `install_and_build.bat`**
4. Wait for it to finish (~5-10 minutes, first time only)
5. Your EXE will be in the `dist` folder
6. Run `dist/eurusd_bot.exe` anytime

### Option 2: If You Already Have Python 3.10+
1. Open Command Prompt in this folder
2. Run: `python install_and_build.bat`
3. Done! Your EXE is in `dist` folder

---

## What It Does

The bot:
- Downloads the latest 200 hours of EUR/USD candlestick data from Yahoo Finance
- Calculates technical indicators (SMA, RSI, MACD)
- Generates BUY/SELL/HOLD signals
- Outputs signals to the console **every hour**
- Runs 24/7 (keep the console window open)

---

## Running the Bot

After building, just run the EXE:
```bash
dist/eurusd_bot.exe
```

Or use the launcher batch:
```bash
run_bot.bat
```

---

## Technical Indicators

**Trend:**
- SMA(20) - Short-term trend
- SMA(50) - Medium-term trend
- Price position relative to both

**Momentum:**
- RSI(14) - Overbought/Oversold levels
- MACD - Momentum and trend changes

---

## Signal Rules

### BUY Signal ✅
- Price > SMA(20) > SMA(50) (uptrend confirmed)
- RSI > 52 (momentum strength)
- MACD > Signal Line (bullish momentum)

### SELL Signal ❌
- Price < SMA(20) < SMA(50) (downtrend confirmed)
- RSI < 48 (momentum weakness)
- MACD < Signal Line (bearish momentum)

### HOLD Signal ⏸️
- None of the above conditions align
- Waiting for clearer signal

---

## Files Included

```
.
├── install_and_build.bat     ← Run this first to build EXE
├── run_bot.bat               ← Run this to start the bot
├── main.py                   ← Bot core logic
├── strategy.py               ← Signal calculation
├── requirements.txt          ← Dependencies list
└── README.md                 ← This file
```

---

## System Requirements

- **Windows 10/11** (64-bit)
- **Internet connection** (for live data)
- **~300 MB free disk space** (for bundled Python + dependencies)
- **~100 MB RAM** while running

---

## First Run

1. Run `install_and_build.bat`
   - If Python is not installed, it will download portable Python 3.11
   - All dependencies are installed automatically
   - PyInstaller bundles everything into one EXE
   - Takes 5-10 minutes the first time

2. Find your EXE in: `dist/eurusd_bot.exe`

3. Run it (no Python needed after this!)

---

## Output Example

```
[2026-10-04 12:00:00 UTC] Fetching EUR/USD data...

============================================================================
[2026-10-04 12:05:30 UTC] EUR/USD HOURLY SIGNAL
============================================================================
Price:             1.08543
Previous Close:    1.08521
SMA(20):           1.08421
SMA(50):           1.08312
RSI(14):           58.45
MACD:              0.000234
MACD Signal:       0.000198
MACD Histogram:    0.000036
----------------------------------------------------------------------------
Signal: [BUY]
Reason: Bullish alignment: Price > SMA20 > SMA50, RSI > 52, MACD positive crossover
============================================================================

Next check scheduled for: 2026-10-04 13:00:00 UTC
Bot is running...
```

---

## Troubleshooting

### "Python not found" error
- Run `install_and_build.bat` again
- The script will download portable Python automatically

### "No data available" message
- Check your internet connection
- Yahoo Finance may be rate-limiting (wait 5 min and try again)

### Build fails
- Delete `build` and `dist` folders
- Run `install_and_build.bat` again
- Try running as Administrator

### EXE crashes immediately
- Open Command Prompt
- Navigate to the `dist` folder
- Run: `eurusd_bot.exe` to see error details

---

## Customization

Edit `strategy.py` to change:
- RSI threshold (line with `rsi > 52`)
- SMA periods (20 and 50)
- MACD parameters
- Signal logic

After editing, run `install_and_build.bat` again to rebuild the EXE.

---

## Disclaimer

⚠️ **This is an educational tool. NOT financial advice.**

Forex trading carries significant risk. Past performance is not indicative of future results.
Test strategies thoroughly with virtual money before risking real capital.

---

## License

Free to use and modify. No warranty.
