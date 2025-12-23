import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# =========================
# CONFIG
# =========================
SYMBOL = "SPY"
START_DATE = "2010-01-01"

IMAGE_DIR = "./images/"
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

WICK_BODY_RATIO = 4.0      
WICK_RANGE_RATIO = 0.60    

HORIZONS = [1, 3, 5]
PERMUTATIONS = 10_000

np.random.seed(42)

# =========================
# LOAD DATA
# =========================
print(f"Downloading data for {SYMBOL}...")
df = yf.download(SYMBOL, start=START_DATE, auto_adjust=True)
df = df.dropna()

if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.get_level_values(0)

# =========================
# CANDLE ANATOMY
# =========================
df["body"] = (df["Close"] - df["Open"]).abs()
df["range"] = df["High"] - df["Low"]

df["upper_wick"] = df["High"] - df[["Open", "Close"]].max(axis=1)
df["lower_wick"] = df[["Open", "Close"]].min(axis=1) - df["Low"]

df = df[(df["body"] > 0) & (df["range"] > 0)]

# =========================
# STRICT SIGNAL DEFINITION
# =========================
k = WICK_BODY_RATIO
r = WICK_RANGE_RATIO

df["long_signal"] = (
    (df["lower_wick"] >= k * df["body"]) &
    (df["lower_wick"] >= r * df["range"]) &
    (df["Close"] > df["Open"])
)

df["short_signal"] = (
    (df["upper_wick"] >= k * df["body"]) &
    (df["upper_wick"] >= r * df["range"]) &
    (df["Close"] < df["Open"])
)

print("\n===== SIGNAL FREQUENCY =====")
print(f"Long signals:  {df['long_signal'].mean():.4f}")
print(f"Short signals: {df['short_signal'].mean():.4f}")
print()

# =========================
# FORWARD RETURNS
# =========================
for h in HORIZONS:
    df[f"fwd_{h}"] = df["Close"].shift(-h) / df["Close"] - 1

df = df.dropna()

# =========================
# SUMMARY STATS
# =========================
def summarize(signal_mask, side):
    print(f"===== {side} SIGNAL STATISTICS =====")
    rows = []

    for h in HORIZONS:
        if side == "LONG":
            rts = df.loc[signal_mask, f"fwd_{h}"]
        else:
            rts = -df.loc[signal_mask, f"fwd_{h}"]

        baseline = df[f"fwd_{h}"]

        rows.append({
            "Horizon": f"{h}D",
            "Signal Mean": rts.mean(),
            "Baseline Mean": baseline.mean(),
            "Signal Median": rts.median(),
            "Win Rate": (rts > 0).mean(),
            "Count": len(rts)
        })

    summary_df = pd.DataFrame(rows)
    print(summary_df)
    print()
    return summary_df

summarize(df["long_signal"], "LONG")
summarize(df["short_signal"], "SHORT")

# =========================
# PERMUTATION TEST (1D LONG)
# =========================
signal_returns = df.loc[df["long_signal"], "fwd_1"].values
baseline_returns = df["fwd_1"].values

observed_diff = signal_returns.mean() - baseline_returns.mean()

diffs = []
print(f"Running {PERMUTATIONS} permutations...")
for _ in range(PERMUTATIONS):
    shuffled = np.random.permutation(baseline_returns)
    fake_signal = shuffled[:len(signal_returns)]
    diffs.append(fake_signal.mean() - baseline_returns.mean())

diffs = np.array(diffs)
p_value = np.mean(diffs >= observed_diff)

print("===== PERMUTATION TEST (1D, LONG) =====")
print(f"Observed mean diff: {observed_diff:.6f}")
print(f"p-value:            {p_value:.4f}")
print()

# =========================
# VISUALIZATION & SAVING
# =========================

# Plot 1: Return Distributions
plt.figure(figsize=(10, 6))
plt.hist(baseline_returns, bins=100, alpha=0.4, density=True, label="All candles", color='gray')
plt.hist(signal_returns, bins=30, alpha=0.7, density=True, label="Long signals", color='blue')
plt.axvline(0, color='black', linestyle='--', alpha=0.5)
plt.legend()
plt.title(f"{SYMBOL} Forward 1-Day Return Distribution (Wick Pattern)")
plt.xlabel("Return")
plt.ylabel("Density")
plt.tight_layout()
plt.savefig(os.path.join(IMAGE_DIR, "return_distribution.png"), dpi=300)
plt.show()

# Plot 2: Permutation Test Results
plt.figure(figsize=(10, 6))
plt.hist(diffs, bins=50, alpha=0.7, color='skyblue', edgecolor='black', label="Null Hypothesis (Shuffled)")
plt.axvline(observed_diff, color='red', linestyle='-', linewidth=2, label=f"Observed Diff (p={p_value:.4f})")
plt.title("Permutation Test: Observed Difference vs. Random Chance")
plt.xlabel("Mean Difference (Signal - Baseline)")
plt.ylabel("Frequency")
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(IMAGE_DIR, "permutation_test.png"), dpi=300)
plt.show()

print(f"Visualizations successfully saved to {IMAGE_DIR}")