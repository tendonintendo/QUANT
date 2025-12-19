from strategy import generate_signal
from config import (
    RISK_PER_TRADE,
    STOP_LOSS_PCT,
    R_MULTIPLE
)


def backtest(df, initial_capital, wick_ratio, strong_ratio):
    capital = initial_capital
    equity_curve = [capital]

    position = None
    entry_price = None
    stop_price = None
    take_profit = None
    position_size = 0
    entry_index = None

    pending_signal = None   # stores ("long"/"short", signal_index)

    for i in range(len(df) - 3):
        candle = df.iloc[i]

        # ─────────────────────────────
        # HANDLE PENDING ENTRY
        # ─────────────────────────────
        if position is None and pending_signal is not None:
            direction, signal_idx = pending_signal

            # execute entry NOW (no future info)
            price = candle["open"]

            if direction == "long":
                stop_price = price * (1 - STOP_LOSS_PCT)
                take_profit = price * (1 + STOP_LOSS_PCT * R_MULTIPLE)
                risk_amount = capital * RISK_PER_TRADE
                position_size = risk_amount / (price - stop_price)

            else:
                stop_price = price * (1 + STOP_LOSS_PCT)
                take_profit = price * (1 - STOP_LOSS_PCT * R_MULTIPLE)
                risk_amount = capital * RISK_PER_TRADE
                position_size = risk_amount / (stop_price - price)

            position = direction
            entry_price = price
            entry_index = i
            pending_signal = None

        # ─────────────────────────────
        # SIGNAL DETECTION
        # ─────────────────────────────
        if position is None and pending_signal is None:
            signal = generate_signal(df, i, wick_ratio, strong_ratio)

            # STRONG SIGNAL → ENTER NEXT CANDLE
            if signal == "long":
                pending_signal = ("long", i)

            elif signal == "short":
                pending_signal = ("short", i)

            # WEAK SIGNAL → WAIT FOR CONFIRMATION
            elif signal == "confirm_long":
                if df.iloc[i + 1]["close"] > df.iloc[i + 1]["open"]:
                    pending_signal = ("long", i + 1)

            elif signal == "confirm_short":
                if df.iloc[i + 1]["close"] < df.iloc[i + 1]["open"]:
                    pending_signal = ("short", i + 1)

        # ─────────────────────────────
        # EXIT LOGIC
        # ─────────────────────────────
        elif position is not None:
            if i == entry_index:
                equity_curve.append(capital)
                continue

            high = candle["high"]
            low = candle["low"]

            if position == "long":
                if low <= stop_price:
                    capital -= position_size * (entry_price - stop_price)
                    position = None
                elif high >= take_profit:
                    capital += position_size * (take_profit - entry_price)
                    position = None

            elif position == "short":
                if high >= stop_price:
                    capital -= position_size * (stop_price - entry_price)
                    position = None
                elif low <= take_profit:
                    capital += position_size * (entry_price - take_profit)
                    position = None

        equity_curve.append(capital)

    return capital, equity_curve
