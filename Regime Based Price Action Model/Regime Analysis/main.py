from config import (
    SYMBOL,
    START_DATE,
    END_DATE,
    ROLLING_WINDOW,
    REJECTION_WICK_RATIO,
    EXPANSION_RANGE_PCT,
    EPSILON
)

from data import load_ohlc
from features import compute_price_features
from regimes import label_regimes
from analysis import regime_summary, regime_persistence


def main():
    df = load_ohlc(SYMBOL, START_DATE, END_DATE)

    if len(df) < ROLLING_WINDOW * 2:
        raise RuntimeError(
            "Not enough data to compute rolling features"
        )

    df = compute_price_features(df, ROLLING_WINDOW, EPSILON)
    df = label_regimes(
        df,
        REJECTION_WICK_RATIO,
        EXPANSION_RANGE_PCT
    )

    df.dropna(inplace=True)

    if df.empty:
        raise RuntimeError(
            "No data left after feature computation and regime labeling"
        )

    print("\n===== REGIME FREQUENCY =====")
    print(df["regime"].value_counts(normalize=True))

    print("\n===== REGIME SUMMARY =====")
    print(regime_summary(df).round(4))

    print("\n===== REGIME PERSISTENCE =====")
    print(regime_persistence(df).round(4))


if __name__ == "__main__":
    main()
