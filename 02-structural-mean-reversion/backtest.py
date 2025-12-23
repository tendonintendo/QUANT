import pandas as pd
import numpy as np

def backtest(
    df,
    initial_capital,
    risk_per_trade,
    wick_body_ratio,
    wick_atr_ratio,
    tp_atr,
    sl_atr,
    max_hold_bars,
    vwap_distance_atr,
):
    capital = initial_capital
    equity_curve = [capital]

    position = None
    trades = []

    for i in range(20, len(df)):
        row = df.iloc[i]

        body = abs(row["close"] - row["open"])
        lower_wick = min(row["open"], row["close"]) - row["low"]
        upper_wick = row["high"] - max(row["open"], row["close"])
        atr = row["atr"]

        dist_from_vwap = (row["close"] - row["vwap"]) / atr

        bullish_reject = (
            dist_from_vwap < -vwap_distance_atr
            and lower_wick > wick_body_ratio * body
            and lower_wick > wick_atr_ratio * atr
            and row["close"] > row["open"]
        )

        bearish_reject = (
            dist_from_vwap > vwap_distance_atr
            and upper_wick > wick_body_ratio * body
            and upper_wick > wick_atr_ratio * atr
            and row["close"] < row["open"]
        )

        # ---------------- ENTRY ----------------
        if position is None:
            if bullish_reject and row["ema_slope"] > -0.02 * atr:
                size = risk_per_trade / (sl_atr * atr)
                position = {
                    "dir": "long",
                    "entry": row["close"],
                    "sl": row["close"] - sl_atr * atr,
                    "tp": row["vwap"],   # mean target
                    "size": size,
                    "bars": 0
                }

            elif bearish_reject and row["ema_slope"] < 0.02 * atr:
                size = risk_per_trade / (sl_atr * atr)
                position = {
                    "dir": "short",
                    "entry": row["close"],
                    "sl": row["close"] + sl_atr * atr,
                    "tp": row["vwap"],
                    "size": size,
                    "bars": 0
                }

        # ---------------- EXIT ----------------
        else:
            position["bars"] += 1
            exit_price = None

            if position["dir"] == "long":
                if row["low"] <= position["sl"]:
                    exit_price = position["sl"]
                elif row["high"] >= position["tp"]:
                    exit_price = position["tp"]
            else:
                if row["high"] >= position["sl"]:
                    exit_price = position["sl"]
                elif row["low"] <= position["tp"]:
                    exit_price = position["tp"]

            if exit_price or position["bars"] >= max_hold_bars:
                if exit_price is None:
                    exit_price = row["close"]

                pnl = (
                    (exit_price - position["entry"])
                    if position["dir"] == "long"
                    else (position["entry"] - exit_price)
                ) * position["size"]

                capital += pnl
                trades.append({
                    "direction": position["dir"],
                    "pnl": pnl,
                    "bars": position["bars"]
                })
                position = None

        equity_curve.append(capital)

    return capital, equity_curve, trades
