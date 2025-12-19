def label_regimes(
    df,
    rejection_ratio,
    expansion_percentile
):
    df = df.copy()
    df["regime"] = "neutral"

    # Compression
    compression_mask = (
        (df["range"] < df["rolling_range_median"])
        & (df["body"] < df["range"] * 0.4)
    )
    df.loc[compression_mask, "regime"] = "compression"

    # Rejection
    rejection_mask = (
        (df["upper_ratio"] > rejection_ratio)
        | (df["lower_ratio"] > rejection_ratio)
    )
    df.loc[rejection_mask, "regime"] = "rejection"

    # Expansion
    expansion_threshold = df["range"].quantile(expansion_percentile)
    expansion_mask = df["range"] > expansion_threshold
    df.loc[expansion_mask, "regime"] = "expansion"

    return df
