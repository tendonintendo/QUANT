from signals import wick_signal

def backtest(
    df,
    initial_capital,
    risk_per_trade,
    stop_loss_pct,
    wick_ratio
):
    capital = initial_capital
    equity_curve = [capital]
    trade_log = []

    position = None
    entry_price = None
    stop_price = None
    position_size = 0

    traded_blocks = set()

    for i in range(1, len(df)):
        candle = df.iloc[i]

        # EXIT LOGIC
        if position is not None:
            high = candle["high"]
            low = candle["low"]
            exited = False

            if position == "long":
                if low <= stop_price:
                    capital -= position_size * (entry_price - stop_price)
                    exited = True
                elif high >= entry_price * (1 + stop_loss_pct * 2):
                    capital += position_size * (entry_price * (1 + stop_loss_pct * 2) - entry_price)
                    exited = True

            equity_curve.append(capital)

            if exited:
                trade_log.append({
                    "entry_index": entry_index,
                    "exit_index": i,
                    "entry_price": entry_price,
                    "exit_price": capital,
                    "regime_block": candle["regime_block"],
                    "regime": candle["regime"],
                    "position": position
                })
                position = None
            continue

        # ENTRY LOGIC
        if candle["regime"] != "compression":
            equity_curve.append(capital)
            continue

        block_id = candle["regime_block"]

        if block_id in traded_blocks:
            equity_curve.append(capital)
            continue

        signal = wick_signal(df, i, wick_ratio)

        if signal != "long":
            equity_curve.append(capital)
            continue

        price = candle["open"]
        stop_price = price * (1 - stop_loss_pct)
        risk_amount = capital * risk_per_trade
        position_size = risk_amount / (price - stop_price)

        entry_price = price
        entry_index = i
        position = "long"
        traded_blocks.add(block_id)

        equity_curve.append(capital)

    return capital, equity_curve, trade_log
