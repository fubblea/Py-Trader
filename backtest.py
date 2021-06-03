import backtrader as bt
import backtrader.indicators as btind
import math
import supertrend
import trend
import yfinance as yf
import pandas as pd

import dotenv
import os
import alpaca_trade_api as alpaca


class DummyDifferenceDivider(bt.Indicator):
    lines = ('diffdiv',)  # output line (array)

    def __init__(self):
        diff = self.data(0) - self.data(-3)
        diffdiv = diff / 2
        
        print(diffdiv)
        self.lines.diffdiv = diffdiv
        
class SupertrendLine(bt.Indicator):
    lines = ('supertrend',)  # output line (array)
    def __init__(self):
        dotenv.load_dotenv()
        api = alpaca.REST(os.getenv("API_KEY"), os.getenv("SECRET_KEY"), os.getenv("ENDPOINT"))
        self.bot = supertrend.Bot(api=api, symbol=symbol, backtest=True)
        
        self.st_data = self.bot.analysis()['ST'].tolist() + self.data
        self.st_data = self.st_data - self.data
        
        self.lines.supertrend = self.st_data

class Supertrend(bt.Strategy):
    
    def __init__(self):
        #DummyDifferenceDivider(self.data)
        #SupertrendLine(self.data)
        
        dotenv.load_dotenv()
        api = alpaca.REST(os.getenv("API_KEY"), os.getenv("SECRET_KEY"), os.getenv("ENDPOINT"))
        self.bot = supertrend.Bot(api=api, symbol=symbol, backtest=True)
        self.i = 0
        self.last_call = 'HOLD'
        self.order_pct = 1
        self.backtest_data = pd.read_csv('backtesting_data.csv')
    
    def next(self):
        print(self.datetime.date(ago=0))
        
        trigger = self.bot.analysis().iloc[self.i]['ST_BUY_SELL']
        bias = trend.find_bias(symbol, backtest_data=self.backtest_data, backtest=True)
        
        if self.position.size == 0 and self.i > self.bot.lookback:                
            if trigger == "BUY" and bias == 'BUY':
                amount_to_invest = (self.order_pct * self.broker.cash)
                self.size = math.floor(amount_to_invest / self.data.close)

                print("BUY {} shares of {} at {}".format(self.size, symbol, self.data.close[0]))
                self.buy(size=self.size)
                
                self.last_call = trigger
                
            elif trigger == "SELL" and bias == 'SELL':
                amount_to_invest = (self.order_pct * self.broker.cash)
                self.size = math.floor(amount_to_invest / self.data.close)

                print("SELL {} shares of {} at {}".format(self.size, symbol, self.data.close[0]))
                self.sell(size=self.size)
                
                self.last_call = trigger
        else:
            if self.last_call == 'BUY' and trigger == 'SELL':
                self.close()
                print("Close Positions")
                
            elif self.last_call == 'SELL' and trigger == 'BUY':
                self.close()
                print("Close Positions")
                
        self.i += 1

global symbol
symbol = 'AAPL'

cerebro = bt.Cerebro()
cerebro.addstrategy(Supertrend)
cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='mysharpe')
cerebro.addanalyzer(bt.analyzers.PyFolio, _name='pyfolio')
cerebro.broker.setcash(10000.0)

dataframe = yf.download(symbol, start='2020-01-01', end='2020-03-30', interval='1d')
dataframe.to_csv('backtesting_data.csv', encoding='utf-8')

data = bt.feeds.PandasData(dataname=dataframe)    
cerebro.adddata(data)
print("Data Imported")

print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
strat = cerebro.run()
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
#cerebro.plot(style='candlestick', barup='green', bardown='red', volume=False)

# Print out the final result
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
print('Sharpe Ratio:', strat[0].analyzers.mysharpe.get_analysis())
strat[0].analyzers.mysharpe.pprint()
pyfoliozer = strat[0].analyzers.getbyname('pyfolio')
returns, positions, transactions, gross_lev = pyfoliozer.get_pf_items()
import pyfolio as pf
pf.create_full_tear_sheet(
    returns,
    positions=positions,
    transactions=transactions,
    #gross_lev=gross_lev,
    live_start_date='2008-01-01',  # This date is sample specific
    round_trips=True)

pf.create_simple_tear_sheet(returns)
pf.create_returns_tear_sheet(returns)