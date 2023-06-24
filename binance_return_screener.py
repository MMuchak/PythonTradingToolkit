import streamlit as st
import pandas as pd
import datetime as dt
from sqlalchemy import create_engine

st.title('Welcome to the live Binance return screener')

# Establish a connection to the local SQLite database named 'CryptoDB.db'
engine = create_engine('sqlite:///CryptoDB.db')

# Fetch the names of all tables in the database. Each table name is considered a symbol.
symbols = pd.read_sql('SELECT name FROM sqlite_master WHERE type = "table"', engine).name.to_list()

# Streamlit creates a dropdown menu for the user to select the lookback period in minutes
lookback = st.selectbox('Pick the lookback in minutes', [1,15,30])

def qry(symbol, lookback):
    # This function queries data for a specific symbol for a specific lookback period from the database
    now = dt.datetime.utcnow()
    before = now - dt.timedelta(minutes=lookback)
    qry_str = f"""SELECT time,price From '{symbol}'
    WHERE time >= '{before}'"""
    df = pd.read_sql(qry_str, engine)
    df.time = pd.to_datetime(df.time)
    return df

def metrics(df):
    # This function calculates the cumulative return for the given DataFrame
    cum_ret = (df.price.pct_change() +1).prod() - 1
    return cum_ret


def allreturns():
    # This function iterates over all symbols and calculates their returns.
    returns = []
    for symbol in symbols:
        returns.append(metrics(qry(symbol,lookback)))
    
    return returns

# Calculate returns for all symbols once and store it in a DataFrame.
all_ret = pd.DataFrame(allreturns(), symbols, columns=['Performance'])

if st.button('Update'):
    all_ret = pd.DataFrame(allreturns(), symbols, columns=['Performance'])

# Fetch the top 10 and the worst 10 performers
top = all_ret.Performance.nlargest(10)
worst = all_ret.Performance.nsmallest(10)

# Display the top and worst performers in two separate columns
cols = st.columns(2)

cols[0].title('Top Performers')
cols[0].write(top)

cols[1].title('Worst Performers')
cols[1].write(worst)
