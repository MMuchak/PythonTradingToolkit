rom binance import Client
from sqlalchemy import create_engine
import pandas as pd
import ta
import numpy as np
import os
from tqdm import tqdm

# Load keys from environment variables. Ensure these are set in the environment where you're running this script.
api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")

# Create connection to SQLite database
engine = create_engine('sqlite:///CryptoDB.db')

# Create Binance client using API keys
client = Client(api_key, api_secret)

def apply_technicals(df):
    """
    Apply MACD and EMA technical indicators to the dataframe.
    """
    df['macd'] = ta.trend.macd_diff(df.c)
    df['EMA100'] = ta.trend.ema_indicator(df.c, window=10)
    return df.dropna()

def check(df):
    """
    Check if the MACD crossover condition and the price above EMA condition are met.
    """
    if np.sign(df.macd).diff().tail(1).values == 2 and \
    df.EMA100.tail(1).values < df.c.tail(1).values:
        return True
    return False

# Get list of all symbol tables in the database
symbols = pd.read_sql("""SELECT name FROM sqlite_master WHERE type = 'table'""",engine).name

# Filter out symbols that contain certain strings
symbols = symbols[~(symbols.str.contains('UP|DOWN|BULL|BEAR|TUSD|GBP|BUSD|EUR', regex=True))]

# This list will hold the symbols for which the check passes
positive_symbols = []

# Iterate over all symbols, apply technical indicators, and run the check
for symbol in tqdm(symbols):
    df = pd.read_sql(symbol, engine)
    df = apply_technicals(df)
    if check(df):
        positive_symbols.append(symbol)

# Print all symbols for which the check passed
print(f'Symbols with positive MACD crossover and price above EMA: {positive_symbols}')
