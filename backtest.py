import backtrader as bt
import datetime
import supertrend
import yfinance as yf

import dotenv
import os
import alpaca_trade_api as alpaca


class Supertrend(bt.Strategy):    
    def __init__(self):
        dotenv.load_dotenv()
        api = alpaca.REST(os.getenv("API_KEY"), os.getenv("SECRET_KEY"), os.getenv("ENDPOINT"))
        self.bot = supertrend.Bot(api=api, symbol='AAPL', backtest=True)
    
    def next(self):
        print(self.datetime.date(ago=0))
        print(self.bot.strat()[0])
        
        if self.bot.strat()[0] == 'BUY':
            self.buy()
        elif self.bot.strat()[0] == 'SELL':
            self.sell()

symbol = 'AAPL'

cerebro = bt.Cerebro()
cerebro.addstrategy(Supertrend)
cerebro.broker.setcash(10000.0)

dataframe = yf.download(symbol, start='2021-01-01', end='2021-01-30', interval='1d')
dataframe.to_csv('backtesting_data.csv', encoding='utf-8')

data = bt.feeds.PandasData(dataname=dataframe)    
cerebro.adddata(data)
print("Data Imported")

print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.run()
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.plot(style='candlestick', barup='green', bardown='red')