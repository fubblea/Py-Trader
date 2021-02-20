import yfinance as yf
import pandas as pd
import numpy as np

def ema(Data, alpha, window):
    
    # alpha is the smoothing factor
    # window is the lookback period
    
    alpha = alpha / (window + 1.0)
    beta  = 1 - alpha
    
    # First value is a simple SMA
    Data.loc[window - 1, 'SMA'] = np.mean(Data.loc[:window - 1, 'ATR'])
    
    # Calculating first EMA
    Data.loc[window, 'EMA'] = ((Data.loc[window, 'ATR'] * alpha) + 
                               (Data.loc[window - 1, 'SMA'] * beta))
    # Calculating the rest of EMA
    for i in range(window + 1, len(Data)):
            try:
                Data.loc[i, 'EMA'] = ((Data.loc[i, 'ATR'] * alpha) + 
                                      (Data.loc[i - 1, 'EMA'] * beta))
        
            except KeyError:
                pass
    return Data

def eATR(Data, atr_lookback):
 
 # TR
 for i in range(len(Data)):
  try:
 
   Data.loc[i, 'ATR'] = max(Data.loc[i, 'High'] - Data.loc[i, 'Low'],
   abs(Data.loc[i, 'High'] - Data.loc[i - 1, 'Close']),
   abs(Data.loc[i, 'Low'] - Data.loc[i - 1, 'Close']))
 
  except KeyError:
   pass
 Data.loc[0, 'ATR'] = 0 
 Data = ema(Data, 2, atr_lookback)
 return Data