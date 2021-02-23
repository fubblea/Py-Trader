import mplfinance as mpf
import pandas as pd

<<<<<<< HEAD
def plot(df, symbol):  
=======
def plot(df, symbol):
>>>>>>> mpf-graph
    df.loc[0,'ST'] = df.loc[1,'ST']
    apdict = mpf.make_addplot(df['ST'], secondary_y=False)
    df = df.set_index('Datetime')
        
<<<<<<< HEAD
    fig, ax = mpf.plot(df,volume=False,addplot=apdict, type='candle', 
                    style='yahoo', title=symbol, returnfig=True)
    
    return fig, ax
=======
    mpf.plot(df,volume=False,addplot=apdict, type='candle', 
            style='yahoo', title=symbol)
>>>>>>> mpf-graph
