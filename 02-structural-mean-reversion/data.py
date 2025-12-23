import yfinance as yf
import pandas as pd


def load_ohlc(symbol, period="60d", interval="5m"):
    """
    Load intraday OHLC data from Yahoo Finance.
    Limited to last 60 days for 5m bars.
    """
    df = yf.download(
        symbol,
        period=period,
        interval=interval,
        auto_adjust=False,
        progress=False,
        threads=False
    )

    if df.empty:
        raise RuntimeError("Empty DataFrame from yfinance")

    df = df[["Open", "High", "Low", "Close", "Volume"]]
    df.columns = ["open", "high", "low", "close", "volume"]
    df.dropna(inplace=True)

    return df
