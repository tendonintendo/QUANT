import numpy as np

def wick_features(candle):
    body = abs(candle["close"] - candle["open"])
    upper_wick = candle["high"] - max(candle["open"], candle["close"])
    lower_wick = min(candle["open"], candle["close"]) - candle["low"]
    return body, upper_wick, lower_wick


def wick_signal(df, i, wick_ratio):
    """
    Long wick rejection signal.
    """
    candle = df.iloc[i]

    body = abs(candle["close"] - candle["open"])
    lower_wick = min(candle["open"], candle["close"]) - candle["low"]

    if body == 0:
        return None

    if lower_wick / body >= wick_ratio and candle["close"] > candle["open"]:
        return "long"

    return None


