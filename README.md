# Python Trading Toolkit

Python Trading Toolkit is a collection of scripts and tools for backtesting and analyzing trading strategies in Python. This toolkit includes various trading strategies, indicators, and backtesting mechanisms with historical data fetched from different sources.

## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Repository Structure](#repository-structure)
- [Usage](#usage)
  - [Backtesting S&P 500 Stocks](#backtesting-sp-500-stocks)
  - [Backtesting Cryptocurrency Trading Strategies](#backtesting-cryptocurrency-trading-strategies)
  - [Live Trading with Binance Trading Bot](#live-trading-with-binance-trading-bot)
  - [Screening Cryptocurrencies with Streamlit Web App](#screening-cryptocurrencies-with-streamlit-web-app)
  - [Checking Cryptocurrencies with Technical Indicators](#checking-cryptocurrencies-with-technical-indicators)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Getting Started

### Prerequisites

Before you start, you need to have Python installed on your machine. You can download Python [here](https://www.python.org/downloads/).

You will also need to install the following Python libraries:

- yfinance
- pandas
- backtrader
- binance-python
- streamlit

### Installation

You can install these libraries using pip:

pip install yfinance pandas backtrader binance-python streamlit

## Repository Structure

This repository contains several scripts and tools for trading. Here is a brief overview:

- `Backtest_Vectorized.py`: A script for backtesting trading strategies on S&P 500 stocks using vectorized backtesting.
- `crypto_trading_backtester.py`: A script for backtesting trading strategies on cryptocurrency data from Binance.
- `binance_trading_bot.py`: This script implements a simple trading bot that trades on Binance. It uses websockets to get real-time price data for Dogecoin. The trading strategy used is a simple one based on price momentum and uses preset profit target and stop loss levels.
- `binance_return_screener.py`: This script uses Streamlit to create a web application that allows the user to screen cryptocurrencies based on their return over a user-specified lookback period. The script fetches data from a local SQLite database that stores cryptocurrency price data.
- `binance_technical_indicator_checker.py`: This script screens cryptocurrencies based on two technical indicators: the Moving Average Convergence Divergence (MACD) and the Exponential Moving Average (EMA). The script checks if the MACD has crossed above the signal line and if the price is above the EMA, which are commonly used as buy signals in technical analysis. The script uses the Binance API to get price data and stores it in a local SQLite database.

## Usage

### Backtesting S&P 500 Stocks

python Backtest_Vectorized.py

This script will download historical price data of S&P 500 stocks and perform backtesting on this data using vectorized backtesting.

### Backtesting Cryptocurrency Trading Strategies

python crypto_trading_backtester.py


Before running this script, make sure to replace `YOUR_API_KEY` and `YOUR_API_SECRET` with your Binance API key and secret. This script fetches historical cryptocurrency data from Binance and performs backtesting using the Backtrader library.

### Live Trading with Binance Trading Bot

python binance_trading_bot.py


This script runs a trading bot for trading Dogecoin on Binance. The bot uses a simple momentum strategy and trades based on the price movement in the past 1 and 15 minutes.

### Screening Cryptocurrencies with Streamlit Web App

streamlit run binance_return_screener.py


This script creates a web application that screens cryptocurrencies based on their return over a specified lookback period. The data is fetched from a local SQLite database.

### Checking Cryptocurrencies with Technical Indicators

python binance_technical_indicator_checker.py


This script screens cryptocurrencies for buy signals based on two technical indicators: the Moving Average Convergence Divergence (MACD) and the Exponential Moving Average (EMA). It fetches data from a local SQLite database and prints the cryptocurrencies for which both conditions hold.

## Contributing

Contributions are welcome! Please feel free to submit a pull request.

## License

This project is licensed under the MIT License.

## Acknowledgements

- [yfinance](https://pypi.org/project/yfinance/) for providing historical stock price data.
- [Backtrader](https://www.backtrader.com/) for providing an awesome backtesting engine.
- [Binance API](https://binance-docs.github.io/apidocs/spot/en/) for providing historical cryptocurrency data.
- [Streamlit](https://streamlit.io/) for making it easy to create web applications for Python.



