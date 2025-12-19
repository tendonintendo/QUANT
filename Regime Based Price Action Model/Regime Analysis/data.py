import time
import yfinance as yf
import pandas as pd

def load_ohlc(symbol, start, end, retries=3, delay=5):
    for attempt in range(retries):
        try:
            df = yf.download(
                symbol,
                start=start,
                end=end,
                auto_adjust=False,
                progress=False,
                threads=False
            )
            if df.empty:
                raise RuntimeError("Empty DataFrame")
            df = df[["Open", "High", "Low", "Close"]]
            df.columns = ["open", "high", "low", "close"]
            df.dropna(inplace=True)
            return df
        except Exception as e:
            print(f"Attempt {attempt+1} failed: {e}")
            time.sleep(delay)
    raise RuntimeError(f"Data download failed after {retries} attempts")
