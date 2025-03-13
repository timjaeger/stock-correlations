import pandas as pd
import yfinance as yf
import numpy as np
from itertools import combinations

# Define tickers and period
tickers = ['GDO', 'DX', 'MEGI', 'SLVO', 'NFLX', 'AAPL', 'GOOGL']
start_date = '2022-01-01'
end_date = '2025-01-15'

# Fetch historical data with error handling and improved compatibility
try:
    print("Attempting to download data from Yahoo Finance...")
    # In yfinance 0.2.54+, auto_adjust=True by default, so Close is already adjusted
    data = yf.download(tickers,
                       start=start_date,
                       end=end_date,
                       progress=True,
                       ignore_tz=True)['Close']
    print(f"Download completed. Data shape: {data.shape}")
except KeyError:
    # Fallback for older versions that might still have 'Adj Close'
    try:
        data = yf.download(tickers,
                           start=start_date,
                           end=end_date,
                           progress=True,
                           ignore_tz=True)['Adj Close']
    except Exception as e:
        print(f"Error downloading data: {str(e)}")
        # Create an empty DataFrame if download fails completely
        data = pd.DataFrame()

# Remove columns (symbols) with all NaN values
data = data.dropna(axis=1, how='all')

# Print remaining symbols after cleaning
valid_symbols = data.columns.tolist()
print(f"\nValid symbols after cleaning: {len(valid_symbols)}")
print("Symbols:", ', '.join(valid_symbols))

# Calculate daily returns (with NaN handling)
returns = data.pct_change(fill_method=None).dropna()

# Calculate correlation matrix
correlation_matrix = returns.corr()

# Print the correlation matrix
print("\nCorrelation Matrix:")
print("-" * 60)
pd.set_option('display.precision',
              3)  # Set display precision for better readability
print(correlation_matrix)
print("-" * 60)

# Print specific correlations between pairs of symbols
print("\nPairwise Correlations:")
for symbol1, symbol2 in combinations(correlation_matrix.columns, 2):
    corr_value = correlation_matrix.loc[symbol1, symbol2]
    print(f"{symbol1} <-> {symbol2}: {corr_value:.3f}")
print("-" * 60)


def find_least_correlated_group(correlation_matrix, group_size=len(tickers)):
    """
    Find a group of symbols with the lowest average absolute correlation.

    Ranking Method:
    1. Randomly select a group of symbols of the specified size
    2. Calculate the correlation sub-matrix for just those symbols
    3. Extract the upper triangle of the correlation matrix (excluding diagonal)
    4. Calculate the average of the absolute correlation values
    5. Repeat this process multiple times (1000 iterations)
    6. Return the group with the lowest average absolute correlation

    This Monte Carlo approach is used because finding the optimal solution
    would require checking all possible combinations, which grows exponentially
    with the number of symbols.

    Parameters:
    - correlation_matrix: DataFrame containing correlations between all symbols
    - group_size: Number of symbols to include in the least correlated group

    Returns:
    - best_group: List of symbols with lowest average absolute correlation
    - lowest_avg_correlation: The average absolute correlation value for this group
    """
    if len(correlation_matrix) < group_size:
        print(
            f"Warning: Only {len(correlation_matrix)} valid symbols available")
        group_size = min(group_size, len(correlation_matrix))

    symbols = correlation_matrix.columns
    best_group = None
    lowest_avg_correlation = float('inf')

    # Perform Monte Carlo sampling to find least correlated group
    for _ in range(1000):  # Try 1000 random combinations
        # Randomly select a group of symbols
        group = list(np.random.choice(symbols, size=group_size, replace=False))

        # Get the correlation sub-matrix for just this group
        group_corr = correlation_matrix.loc[group, group]

        # Calculate average of absolute correlations (upper triangle only, excluding diagonal)
        # np.triu_indices_from(group_corr, k=1) gets indices of upper triangle excluding diagonal
        avg_corr = np.abs(group_corr.values[np.triu_indices_from(group_corr,
                                                                 k=1)]).mean()

        # Keep track of the best group found so far
        if avg_corr < lowest_avg_correlation:
            lowest_avg_correlation = avg_corr
            best_group = group

    return best_group, lowest_avg_correlation


# Find the least correlated group with group_size equal to the length of tickers
least_correlated_group, avg_correlation = find_least_correlated_group(
    correlation_matrix, group_size=len(tickers))

if least_correlated_group:
    print("\nLeast Correlated Symbols Group:")
    print("-" * 40)

    # Calculate average correlation for each symbol with other symbols in the group
    print("Symbol  |  Avg Correlation")
    print("-" * 40)

    for symbol in least_correlated_group:
        # Get correlations of this symbol with all other symbols in the group
        correlations = []
        for other_symbol in least_correlated_group:
            if other_symbol != symbol:
                corr_value = correlation_matrix.loc[symbol, other_symbol]
                correlations.append(corr_value)

        # Calculate average absolute correlation for this symbol
        avg_symbol_corr = np.mean(np.abs(correlations))

        print(f"{symbol:6} |  {avg_symbol_corr:.4f}")

    print("-" * 40)
    print(f"Group's average absolute correlation: {avg_correlation:.4f}")
else:
    print("\nError: Could not find valid group of symbols")
