import sys
from pathlib import Path
import pandas as pd

# -------------------------------------------------
# Resolve project root
# -------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Add "Regime Analysis" directory to Python path
REGIME_ANALYSIS_DIR = PROJECT_ROOT / "Regime Analysis"
sys.path.append(str(REGIME_ANALYSIS_DIR))

# -------------------------------------------------
# Imports from Regime Analysis
# -------------------------------------------------
from data import load_ohlc
from regimes import label_regimes

# -------------------------------------------------
# Imports from Model (local)
# -------------------------------------------------
from backtest import backtest
from evaluation import summarize_results

# -------------------------------------------------
# Configuration
# -------------------------------------------------
SYMBOL = "SPY"
START_DATE = "2015-01-01"
END_DATE = "2024-01-01"

INITIAL_CAPITAL = 1000.0
RISK_PER_TRADE = 0.01
STOP_LOSS_PCT = 0.01
WICK_RATIO = 2.0

REJECTION_RATIO = 2.0
EXPANSION_PERCENTILE = 0.8
RANGE_WINDOW = 20

# -------------------------------------------------
# Data Preparation
# -------------------------------------------------
def prepare_features(df):
    """
    Compute candle features and rolling statistics required for regime labeling.
    """
    df = df.copy()
    df["range"] = df["high"] - df["low"]
    df["body"] = (df["close"] - df["open"]).abs()
    df["upper_ratio"] = (df["high"] - df[["close", "open"]].max(axis=1)) / df["range"]
    df["lower_ratio"] = (df[["close", "open"]].min(axis=1) - df["low"]) / df["range"]
    df["rolling_range_median"] = df["range"].rolling(RANGE_WINDOW).median()
    return df

def detect_regime_blocks(df):
    """
    Assign unique block IDs to each continuous regime segment.
    """
    df = df.copy()
    df["regime_shift"] = (df["regime"] != df["regime"].shift(1)).astype(int)
    df["regime_block"] = df["regime_shift"].cumsum()
    return df

def prepare_dataframe():
    """
    Load OHLC data, compute features, label regimes, and assign regime blocks.
    """
    df = load_ohlc(SYMBOL, START_DATE, END_DATE)
    df = prepare_features(df)
    df = label_regimes(df, rejection_ratio=REJECTION_RATIO, expansion_percentile=EXPANSION_PERCENTILE)
    df.dropna(inplace=True)
    df = detect_regime_blocks(df)
    return df

# -------------------------------------------------
# Diagnostics
# -------------------------------------------------
def regime_diagnostics(df):
    """
    Compute regime frequency and block lengths.
    """
    regime_counts = df["regime"].value_counts(normalize=True)
    block_lengths = df.groupby(["regime_block", "regime"]).size().reset_index(name="length")
    return regime_counts, block_lengths

# -------------------------------------------------
# Main
# -------------------------------------------------
def main():
    df = prepare_dataframe()

    # Regime diagnostics
    regime_freq, block_lengths = regime_diagnostics(df)
    print("===== REGIME DIAGNOSTICS =====")
    print("Regime frequency (proportion):")
    print(regime_freq.round(4))
    print("\nExample regime blocks:")
    print(block_lengths.head(10))

    # Backtest
    final_capital, equity_curve, trade_log = backtest(
        df=df,
        initial_capital=INITIAL_CAPITAL,
        risk_per_trade=RISK_PER_TRADE,
        stop_loss_pct=STOP_LOSS_PCT,
        wick_ratio=WICK_RATIO
    )

    # Evaluation
    results = summarize_results(
        final_capital=final_capital,
        equity_curve=equity_curve,
        initial_capital=INITIAL_CAPITAL
    )

    print("\n===== REGIME BLOCK PRICE ACTION MODEL =====")
    for k, v in results.items():
        print(f"{k}: {v}")

    # Trades per regime
    if trade_log is not None and len(trade_log) > 0:
        trade_df = pd.DataFrame(trade_log)
        trades_per_regime = trade_df["regime"].value_counts()
        print("\nTrades per regime:")
        print(trades_per_regime)

if __name__ == "__main__":
    main()
