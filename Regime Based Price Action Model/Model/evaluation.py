import numpy as np
import pandas as pd


def summarize_results(final_capital, equity_curve, initial_capital):
    """
    Compute basic performance statistics from equity curve.
    """
    equity = pd.Series(equity_curve)

    returns = equity.pct_change().dropna()

    total_return = final_capital - initial_capital

    if len(returns) == 0:
        win_rate = 0.0
        max_drawdown = 0.0
    else:
        win_rate = (returns > 0).mean()
        cumulative_max = equity.cummax()
        drawdowns = equity - cumulative_max
        max_drawdown = drawdowns.min()

    return {
        "Total Return": round(total_return, 2),
        "Win Rate": round(win_rate, 4),
        "Max Drawdown": round(max_drawdown, 2),
        "Trades": int((returns != 0).sum())
    }



def regime_performance(df):
    """
    Diagnostics only. No trading logic.
    """
    df = df.copy()
    df["ret"] = df["close"].pct_change()

    summary = []

    for regime, sub in df.groupby("regime"):
        avg_ret = sub["ret"].mean()
        vol = sub["ret"].std()
        count = len(sub)

        summary.append({
            "Regime": regime,
            "Observations": count,
            "Avg Daily Return": avg_ret,
            "Volatility": vol
        })

    return pd.DataFrame(summary)
