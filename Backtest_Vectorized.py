# Import necessary libraries
import yfinance as yf
import pandas as pd

# Function to get the ticker symbols of S&P 500 companies
def get_sp500_tickers():
    """
    Fetches the list of S&P 500 company ticker symbols from Wikipedia.
    
    Returns:
        List of ticker symbols.
    """
    # Specify the URL of the Wikipedia page
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    
    # Read the HTML tables into a list of DataFrame objects
    # The first DataFrame (index 0) contains the ticker symbols
    return pd.read_html(url)[0].Symbol.to_list()

# Download historical stock price data
def download_price_data(tickers, start_date):
    """
    Downloads historical stock price data for the provided ticker symbols.
    
    Args:
        tickers: List of stock ticker symbols.
        start_date: Start date for historical data.
        
    Returns:
        DataFrame containing historical stock price data.
    """
    # Using yfinance to download the historical stock price data
    return yf.download(tickers, start=start_date)

# Function to slice the price data for a specific stock symbol
def slice_stock_data(price_data, symbol):
    """
    Slices price data for a specific stock symbol.
    
    Args:
        price_data: DataFrame containing historical stock price data for multiple stocks.
        symbol: The stock symbol to slice data for.
        
    Returns:
        A DataFrame containing the historical stock price data for the specified stock symbol.
    """
    # Copy the data to avoid modifying the original DataFrame
    sliced_data = price_data.copy()
    
    # Filter the columns for the specific stock symbol
    sliced_data = sliced_data[sliced_data.columns[sliced_data.columns.get_level_values(1) == symbol]]
    
    # Drop the level containing the stock symbol
    sliced_data.columns = sliced_data.columns.droplevel(1)
    
    # Calculate the next day's opening price and add it as a new column
    sliced_data.loc[:, 'next_day_open'] = sliced_data.Open.shift(-1)
    
    return sliced_data

# Function to calculate Simple Moving Averages
def calculate_moving_averages(data, short_window, long_window):
    """
    Calculates simple moving averages.
    
    Args:
        data: DataFrame containing historical stock price data for a single stock.
        short_window: The window size for the short moving average.
        long_window: The window size for the long moving average.
    """
    # Calculate the short and long simple moving averages
    data['short_sma'] = data.Close.rolling(short_window).mean()
    data['long_sma'] = data.Close.rolling(long_window).mean()

# Vectorized backtesting function
def vectorized_backtest(data, short_window, long_window):
    """
    Performs vectorized backtesting.
    
    Args:
        data: DataFrame containing historical stock price data for a single stock.
        short_window: The window size for the short moving average.
        long_window: The window size for the long moving average.
        
    Returns:
        The cumulative gain.
    """
    # Calculate the moving averages
    calculate_moving_averages(data, short_window, long_window)
    
    # Determine the initial buy signal
    initial_buy = pd.Series(data.index == (data.short_sma > data.long_sma).idxmax(), index=data.index)
    
    # Determine the real signals
    real_signal = initial_buy | (data.short_sma > data.long_sma).diff()
    
       # Filter out the trades based on the signals
    trades = data[real_signal]

    # If there's an odd number of trades, we need to mark the last one to market
    if len(trades) % 2 != 0:
        mark_to_market = data.tail(1).copy()
        mark_to_market.next_day_open = mark_to_market.Close
        trades = pd.concat([trades, mark_to_market])
    
    # Calculate the profits for each pair of trades
    profits = trades.next_day_open.diff()[1::2] / trades.next_day_open[0::2].values
    
    # Calculate the cumulative gain
    return (profits + 1).prod()

# Main function to execute the script
def main():
    # Get S&P 500 tickers
    sp500_tickers = get_sp500_tickers()
    
    # Download historical stock price data
    historical_data = download_price_data(sp500_tickers, start_date='2020-01-01')
    
    # Prepare storage for the results
    results_train = []
    results_test = []

    # Loop through each stock symbol for backtesting
    for symbol in sp500_tickers:
        stock_data = slice_stock_data(historical_data, symbol)
        print(f'Result for {symbol}')
        
        # Split data into training and testing sets (60% train, 40% test)
        train_data = stock_data[:int(len(stock_data) * 0.6)].copy()
        test_data = stock_data[int(len(stock_data) * 0.6):].copy()
        
        # Perform vectorized backtesting on the training data and store the result
        train_result = vectorized_backtest(train_data, 50, 100)
        print(train_result)
        
        # Perform vectorized backtesting on the testing data and store the result
        test_result = vectorized_backtest(test_data, 50, 100)
        
        # Append the results to the lists
        results_train.append(train_result)
        results_test.append(test_result)

    # Create a DataFrame to store the profits
    profits = pd.DataFrame({'training_profit': results_train, 'testing_profit': results_test}, index=sp500_tickers)

    # Display the stocks with the highest training profits
    display(profits.nlargest(5, 'training_profit'))

# Execute main function
main()
