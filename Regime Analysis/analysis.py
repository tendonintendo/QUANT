import pandas as pd


def regime_summary(df):
    df = df.copy()

    # Precompute forward values safely
    df["next_range"] = df["range"].shift(-1)
    df["next_close"] = df["close"].shift(-1)
    df["next_return_1d"] = df["next_close"] / df["close"] - 1

    rows = []

    for regime in df["regime"].unique():
        sub = df[df["regime"] == regime]

        rows.append({
            "Regime": regime,
            "Frequency": len(sub) / len(df),
            "Avg Range": sub["range"].mean(),
            "Avg Next Day Range": sub["next_range"].mean(),
            "Avg 1D Return": sub["next_return_1d"].mean()
        })

    return pd.DataFrame(rows)


def regime_persistence(df):
    df = df.copy()

    rows = []

    for regime in df["regime"].unique():
        mask = df["regime"] == regime
        persistence = mask & (df["regime"].shift(-1) == regime)

        rows.append({
            "Regime": regime,
            "Persistence Rate": persistence.sum() / mask.sum()
        })

    return pd.DataFrame(rows)
