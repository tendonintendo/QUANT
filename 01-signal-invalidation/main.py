import numpy as np
from monte_carlo import generate_ohlc
from backtest import backtest
from config import (
    INITIAL_CAPITAL,
    WICK_RATIO,
    STRONG_RATIO,
    N_CANDLES,
    N_SIMULATIONS
)

final_capitals = []
equity_curves = []

for _ in range(N_SIMULATIONS):
    df = generate_ohlc(n_candles=N_CANDLES)

    final_capital, equity_curve = backtest(
        df,
        INITIAL_CAPITAL,
        WICK_RATIO,
        STRONG_RATIO
    )

    final_capitals.append(final_capital)
    equity_curves.append(equity_curve)

final_capitals = np.array(final_capitals)

print("Monte Carlo Results")
print("-------------------")
print(f"Mean final capital: {final_capitals.mean():.2f}")
print(f"Median: {np.median(final_capitals):.2f}")
print(f"Win rate: {(final_capitals > INITIAL_CAPITAL).mean() * 100:.1f}%")
print(f"Worst run final capital: {final_capitals.min():.2f}")
