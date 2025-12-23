import numpy as np
import pandas as pd

def generate_ohlc(
    n_candles=1000,
    start_price=100,
    mu=0.0,
    sigma=0.01
):
    prices = [start_price]

    for _ in range(n_candles):
        ret = np.random.normal(mu, sigma)
        prices.append(prices[-1] * np.exp(ret))

    prices = np.array(prices)

    opens = prices[:-1]
    closes = prices[1:]

    highs = np.maximum(opens, closes) * (1 + np.random.uniform(0, 0.002, len(opens)))
    lows  = np.minimum(opens, closes) * (1 - np.random.uniform(0, 0.002, len(opens)))

    df = pd.DataFrame({
        "open": opens,
        "high": highs,
        "low": lows,
        "close": closes
    })

    return df
