def candle_features(candle):
    body = abs(candle["close"] - candle["open"])
    lower_wick = min(candle["open"], candle["close"]) - candle["low"]
    upper_wick = candle["high"] - max(candle["open"], candle["close"])
    return body, lower_wick, upper_wick


def generate_signal(df, i, wick_ratio, strong_ratio):
    candle = df.iloc[i]
    body, lower_wick, upper_wick = candle_features(candle)

    if body == 0:
        return None

    # Bullish
    if candle["close"] > candle["open"] and lower_wick >= wick_ratio * body:
        if lower_wick >= strong_ratio * body:
            return "long"
        else:
            return "confirm_long"

    # Bearish
    if candle["close"] < candle["open"] and upper_wick >= wick_ratio * body:
        if upper_wick >= strong_ratio * body:
            return "short"
        else:
            return "confirm_short"

    return None
