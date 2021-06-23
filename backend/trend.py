import warnings

import ta
import yfinance as yf

import print_supress


def find_bias(symbol, backtest=False, backtest_data=[]):
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    
    if backtest == True:
        data = backtest_data
    else:
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
        return 'BUY'
    
    elif (adx_pos < adx_neg) and (adx >= 17):
        return 'SELL'
    
    else:
        return 'NEUTRAL'