import backtrader as bt
import backtrader.indicators as btind
import math
import supertrend
import yfinance as yf

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
    
    def next(self):
        print(self.datetime.date(ago=0))
        
        if self.position.size == 0:                
            if self.bot.strat(self.i)[0] == 'HOLD':
                pass
                print("HOLD")
                
            elif self.bot.strat(self.i)[0] == "BUY":
                amount_to_invest = (self.order_pct * self.broker.cash)
                self.size = math.floor(amount_to_invest / self.data.close)

                print("Buy {} shares of {} at {}".format(self.size, symbol, self.data.close[0]))
                self.buy(size=self.size)
                print("BUY")
                
            else:
                amount_to_invest = (self.order_pct * self.broker.cash)
                self.size = math.floor(amount_to_invest / self.data.close)

                print("Sell {} shares of {} at {}".format(self.size, symbol, self.data.close[0]))
                self.sell(size=self.size)
                print("SELL")
        else:
            if self.last_call == 'BUY' and self.bot.strat(self.i)[0] == 'SELL':
                self.close()
                print("Close Positions")
                
            elif self.last_call == 'SELL' and self.bot.strat(self.i)[0] == 'BUY':
                self.close()
                print("Close Positions")
            else:
                print("HOLD")
        
        self.last_call = self.bot.strat(self.i)[0]
        self.i += 1

global symbol
symbol = 'AAPL'

cerebro = bt.Cerebro()
cerebro.addstrategy(Supertrend)
cerebro.broker.setcash(10000.0)

dataframe = yf.download(symbol, start='2021-01-01', end='2021-04-05', interval='1d')
dataframe.to_csv('backtesting_data.csv', encoding='utf-8')

data = bt.feeds.PandasData(dataname=dataframe)    
cerebro.adddata(data)
print("Data Imported")

print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.run()
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.plot(style='candlestick', barup='green', bardown='red')