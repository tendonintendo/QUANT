import pandas as pd
from data import load_ohlc
from backtest import backtest
from evaluation import (
    summarize_results,
    trade_sharpe,
    equity_sharpe,
    monte_carlo_trades,
    decompose_trades,
    trade_sequence_stats
)

# -------------------------------------------------
# Configuration
# -------------------------------------------------
SYMBOL = "SPY"

INITIAL_CAPITAL = 1000
RISK_PER_TRADE = 10

WICK_BODY_RATIO = 2.0
WICK_ATR_RATIO = 0.5

TP_ATR = 0.8
SL_ATR = 0.6
MAX_HOLD_BARS = 6

VWAP_DISTANCE_ATR = 1.2


# -------------------------------------------------
# Feature Engineering
# -------------------------------------------------
def prepare_features(df):
    df = df.copy()

    df["range"] = df["high"] - df["low"]
    df["atr"] = df["range"].rolling(14).mean()

    # VWAP (session-agnostic cumulative)
    df["vwap"] = (df["close"] * df["volume"]).cumsum() / df["volume"].cumsum()

    df["ema"] = df["close"].ewm(span=15).mean()
    df["ema_slope"] = df["ema"] - df["ema"].shift(5)

    return df


# -------------------------------------------------
# Main
# -------------------------------------------------
def main():
    # Load & prepare data
    df = load_ohlc(SYMBOL)
    df = prepare_features(df)
    df.dropna(inplace=True)

    # Run backtest
    final_capital, equity_curve, trades = backtest(
        df=df,
        initial_capital=INITIAL_CAPITAL,
        risk_per_trade=RISK_PER_TRADE,
        wick_body_ratio=WICK_BODY_RATIO,
        wick_atr_ratio=WICK_ATR_RATIO,
        tp_atr=TP_ATR,
        sl_atr=SL_ATR,
        max_hold_bars=MAX_HOLD_BARS,
        vwap_distance_atr=VWAP_DISTANCE_ATR,
    )

    trade_df = pd.DataFrame(trades)

    # ---------------- Results ----------------
    results = summarize_results(
        final_capital=final_capital,
        equity_curve=equity_curve,
        initial_capital=INITIAL_CAPITAL,
    )

    print("\n===== INTRADAY WICK + VWAP REVERSION =====")
    print(f"Final Capital: {final_capital:.2f}")

    for k, v in results.items():
        print(f"{k}: {v}")

    if not trade_df.empty:
        print("\nTrade diagnostics:")
        print(f"Trades: {len(trade_df)}")
        print(f"Win Rate: {(trade_df['pnl'] > 0).mean():.2%}")
        print(f"Avg Trade PnL: {trade_df['pnl'].mean():.2f}")
        print(f"Median Hold (bars): {trade_df['bars'].median()}")

    # ---------------- Evaluation ----------------
    print("\n===== EVALUATION =====")

    ts = trade_sharpe(trades, INITIAL_CAPITAL)
    es = equity_sharpe(equity_curve)

    print(f"Trade Sharpe: {ts:.2f}")
    print(f"Equity Sharpe: {es:.2f}")

    mc = monte_carlo_trades(trades, INITIAL_CAPITAL)

    if mc:
        print("\nMonte Carlo Results (Trades Resampled):")
        print(f"Mean Final Capital: {mc['mean_final_capital']:.2f}")
        print(f"Median Final Capital: {mc['median_final_capital']:.2f}")
        print(f"5th Percentile: {mc['5pct']:.2f}")
        print(f"95th Percentile: {mc['95pct']:.2f}")
        print(f"Probability of Loss: {mc['prob_loss']:.2%}")
    
    seq = trade_sequence_stats(trades)
    if seq:
        print("\n===== TRADE SEQUENCING =====")
        for k, v in seq.items():
            print(f"{k}: {v}")


    # ---------------- Decomposition ----------------
    print("\n===== WIN / LOSS DECOMPOSITION =====")

    breakdown = decompose_trades(trades)

    if breakdown:
        print(f"Total Trades: {breakdown['total_trades']}")
        print(f"Win Rate: {breakdown['win_rate']:.2%}")

        print("\n-- Winners --")
        print(f"Avg Win: {breakdown['avg_win']:.2f}")
        print(f"Median Win: {breakdown['median_win']:.2f}")
        print(f"Median Hold (bars): {breakdown['win_hold_bars']}")

        print("\n-- Losers --")
        print(f"Avg Loss: {breakdown['avg_loss']:.2f}")
        print(f"Median Loss: {breakdown['median_loss']:.2f}")
        print(f"Median Hold (bars): {breakdown['loss_hold_bars']}")

        print(f"\nProfit Factor: {breakdown['profit_factor']:.2f}")



if __name__ == "__main__":
    main()
