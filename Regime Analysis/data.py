import yfinance as yf


def load_ohlc(symbol, start, end):
    df = yf.download(
        symbol,
        start=start,
        end=end,
        auto_adjust=False,
        progress=False,
        threads=False
    )

    if df.empty:
        raise RuntimeError(
            f"Data download failed or returned empty DataFrame for symbol: {symbol}"
        )

    df = df[["Open", "High", "Low", "Close"]]
    df.columns = ["open", "high", "low", "close"]
    df.dropna(inplace=True)

    if df.empty:
        raise RuntimeError(
            "DataFrame is empty after cleaning OHLC data"
        )

    return df
