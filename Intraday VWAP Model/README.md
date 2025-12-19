# Intraday Wick + VWAP Mean Reversion Strategy  
## Research Extension, Model Construction, and Evaluation

**Date:** 19/12/2025  
**Data Window:** Last 60 trading days  

---

## Overview

This project extends prior research on wick-based price action signals into a **fully specified intraday trading model**.  

The previous research established that **wick patterns alone do not possess standalone predictive power** when evaluated using forward returns, permutation tests, and synthetic Monte Carlo simulations. However, that research also suggested an important insight:

> Wick signals may be useful **as contextual filters**, rather than as directional predictors.

This project operationalizes that insight by embedding wick rejection behavior into an **intraday VWAP mean-reversion framework**, with explicit risk controls and trade management.

The goal is not to optimize Sharpe ratio, but to construct a **structurally sound intraday strategy** with asymmetric payoff characteristics and bounded downside.

---

## Relationship to Previous Research

### What We Learned Previously in Price Action Analysis

From the prior wick-based research:

- Wick signals **do not generate statistically significant forward returns on their own**
- Apparent profitability in synthetic Monte Carlo tests was caused by **structural bias**
- Real market data showed:
  - Weak drift
  - Low signal frequency
  - Strong asymmetry between long and short behavior
- Wick patterns are better suited as **filters or context**, not entries

### How This Project Uses Those Results

This model **does not assume wicks predict direction**.

Instead:

- Wicks are treated as **rejection signals**
- Trades are only taken when price is **extended from VWAP**
- The target is **mean reversion**, not continuation
- Directional bias is controlled using:
  - VWAP distance
  - EMA slope (trend context)
  - Fixed risk and asymmetric exits

In short:  
> The wick is not the edge — **the market structure is**.

---

## Model Description

### Strategy Type

- **Intraday mean reversion**
- Instrument: **SPY**
- Timeframe: Intraday (5-minute bars)
- Holding period: Short (1–6 bars)

---

## Key Components

### 1. VWAP (Volume-Weighted Average Price)

VWAP represents the average price traded throughout the session, weighted by volume:

\[
VWAP = \frac{\sum (Price \times Volume)}{\sum Volume}
\]

Market participants (especially institutions) commonly treat VWAP as a **fair value anchor**.

In this model:

- Price far above VWAP → potential short mean reversion
- Price far below VWAP → potential long mean reversion
- VWAP is used as the **primary take-profit target**

---

### 2. Wick Rejection Logic (Contextual Filter)

A trade is only considered when:

- Price is sufficiently far from VWAP (measured in ATR units)
- The candle exhibits a **large wick relative to its body**
- The wick is large relative to recent volatility (ATR)

This captures **failed price extension**, not directional prediction.

---

### 3. Trend Constraint (EMA Slope)

To avoid fading strong trends:

- Long trades are suppressed if downside momentum is strong
- Short trades are suppressed if upside momentum is strong

This aligns with earlier findings that wick signals degrade in trending regimes.

---

### 4. Risk Management

- Fixed dollar risk per trade
- Stop loss defined in ATR units
- Profit target set at VWAP
- Maximum holding time enforced

This ensures:

- Losses are small and consistent
- Wins are allowed to expand naturally

---

## Backtest Summary

### Core Performance Metrics

| Metric | Value |
|------|------|
| Final Capital | 1352.24 |
| Total Return | +352.24 |
| Trades | 51 |
| Max Drawdown | -72.77 |

---

### Trade Statistics

| Metric | Value |
|------|------|
| Win Rate | 37.25% |
| Avg Trade PnL | +6.91 |
| Median Hold | 2 bars |

Despite a low win rate, average wins are significantly larger than losses.

---

## Risk & Robustness Evaluation

### Sharpe Ratios

| Metric | Value |
|------|------|
| Trade Sharpe | 0.20 |
| Equity Sharpe | 0.02 |

Interpretation:

- Returns are **highly skewed**
- Equity curve is jump-driven rather than smooth
- Sharpe ratio is not an appropriate primary metric for this payoff structure

---

### Monte Carlo Analysis (Trade Resampling)

| Metric | Value |
|------|------|
| Mean Final Capital | 1351.90 |
| Median Final Capital | 1329.12 |
| 5th Percentile | 980.99 |
| 95th Percentile | 1808.46 |
| Probability of Loss | 5.80% |

Interpretation:

- The strategy is robust to trade sequencing
- Downside is bounded
- Upside is asymmetric
- Most random permutations remain profitable

---

## Trade Behavior Decomposition

### Winners vs Losers

| Category | Value |
|--------|------|
| Avg Win | +35.38 |
| Avg Loss | -10.00 |
| Profit Factor | 2.10 |

---

### Holding Time Asymmetry

| Trade Type | Median Hold |
|----------|-------------|
| Winners | 6 bars |
| Losers | 1 bar |

This is a hallmark of well-constructed mean-reversion systems:

- Losses are rejected quickly
- Winners are given time to revert fully

---

### Trade Sequencing

| Metric | Value |
|------|------|
| Max Consecutive Losses | 5 |
| Max Consecutive Wins | 3 |
| Avg Recovery (trades) | 4.43 |
| Max Recovery | 11 |

This confirms the strategy is **psychologically and financially survivable**.

---

## Final Conclusions

- Wick patterns alone do not produce alpha  
- Wick behavior becomes useful when **anchored to market structure**
- VWAP provides a strong intraday mean-reversion reference
- The resulting strategy:
  - Has low win rate but strong payoff asymmetry
  - Exhibits bounded drawdowns
  - Is robust under Monte Carlo resampling
- Low Sharpe is expected and acceptable given return skew

---

## Key Takeaways

- Edge comes from **structure, not patterns**
- Mean-reversion strategies should be evaluated using:
  - Profit factor
  - Drawdown
  - Monte Carlo robustness
- Sharpe ratio is not suitable for fat-tailed intraday systems
- Wick signals are best used as **filters**, not forecasts

---

## Status

This repository represents a **completed research cycle**:

- Hypothesis → testing → rejection → reframing → implementation → evaluation

Further work could include:

- Walk-forward validation
- Regime segmentation
- Execution modeling and slippage analysis

But as a research artifact, this model is **complete and internally consistent**.
