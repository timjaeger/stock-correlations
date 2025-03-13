
# Portfolio Correlation Analysis Tool

## Overview
This repository contains tools for analyzing financial securities with a focus on correlation analysis. The `correlations.py` script helps identify groups of securities with minimal correlation, useful for portfolio diversification.

## Dependencies
To run the scripts in this repository, you'll need the following Python packages:
- pandas
- numpy
- yfinance
- itertools (from standard library)

You can install the required packages using pip:
```
pip install pandas numpy yfinance
```

## How correlations.py Works

The `correlations.py` script analyzes correlations between different securities using historical price data from Yahoo Finance. It helps identify groups of securities that have low correlation with each other, which is valuable for portfolio diversification.

### Key Features:
1. Downloads historical price data for a list of securities
2. Calculates correlation matrix between all securities
3. Identifies the group of securities with the lowest average correlation using a Monte Carlo approach
4. Displays detailed correlation information for analysis

### Process Flow:
1. Define a list of stock/ETF tickers to analyze
2. Fetch historical closing price data from Yahoo Finance
3. Calculate daily returns for all securities
4. Generate a correlation matrix based on these returns
5. Use a Monte Carlo simulation to find the least correlated group of securities
6. Display detailed correlation metrics for the identified group

### Monte Carlo Approach:
The script uses a Monte Carlo approach to find the least correlated group of securities. This approach is used because checking all possible combinations would be computationally expensive. The script:
1. Randomly selects groups of securities
2. Calculates the average absolute correlation for each group
3. Repeats this process 1,000 times
4. Returns the group with the lowest average absolute correlation

## How to Run

Simply execute the script using Python:
```
python correlations.py
```

### Customization:
You can modify the script to analyze different securities by changing the `tickers` list at the beginning of the file:
```python
tickers = ['GDO', 'DX', 'MEGI', 'SLVO', 'NFLX', 'AAPL', 'GOOGL']
```

You can also adjust the date range by modifying:
```python
start_date = '2022-01-01'
end_date = '2025-01-15'
```

## Output
The script produces several outputs:
1. A list of valid symbols after cleaning (removing symbols with no data)
2. A full correlation matrix showing how all symbols correlate with each other
3. Pairwise correlations between each pair of symbols
4. A list of the least correlated symbols with their average correlation metrics

This information can be used to construct a diversified portfolio with reduced overall risk.
