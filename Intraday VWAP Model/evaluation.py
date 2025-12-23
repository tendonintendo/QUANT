import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_strategy_results(df, equity_curve, trades):
    IMAGE_DIR = "./images/"
    if not os.path.exists(IMAGE_DIR):
        os.makedirs(IMAGE_DIR)

    # 1. Equity Curve Plot
    plt.figure(figsize=(12, 6))
    plt.plot(equity_curve, label='Equity Curve', color='blue')
    plt.title('Intraday Strategy Performance (SPY)')
    plt.ylabel('Capital')
    plt.grid(True, alpha=0.3)
    plt.savefig(f"{IMAGE_DIR}equity_curve.png")
    
    # 2. Trade Distribution (Asymmetry)
    pnls = [t['pnl'] for t in trades]
    plt.figure(figsize=(10, 5))
    plt.hist(pnls, bins=20, color='skyblue', edgecolor='black')
    plt.axvline(0, color='red', linestyle='--')
    plt.title('Trade PnL Distribution (Asymmetric Payoff)')
    plt.savefig(f"{IMAGE_DIR}trade_distribution.png")

def trade_sequence_stats(trades):
    """
    Analyze loss streaks, win streaks, and recovery behavior.
    """
    if not trades:
        return None

    pnls = np.array([t["pnl"] for t in trades])
    wins = pnls > 0

    max_loss_streak = 0
    max_win_streak = 0
    current_loss = 0
    current_win = 0

    for w in wins:
        if w:
            current_win += 1
            current_loss = 0
        else:
            current_loss += 1
            current_win = 0

        max_loss_streak = max(max_loss_streak, current_loss)
        max_win_streak = max(max_win_streak, current_win)

    equity = np.cumsum(pnls)
    peak = equity[0]
    drawdowns = []
    dd_start = None

    for i, e in enumerate(equity):
        if e >= peak:
            if dd_start is not None:
                drawdowns.append(i - dd_start)
                dd_start = None
            peak = e
        else:
            if dd_start is None:
                dd_start = i

    avg_recovery = np.mean(drawdowns) if drawdowns else 0
    max_recovery = np.max(drawdowns) if drawdowns else 0

    return {
        "Max Consecutive Losses": int(max_loss_streak),
        "Max Consecutive Wins": int(max_win_streak),
        "Avg Drawdown Recovery (trades)": round(avg_recovery, 2),
        "Max Drawdown Recovery (trades)": int(max_recovery),
    }

def decompose_trades(trades):
    """
    Break down winners vs losers.
    Returns a dict of descriptive stats.
    """
    if not trades:
        return None

    df = pd.DataFrame(trades)

    winners = df[df["pnl"] > 0]
    losers = df[df["pnl"] <= 0]

    stats = {
        "total_trades": len(df),

        "win_rate": len(winners) / len(df),

        "avg_win": winners["pnl"].mean() if not winners.empty else 0.0,
        "avg_loss": losers["pnl"].mean() if not losers.empty else 0.0,

        "median_win": winners["pnl"].median() if not winners.empty else 0.0,
        "median_loss": losers["pnl"].median() if not losers.empty else 0.0,

        "win_hold_bars": winners["bars"].median() if not winners.empty else 0,
        "loss_hold_bars": losers["bars"].median() if not losers.empty else 0,

        "profit_factor": (
            winners["pnl"].sum() / abs(losers["pnl"].sum())
            if not losers.empty else np.inf
        ),
    }

    return stats

def sharpe_ratio(returns, risk_free=0.0):
    """
    Generic Sharpe Ratio.
    returns: array-like of returns (not prices)
    """
    returns = np.asarray(returns)
    if len(returns) < 2:
        return 0.0

    excess = returns - risk_free
    std = excess.std(ddof=1)

    if std == 0:
        return 0.0

    return excess.mean() / std

def equity_sharpe(equity_curve):
    equity = np.asarray(equity_curve)
    returns = np.diff(equity) / equity[:-1]

    if len(returns) < 2:
        return 0.0

    return sharpe_ratio(returns)

def trade_sharpe(trades, initial_capital):
    if len(trades) < 2:
        return 0.0

    pnls = np.array([t["pnl"] for t in trades])
    returns = pnls / initial_capital

    return sharpe_ratio(returns)

def monte_carlo_trades(
    trades,
    initial_capital,
    n_simulations=1000,
    seed=42
):
    rng = np.random.default_rng(seed)

    pnls = np.array([t["pnl"] for t in trades])
    if len(pnls) == 0:
        return None

    final_capitals = []

    for _ in range(n_simulations):
        sampled = rng.choice(pnls, size=len(pnls), replace=True)
        final_capitals.append(initial_capital + sampled.sum())

    final_capitals = np.array(final_capitals)

    return {
        "mean_final_capital": final_capitals.mean(),
        "median_final_capital": np.median(final_capitals),
        "5pct": np.percentile(final_capitals, 5),
        "95pct": np.percentile(final_capitals, 95),
        "prob_loss": (final_capitals < initial_capital).mean(),
    }

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
