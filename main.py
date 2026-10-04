import sys
import os
from datetime import datetime, timedelta, timezone

try:
    import yfinance as yf
    from apscheduler.schedulers.blocking import BlockingScheduler
    from strategy import get_signal
except ImportError as e:
    print(f"Error: Missing dependency - {e}")
    print("Please run 'install_and_build.bat' first.")
    input("Press Enter to exit...")
    sys.exit(1)

TICKER = "EURUSD=X"
INTERVAL = "1h"
PERIOD = "200h"

def fetch_market_data():
    """Fetch EUR/USD hourly data from Yahoo Finance."""
    try:
        data = yf.download(
            TICKER,
            period=PERIOD,
            interval=INTERVAL,
            auto_adjust=False,
            progress=False,
        )
        return data
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def print_signal_summary(summary):
    """Print trading signal summary to console."""
    print("\n" + "=" * 120)
    print(f"[{summary['timestamp']}] EUR/USD HOURLY SIGNAL")
    print("=" * 120)
    print(f"Price:             {summary['price']:.5f}")
    print(f"Previous Close:    {summary['prev_close']:.5f}")
    print(f"SMA(20):           {summary['sma_20']:.5f}")
    print(f"SMA(50):           {summary['sma_50']:.5f}")
    print(f"RSI(14):           {summary['rsi_14']:.2f}")
    print(f"MACD:              {summary['macd']:.6f}")
    print(f"MACD Signal:       {summary['macd_signal']:.6f}")
    print(f"MACD Histogram:    {summary['macd_hist']:.6f}")
    print("-" * 120)
    
    if summary['signal'] == "BUY":
        signal_str = "\u001b[92m[BUY] \u001b[0m"
    elif summary['signal'] == "SELL":
        signal_str = "\u001b[91m[SELL]\u001b[0m"
    else:
        signal_str = "\u001b[93m[HOLD]\u001b[0m"
    
    print(f"Signal: {signal_str}")
    print(f"Reason: {summary['reason']}")
    print("=" * 120 + "\n")

def run_cycle():
    """Execute one analysis cycle."""
    try:
        now = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S %Z')
        print(f"[{now}] Fetching EUR/USD data...")
        
        df = fetch_market_data()
        if df is None or df.empty:
            print(f"[{now}] No data available. Retrying in 1 hour...")
            return

        summary = get_signal(df)
        print_signal_summary(summary)
    except Exception as exc:
        now = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S %Z')
        print(f"[{now}] ERROR: {exc}")
        import traceback
        traceback.print_exc()

def main():
    """Main bot entry point."""
    print("\n" + "*" * 120)
    print("*" + " " * 118 + "*")
    print("*" + " EUR/USD Hourly Signal Bot - Standalone EXE".center(118) + "*")
    print("*" + " " * 118 + "*")
    print("*" * 120)
    print(f"\nStarted at: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print(f"Ticker: {TICKER}")
    print(f"Timeframe: {INTERVAL}")
    print(f"Historical period: {PERIOD}")
    print("\nThe bot will analyze EUR/USD and output signals every hour.")
    print("Keep this window open for continuous operation.")
    print("Press Ctrl+C to stop the bot.\n")

    # Run first cycle immediately
    run_cycle()

    # Schedule hourly checks
    scheduler = BlockingScheduler()
    scheduler.add_job(
        run_cycle,
        trigger="interval",
        hours=1,
        next_run_time=datetime.now(timezone.utc) + timedelta(hours=1),
    )
    
    next_check = (datetime.now(timezone.utc) + timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S %Z')
    print(f"Next check scheduled for: {next_check}")
    print("Bot is running...\n")
    
    try:
        scheduler.start()
    except KeyboardInterrupt:
        print("\n\nBot stopped by user.")
        sys.exit(0)

if __name__ == "__main__":
    main()
