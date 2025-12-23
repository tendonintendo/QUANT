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
* **Marshall, Young, and Rose (2006):** Utilized bootstrap methodologies across Dow Jones components and explicitly failed to find statistically significant excess returns from candlestick signals.
* **Aronson (2011):** Emphasizes that many technical signals are the result of Data Mining Bias; utilizes the Scientific Method to move beyond anecdotal patterns.
* **Jamaloodeen, Heinz, and Pollacia (2018):** Statistical analysis confirming that observed effects of price extremes remain insufficient for robust trading profitability.

### Part 2: Mean Reversion and Structural Alpha
* **Nassar and Ephrem (2020):** Argues that price movements are overextensions from a volume-weighted equilibrium; validates the velocity of reversion thesis.
* **Bhattacharyya (2024):** Emphasizes convexity and risk-to-reward ratios in modern intraday mean-reversion algorithms.
* **Leung and Li (2015):** Provides a framework for Optimal Stopping, consistent with our findings on winning trade decay.

---

## Future Research Directions
* **Uncertainty Quantification in ML:** Exploring methods like **Conformal Prediction** to generate statistically guaranteed confidence intervals for predictive models.
* **Reliable Distributed Simulation:** Porting logic engines to **C++** to handle high-concurrency event-driven simulations with nanosecond precision.
* **Order Flow Dynamics:** Incorporating Volume Profile and Cumulative Delta to refine signal exhaustion points in high-volatility regimes.

---
*Disclaimer: This repository is for research and educational purposes only. Quantitative models involve significant risk and past performance is not indicative of future results.*
