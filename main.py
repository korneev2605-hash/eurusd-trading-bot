import sys
from datetime import datetime, timedelta, timezone
import yfinance as yf
from apscheduler.schedulers.blocking import BlockingScheduler
from strategy import get_signal

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
    print("\n" + "=" * 100)
    print(f"[{summary['timestamp']}] EUR/USD SIGNAL")
    print("=" * 100)
    print(f"Price:           {summary['price']:.5f}")
    print(f"Previous Close:  {summary['prev_close']:.5f}")
    print(f"SMA(20):         {summary['sma_20']:.5f}")
    print(f"SMA(50):         {summary['sma_50']:.5f}")
    print(f"RSI(14):         {summary['rsi_14']:.2f}")
    print(f"MACD:            {summary['macd']:.6f}")
    print(f"MACD Signal:     {summary['macd_signal']:.6f}")
    print(f"MACD Histogram:  {summary['macd_hist']:.6f}")
    print("-" * 100)
    signal_color = "🟢" if summary['signal'] == "BUY" else "🔴" if summary['signal'] == "SELL" else "🟡"
    print(f"{signal_color} SIGNAL: {summary['signal']}")
    print(f"Reason: {summary['reason']}")
    print("=" * 100 + "\n")

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
    print("\n" + "*" * 100)
    print("*" + " " * 98 + "*")
    print("*" + " EUR/USD Hourly Signal Bot (Standalone EXE)".center(98) + "*")
    print("*" + " " * 98 + "*")
    print("*" * 100)
    print(f"\nStarting bot at {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print(f"Ticker: {TICKER}")
    print(f"Timeframe: {INTERVAL}")
    print(f"Historical data: {PERIOD}")
    print("\nThe bot will check for signals every hour.")
    print("Keep this window open for continuous operation.\n")

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
    
    print(f"Next check scheduled for: {(datetime.now(timezone.utc) + timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print("Bot is running. Do not close this window.\n")
    
    try:
        scheduler.start()
    except KeyboardInterrupt:
        print("\nBot stopped by user.")
        sys.exit(0)

if __name__ == "__main__":
    main()
