# Import necessary libraries
import datetime
import backtrader as bt
import yfinance as yf
import pandas as pd
from binance.client import Client

# NOTE: Replace 'YOUR_API_KEY' and 'YOUR_API_SECRET' with your Binance API key and secret
API_KEY = 'YOUR_API_KEY'
API_SECRET = 'YOUR_API_SECRET'

# Initialize Binance Client
client = Client(API_KEY, API_SECRET)

# Function to fetch historical data from Binance
def getdata(symbol, start):
    frame = pd.DataFrame(client.get_historical_klines(symbol,
                                                     '1d',
                                                     start))
    frame = frame.iloc[:,:6]
    frame.columns = ['Time','Open','High','Low','Close','Volume']
    frame.set_index('Time', inplace=True)
    frame.index = pd.to_datetime(frame.index,unit='ms')
    frame = frame.astype(float)
    return frame

# Fetch historical data for BTC/USDT pair from Binance
data = getdata('BTCUSDT','2021-01-01')

# Define the trading strategy class
class TestStrategy(bt.Strategy):
    # Define the parameters for optimization
    params = (
        ('sma_period', 200),
        ('bollinger_period', 20),
        ('bollinger_devfactor', 2.5),
        ('rsi_period', 2)
    )

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        ''' Initialize the strategy '''
        self.dataclose = self.datas[0].close
        self.order = None
        
        # Initialize indicators
        self.sma = bt.ind.SMA(period=self.params.sma_period)
        self.boll = bt.ind.BollingerBands(period=self.params.bollinger_period, devfactor=self.params.bollinger_devfactor)
        self.rsi = bt.ind.RSI(period=self.params.rsi_period, safediv=True)

    def notify_order(self, order):
        ''' Handle the events of order execution '''
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, %.2f' % order.executed.price)
            elif order.issell():
                self.log('SELL EXECUTED, %.2f' % order.executed.price)

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def next(self):
        ''' Define the core trading logic '''
        self.log('Close, %.2f' % self.dataclose[0])
        self.log('SMA, %.2f' % self.sma[0])
        self.log('Bollinger Bands, Top: %.2f, Mid: %.2f, Bot: %.2f' % (self.boll.lines.top[0], self.boll.lines.mid[0], self.boll.lines.bot[0]))
        self.log('RSI, %.2f' % self.rsi[0])

        if self.order:
            return

        if not self.position:
            if self.data.close > self.sma and self.data.close < self.boll.lines.bot:
                self.log('BUY CREATE, %.2f' % self.dataclose[0])
                self.order = self.buy(exectype = bt.Order.Limit, price = 0.97* self.dataclose[0])
        else:
            if self.rsi > 50 or len(self) >= (self.bar_executed + 10):
                self.log('SELL CREATE, %.2f' % self.dataclose[0])
                self.order = self.sell()

# Main function to run the backtesting
if __name__ == '__main__':
    # Create a cerebro entity
    cerebro = bt.Cerebro()

    # Add a strategy
    cerebro.addstrategy(TestStrategy)

    # Create a Data Feed
    data = bt.feeds.PandasData(dataname=data)

    # Add the Data Feed to Cerebro
    cerebro.adddata(data)

    # Set our desired cash start
    cerebro.broker.setcash(1000)

    # Set the commission - 0.5% ... divide by 100 to remove the percentage
    cerebro.broker.setcommission(commission=0.005)

    # Add a sizer based on the stake
    cerebro.addsizer(bt.sizers.PercentSizer, percents=100)

    # Print out the starting conditions
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Run over everything
    cerebro.run()

    # Print out the final result
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Plot the result
    cerebro.plot()
