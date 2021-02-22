import mplfinance as mpf
import datetime
import pandas as pd

def plot(df, symbol):
    df.loc[:10,'ST'] = df.loc[10,'ST']
    apdict = mpf.make_addplot(df['ST'], secondary_y=False)
    df = df.set_index('Datetime')
    
    mpf.plot(df,volume=True,addplot=apdict, type='candle', style='yahoo', title=symbol)
