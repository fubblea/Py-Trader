import mplfinance as mpf
import pandas as pd

class Grapher():
    def __init__(self, data, symbol) -> None:
        self.df = data
        self.symbol = symbol
        
    def plot(self):  
        self.df.loc[0,'ST'] = self.df.loc[1,'ST']
        apdict = mpf.make_addplot(self.df['ST'], secondary_y=False)
        self.df = self.df.set_index('Datetime')
        
        mpf.plot(self.df,volume=False,addplot=apdict, type='candle', 
                        style='yahoo', title=self.symbol)
        
    def update(self, bot):
        data = bot.analysis()
        if data.iloc[-1, 0] != self.df.iloc[-1, 0]:
            print("Updating graph")
            self.df = data
            self.plot()