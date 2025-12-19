import numpy as np


def compute_price_features(df, rolling_window, epsilon):
    df = df.copy()

    df["body"] = (df["close"] - df["open"]).abs()
    df["range"] = df["high"] - df["low"]

    df["upper_wick"] = df["high"] - df[["open", "close"]].max(axis=1)
    df["lower_wick"] = df[["open", "close"]].min(axis=1) - df["low"]

    df["upper_ratio"] = df["upper_wick"] / (df["body"] + epsilon)
    df["lower_ratio"] = df["lower_wick"] / (df["body"] + epsilon)

    df["rolling_range_mean"] = df["range"].rolling(rolling_window).mean()
    df["rolling_range_median"] = df["range"].rolling(rolling_window).median()

    df["rolling_high"] = df["high"].rolling(rolling_window).max()
    df["rolling_low"] = df["low"].rolling(rolling_window).min()

    df["range_position"] = (
        (df["close"] - df["rolling_low"])
        / (df["rolling_high"] - df["rolling_low"] + epsilon)
    )

    return df
