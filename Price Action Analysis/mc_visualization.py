import numpy as np
import matplotlib.pyplot as plt
import os

from monte_carlo import generate_ohlc
from backtest import backtest
from config import (
    INITIAL_CAPITAL,
    WICK_RATIO,
    STRONG_RATIO,
    N_CANDLES,
)

IMAGE_DIR = "./images/"
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

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
plt.figure(figsize=(10, 6))
plt.hist(final_capitals, bins=30, color='skyblue', edgecolor='black', alpha=0.7)
plt.axvline(INITIAL_CAPITAL, color='red', linestyle='--', label='Initial Capital')
plt.title("Monte Carlo Final Capital Distribution", fontsize=14)
plt.xlabel("Final Capital", fontsize=12)
plt.ylabel("Frequency", fontsize=12)
plt.legend()
plt.savefig(os.path.join(IMAGE_DIR, "mc_distribution.png"), dpi=300)
plt.close()

# ─────────────────────────
# PLOT 2: EQUITY CURVES
# ─────────────────────────
plt.figure(figsize=(10, 6))
for curve in equity_curves[:PLOT_PATHS]:
    plt.plot(curve, alpha=0.3, color='gray')

plt.axhline(INITIAL_CAPITAL, color='red', linestyle='--', label='Initial Capital')
plt.title(f"Monte Carlo Equity Curves (First {PLOT_PATHS} Paths)", fontsize=14)
plt.xlabel("Time (Steps)", fontsize=12)
plt.ylabel("Equity", fontsize=12)
plt.savefig(os.path.join(IMAGE_DIR, "mc_equity_paths.png"), dpi=300)
plt.close()

# ─────────────────────────
# PLOT 3: MEAN EQUITY CURVE
# ─────────────────────────
min_len = min(len(c) for c in equity_curves)
aligned = np.array([c[:min_len] for c in equity_curves])
mean_equity = aligned.mean(axis=0)

plt.figure(figsize=(10, 6))
plt.plot(mean_equity, color='navy', linewidth=2, label='Mean Equity')
plt.axhline(INITIAL_CAPITAL, color='red', linestyle='--', label='Initial Capital')
plt.title("Expected Value of Equity (Monte Carlo Mean)", fontsize=14)
plt.xlabel("Time (Steps)", fontsize=12)
plt.ylabel("Equity", fontsize=12)
plt.legend()
plt.savefig(os.path.join(IMAGE_DIR, "mc_mean_equity.png"), dpi=300)
plt.close()

print(f"Success: 3 visualizations saved to {IMAGE_DIR}")