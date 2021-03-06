import warnings

import ta
import yfinance as yf

import print_supress


def find_bias(symbol):
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    
    with print_supress.suppress_stdout_stderr():
        data =yf.download(symbol, period="5d",interval="60m")
        data=data.reset_index()
    
    bias = ta.trend.ADXIndicator(data['High'], data['Low'], data["Close"])\

    adx = bias.adx()
    adx = adx.iloc[-1]
    
    adx_pos = bias.adx_pos()
    adx_pos = adx_pos.iloc[-1]
    
    adx_neg = bias.adx_neg()
    adx_neg = adx_neg.iloc[-1]
    
    
    if (adx_pos > adx_neg) and (adx >= 17):
        return 'buy'
    
    elif (adx_pos < adx_neg) and (adx >= 17):
        return 'sell'
    
    else:
        return 'neutral'