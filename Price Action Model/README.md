# Wick-Based Price Action Strategy  
## Research Summary and Validation Notes

## Overview

This project investigates a wick-based price action trading idea using both synthetic data and real market data. The goal is not to immediately build a profitable strategy, but to rigorously test whether wick-based candlestick patterns contain statistically meaningful predictive information.

The research combines Monte Carlo simulation, forward return analysis, and permutation testing to separate structural bias from genuine signal.

---

## 1. Monte Carlo Simulation Using Synthetic OHLC Data

### Objective

Monte Carlo simulation is used to evaluate how the strategy behaves when prices are generated from a stochastic process without embedded market structure.

### Summary Results

| Metric | Result |
|------|-------|
| Mean Final Capital | ~1100+ |
| Median Final Capital | ~1100+ |
| Win Rate | ~90 percent |
| Equity Curve | Smooth, upward sloping |

### Interpretation

The strategy performs unrealistically well on synthetic data. Equity curves exhibit near-linear growth and extremely high win rates. Since the data contains no real market structure, this behavior indicates model bias rather than true alpha.

Conclusion: Monte Carlo results alone are insufficient for validating a trading strategy.

---

## 2. Wick Signal Frequency on Real Market Data

| Signal Type | Frequency |
|------------|-----------|
| Long Signals | 3.56 percent |
| Short Signals | 1.85 percent |

Interpretation:
Signals are rare and selective. There is a clear long-side dominance, suggesting a directional market bias rather than a symmetric signal.

---

## 3. Forward Return Analysis

### Long Signals

| Horizon | Mean Return | Win Rate | Count |
|--------|-------------|----------|-------|
| 1 Day | +0.024 percent | 57.0 percent | 142 |
| 3 Days | +0.186 percent | 59.2 percent | 142 |
| 5 Days | +0.361 percent | 66.9 percent | 142 |

### Short Signals

| Horizon | Mean Return | Win Rate | Count |
|--------|-------------|----------|-------|
| 1 Day | -0.061 percent | 41.9 percent | 74 |
| 3 Days | -0.142 percent | 40.5 percent | 74 |
| 5 Days | -0.307 percent | 41.9 percent | 74 |

Interpretation:
Long signals show increasing positive drift with longer holding horizons. Short signals are weaker and inconsistent. This asymmetry is consistent with long-term equity market drift rather than a strong directional candle-based edge.

---

## 4. Forward Return Distribution

The one-day forward return distribution for both long and short signals is tightly centered around zero and closely approximates a normal distribution. Any observed edge is extremely small in magnitude.

---

## 5. Permutation Test for Statistical Significance

### Long Signal One-Day Horizon

| Metric | Value |
|-------|-------|
| Observed Mean Difference | -0.000339 |
| p-value | 0.6436 |

Interpretation:
The high p-value indicates that the observed performance is statistically indistinguishable from random chance. The null hypothesis cannot be rejected.

---

## Final Conclusions

- Wick-based candlestick signals do not exhibit standalone predictive power
- Apparent profitability in Monte Carlo testing is driven by structural bias
- Real market data shows weak effects that fail statistical significance tests
- No reliable directional alpha is detected

---

## Key Takeaways

- Monte Carlo profitability does not imply real-world edge
- Forward return analysis is more informative than cumulative equity curves
- Statistical testing is essential to avoid false conclusions
- Wick patterns are better suited as contextual or filtering signals rather than standalone entries

This repository serves as a research framework for further experimentation, including regime filters, volatility conditioning, and walk-forward validation.
