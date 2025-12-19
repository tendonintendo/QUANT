import numpy as np
import matplotlib.pyplot as plt

from monte_carlo import generate_ohlc
from backtest import backtest
from config import (
    INITIAL_CAPITAL,
    WICK_RATIO,
    STRONG_RATIO,
    N_CANDLES,
)

N_RUNS = 200
PLOT_PATHS = 30

final_capitals = []
equity_curves = []

for _ in range(N_RUNS):
    df = generate_ohlc(n_candles=N_CANDLES)
    final_cap, equity = backtest(
        df,
        INITIAL_CAPITAL,
        WICK_RATIO,
        STRONG_RATIO
    )
    final_capitals.append(final_cap)
    equity_curves.append(equity)

final_capitals = np.array(final_capitals) 

# ─────────────────────────
# PLOT 1: FINAL CAPITAL DISTRIBUTION
# ─────────────────────────
plt.figure()
plt.hist(final_capitals, bins=30)
plt.axvline(INITIAL_CAPITAL)
plt.title("Monte Carlo Final Capital Distribution")
plt.xlabel("Final Capital")
plt.ylabel("Frequency")
plt.show()

# ─────────────────────────
# PLOT 2: EQUITY CURVES
# ─────────────────────────
plt.figure()
for curve in equity_curves[:PLOT_PATHS]:
    plt.plot(curve, alpha=0.5)

plt.axhline(INITIAL_CAPITAL)
plt.title("Monte Carlo Equity Curves")
plt.xlabel("Time")
plt.ylabel("Equity")
plt.show()

# ─────────────────────────
# PLOT 3: MEAN EQUITY CURVE
# ─────────────────────────
min_len = min(len(c) for c in equity_curves)
aligned = np.array([c[:min_len] for c in equity_curves])

mean_equity = aligned.mean(axis=0)

plt.figure()
plt.plot(mean_equity)
plt.axhline(INITIAL_CAPITAL)
plt.title("Mean Monte Carlo Equity Curve")
plt.xlabel("Time")
plt.ylabel("Equity")
plt.show()
