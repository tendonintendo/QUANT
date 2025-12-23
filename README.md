# Quantitative Market Microstructure and Signal Invalidation
**Author:** Muhammad Rengga Putra Kuncoro  
**Focus:** Statistical Inference, Monte Carlo Simulations, and Intraday Structural Alpha

## Executive Summary
This repository contains a two-part quantitative study on market efficiency and the statistical validity of technical signals. The project transitions from invalidating structural biases in common price action heuristics to engineering a robust mean-reversion framework anchored by institutional value metrics (VWAP).

### Key Research Findings
* **Signal Invalidation:** Demonstrated that standalone wick-based patterns fail to reject the null hypothesis (p = 0.6456). Apparent alpha in initial simulations was identified as a structural artifact of entry/exit framing rather than predictive power.
* **Integrated Alpha:** Developed a VWAP-anchored mean reversion model yielding a Profit Factor of 2.25 and a statistically significant edge (p = 0.039).
* **Risk Management:** Achieved a 96.1% Probability of Profit across 1,000 Monte Carlo path resamples, confirming the robustness of the integrated system.

---

## Repository Structure

### Part 1: Statistical Validation of Price Action Signals
* **Objective:** Test the predictive validity of wick-based candlestick patterns.
* **Methodology:** Permutation Testing and Monte Carlo Bias Detection using 15 years of SPY ETF data.
* **Key Result:** High win rates on stochastic synthetic data identified "False Alpha" inherent in the signal's logic.



### Part 2: Integrated Alpha via VWAP Mean Reversion
* **Objective:** Engineering a tradable system by combining price exhaustion with structural anchors.
* **Methodology:** Asymmetric Payoff Decomposition on 5-minute intraday intervals.
* **Key Result:** Exploited volatility elasticity to create a positively skewed PnL distribution with a median win-to-loss duration ratio of 6:1.



---

## Tech Stack and Methodology
* **Language:** Python (Pandas, NumPy, SciPy, Matplotlib)
* **Statistical Frameworks:**
    * **Stochastic Synthetic Control Groups:** Used for generating neutral OHLC data to isolate logic-based bias.
    * **Permutation Testing:** Used to calculate exact p-values against randomized baselines.
    * **Monte Carlo Resampling:** Used to assess path dependency and maximum drawdown robustness.

---

## Literature Review and Academic Benchmarks

### Part 1: Technical Analysis and Market Efficiency
* **Marshall, Young, and Rose (2006):** Utilized bootstrap methodologies across Dow Jones components and explicitly failed to find statistically significant excess returns from candlestick signals, concluding they do not create value in efficient markets.
* **Aronson (2011):** Emphasizes that many technical signals are the result of Data Mining Bias. This research utilizes the "Scientific Method" approach advocated by Aronson to move beyond objective statistical inference.
* **Jamaloodeen, Heinz, and Pollacia (2018):** Conducted a statistical analysis confirming that while wicks (price extremes) may encode minor information, the observed effects remain small, temporary, and insufficient for robust trading profitability.

### Part 2: Mean Reversion and Structural Alpha
* **Nassar and Ephrem (2020):** In Mean Reversion: A New Approach, the authors argue that price movements are overextensions from a volume-weighted equilibrium. Our results, specifically the rapid 10-minute median hold, validate their velocity of reversion thesis.
* **Bhattacharyya (2024):** Design and Development of Mean Reversion Strategies emphasizes convexity over win rate. Our Trade Sharpe (0.22) and Profit Factor (2.25) align with the performance profiles of modern intraday mean-reversion algorithms that prioritize risk-to-reward ratios.
* **Leung and Li (2015):** In Optimal Mean Reversion Trading, the authors provide a framework for Optimal Stopping. Our data shows that winners take 6x longer to develop than losers, suggesting that mean reversion is a process of decay back to the VWAP anchor.

---

## Future Research Directions
* **Uncertainty Quantification:** Implementing Conformal Prediction to generate adaptive confidence intervals for mean-reversion targets, ensuring guaranteed coverage.
* **Order Flow Integration:** Incorporating Volume Profile and Cumulative Delta to refine signal exhaustion points.
* **High-Performance Backtesting:** Porting the simulation engine to C++ to evaluate nanosecond-level latency and high-frequency execution effects.

---
*Disclaimer: This repository is for research and educational purposes only. Quantitative models involve significant risk and past performance is not indicative of future results.*
