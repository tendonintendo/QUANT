# Quantitative Finance Learning Journey

## Overview

This repository documents my personal journey into quantitative finance and algorithmic trading. As someone diving deeper into the world of trading, I've created this project to explore key concepts in quant finance, with a focus on modeling, simulation, backtesting, and other computer science principles applied to financial markets.

The project so far has been organized into four main areas:
- **Visualize**: Basic data visualization and analysis tools for market data
- **Modeling**: Exploring volatility modeling techniques like GARCH for cryptocurrency markets
- **Price Action Analysis**: Developing and validating a wick-based trading strategy using Monte Carlo simulation and statistical testing
- **Intraday VWAP Model**: Intraday mean-reversion strategy combining VWAP anchors with wick-based filters for SPY trading

This is an educational project aimed at understanding the complexities of financial markets through hands-on implementation rather than building production-ready trading systems.

## Project Structure

### Visualize/
Basic visualization tools for financial data analysis:
- `main.ipynb`: Jupyter notebook with price charts, moving averages, return distributions, and rolling volatility plots for cryptocurrency data

### Modeling/
Contains Jupyter notebooks exploring advanced financial modeling techniques:
- `garch.ipynb`: Implementation of GARCH (Generalized Autoregressive Conditional Heteroskedasticity) models for volatility forecasting in Bitcoin. Includes rolling volatility analysis, volatility regime classification, and multi-step ahead volatility predictions.

### Price Action Analysis/
A comprehensive research framework for testing wick-based candlestick trading strategies:
- `main.py`: Entry point for running the complete analysis pipeline
- `backtest.py`: Backtesting engine with risk management (stop losses, position sizing)
- `strategy.py`: Signal generation logic for wick-based price action patterns
- `monte_carlo.py`: Monte Carlo simulation using synthetic OHLC data to test for model bias
- `wick_signal_validation.py`: Statistical validation of signals using forward return analysis and permutation testing
- `mc_visualization.py`: Visualization tools for Monte Carlo results
- `config.py`: Configuration parameters for risk management and strategy settings

Key findings from this module:
- Monte Carlo simulations revealed strong model bias in synthetic data
- Real market data showed weak statistical significance for wick patterns
- Emphasizes the importance of rigorous statistical testing over curve-fitting

### Intraday VWAP Model/
An intraday mean-reversion trading strategy for SPY using 5-minute bars:
- `main.py`: Entry point for running the backtest and evaluation pipeline
- `backtest.py`: Backtesting engine with VWAP-based entries, wick filters, and risk management
- `data.py`: Data acquisition and preprocessing for intraday SPY data
- `evaluation.py`: Performance analysis, Monte Carlo robustness testing, and trade statistics

Key findings from this module:
- Wick patterns serve as effective contextual filters for mean-reversion setups
- VWAP provides a strong intraday fair-value anchor for profit targets
- Strategy exhibits asymmetric payoffs with bounded drawdowns and low win rate but high profit factor
- Emphasizes structural edges over pattern-based predictions in intraday trading

## Key Concepts Explored

### Modeling & Simulation
- **GARCH Models**: Capturing volatility clustering and persistence in financial time series
- **Monte Carlo Methods**: Generating synthetic market data to test strategy robustness
- **Volatility Regimes**: Classifying market conditions into low/medium/high volatility states

### Backtesting & Validation
- **Risk Management**: Position sizing, stop losses, and risk per trade controls
- **Statistical Testing**: Permutation tests for significance, forward return analysis
- **Bias Detection**: Separating genuine alpha from data-snooping and model overfitting

### Computer Science Applications
- **Data Structures**: Time series manipulation with pandas
- **Algorithms**: Signal generation, backtesting loops, statistical computations
- **Visualization**: Matplotlib for financial charts and analysis
- **APIs**: yfinance for market data retrieval

## Getting Started

### Prerequisites
- Python 3.11+
- Jupyter Notebook
- Required packages listed in `requirements.txt`

### Installation
```bash
pip install -r requirements.txt
```

### Running the Models
```bash
python main.py
```

This will execute the full pipeline: Monte Carlo simulation, backtesting, and evaluation.

### Exploring Models
Open the Jupyter notebooks in Modeling/ and Visualize/ to see interactive implementations of GARCH modeling and data visualization.

## Current Status

This project represents my ongoing learning process. Through rigorous research in the Price Action Analysis module, I learned that wick patterns alone lack standalone predictive power, emphasizing the need for statistical validation over curve-fitting. Building on these insights, the Intraday VWAP Model demonstrates how wick signals can serve as effective contextual filters in structured mean-reversion strategies, highlighting the importance of market structure and bounded risk management in developing survivable trading systems.

## Disclaimer

This is an educational project for learning purposes only. The strategies and models presented here are not intended for actual trading or investment decisions. Financial markets involve significant risk, and past performance does not guarantee future results.

## References & Learning Resources

- "Advances in Financial Machine Learning" by Marcos Lopez de Prado
- "Python for Data Analysis" by Wes McKinney
- Online courses on quantitative finance and algorithmic trading
- Academic papers on GARCH models and volatility forecasting

---

*This repository serves as both a practical toolkit and a learning diary for quantitative finance concepts.*