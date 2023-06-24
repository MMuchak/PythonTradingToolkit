import websocket
import json
import pandas as pd
import logging

# Constants
ENDPOINT = 'wss://stream.binance.com:9443/ws'  # Binance websocket endpoint
PROFIT_TARGET_FACTOR = 1.002  # Profit target factor (0.2% profit target)
STOP_LOSS_FACTOR = 0.998  # Stop loss factor (0.2% stop loss)
SUBSCRIPTION_MESSAGE = json.dumps({
    'method': 'SUBSCRIBE',
    "params": ["dogeusdt@kline_1m", "dogeusdt@kline_15m"],
    'id': 1
})  # Message to subscribe to Binance streams

# Set up logging
logging.basicConfig(level=logging.INFO)

class TradingBot:
    def __init__(self):
        self.returns = {'1m': 0, '15m': 0}  # Store returns for 1m and 15m
        self.in_position = False  # Track if we are currently holding the coin
        self.buy_price = None  # Store the price at which we bought the coin

    def on_open(self, ws):
        """Function to execute when the websocket is opened."""
        ws.send(SUBSCRIPTION_MESSAGE)

    def on_message(self, ws, message):
        """Function to execute when a message is received from the websocket."""
        # Parse message JSON
        out = json.loads(message)

        # Create DataFrame from message
        df_ = pd.DataFrame(out['k'], index=[pd.to_datetime(out['E'], unit='ms')])[['s','i','o','c']]
        df_['ret ' + df_.i.values[0]] = float(df_.c) / float(df_.o) - 1
        self.returns[df_.i.values[0]] = float(df_.c) / float(df_.o) - 1
        logging.info(df_)

        # If not currently in position and 15m return is negative and 1m return is positive, buy
        if not self.in_position and self.returns['15m'] < 0 and self.returns['1m'] > 0:
            self.buy_price = float(df_.c)
            self.in_position = True
            logging.info('Bought at price: %s', self.buy_price)

        # If in position, check if it is time to sell
        if self.in_position:
            logging.info('In position, checking if it is time to sell...')
            target_profit = self.buy_price * PROFIT_TARGET_FACTOR
            stop_loss = self.buy_price * STOP_LOSS_FACTOR
            logging.info('Target profit: %s', target_profit)
            logging.info('Stop loss: %s', stop_loss)

            # If current price is greater than target profit, sell
            if float(df_.c) > target_profit:
                logging.info('Target profit reached - sell')
                logging.info('Profit: %s', float(df_.c) - self.buy_price)
                self.in_position = False

            # If current price is less than stop loss, sell
            elif float(df_.c) < stop_loss:
                logging.info('Stop loss reached - sell')
                logging.info('Loss: %s', float(df_.c) - self.buy_price)
                self.in_position = False


def main():
    """Main function to run the bot."""
    bot = TradingBot()  # Create instance of the bot
    ws = websocket.WebSocketApp(ENDPOINT, on_message=bot.on_message
