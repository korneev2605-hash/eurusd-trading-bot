import math
from datetime import datetime, timezone
import numpy as np
import pandas as pd

def calculate_rsi(series: pd.Series, period: int = 14) -> pd.Series:
    """Calculate RSI indicator."""
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()

    rs = avg_gain / avg_loss.replace(0, np.nan)
    rsi = 100 - (100 / (1 + rs))
    return rsi.fillna(50)

def calculate_macd(series: pd.Series):
    """Calculate MACD indicator."""
    ema_fast = series.ewm(span=12, adjust=False).mean()
    ema_slow = series.ewm(span=26, adjust=False).mean()
    macd = ema_fast - ema_slow
    signal = macd.ewm(span=9, adjust=False).mean()
    hist = macd - signal
    return macd, signal, hist

def prepare_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Prepare dataframe with technical indicators."""
    if df.empty:
        raise ValueError("No market data received from Yahoo Finance.")

    cleaned = df.copy()
    cleaned.columns = [col.strip() for col in cleaned.columns]

    if "Close" not in cleaned.columns:
        raise KeyError("Close price data not found.")

    # Calculate moving averages
    cleaned["SMA_20"] = cleaned["Close"].rolling(window=20).mean()
    cleaned["SMA_50"] = cleaned["Close"].rolling(window=50).mean()
    
    # Calculate momentum indicators
    cleaned["RSI_14"] = calculate_rsi(cleaned["Close"], period=14)
    cleaned["MACD"], cleaned["MACD_SIGNAL"], cleaned["MACD_HIST"] = calculate_macd(cleaned["Close"])
    
    return cleaned

def get_signal(df: pd.DataFrame):
    """Generate trading signal based on technical analysis."""
    prepared = prepare_dataframe(df)
    last = prepared.iloc[-1]
    prev = prepared.iloc[-2] if len(prepared) > 1 else last

    # Extract latest values
    price = float(last["Close"])
    sma_20 = float(last["SMA_20"])
    sma_50 = float(last["SMA_50"])
    rsi = float(last["RSI_14"])
    macd = float(last["MACD"])
    macd_signal = float(last["MACD_SIGNAL"])
    macd_hist = float(last["MACD_HIST"])

    # Trend analysis
    bullish_trend = price > sma_20 > sma_50
    bearish_trend = price < sma_20 < sma_50
    bullish_momentum = macd > macd_signal and macd_hist > 0
    bearish_momentum = macd < macd_signal and macd_hist < 0

    # Signal generation logic
    if bullish_trend and rsi > 52 and bullish_momentum:
        signal = "BUY"
        reason = "Bullish alignment: Price > SMA20 > SMA50, RSI > 52, MACD positive crossover"
    elif bearish_trend and rsi < 48 and bearish_momentum:
        signal = "SELL"
        reason = "Bearish alignment: Price < SMA20 < SMA50, RSI < 48, MACD negative crossover"
    else:
        signal = "HOLD"
        reason = "No clear signal. Waiting for stronger confluence of indicators."

    # Prepare summary
    summary = {
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S %Z"),
        "price": round(price, 5),
        "sma_20": round(sma_20, 5),
        "sma_50": round(sma_50, 5),
        "rsi_14": round(rsi, 2),
        "macd": round(macd, 6),
        "macd_signal": round(macd_signal, 6),
        "macd_hist": round(macd_hist, 6),
        "signal": signal,
        "reason": reason,
        "prev_close": round(float(prev["Close"]), 5),
    }
    return summary
