import ta
import yfinance as yf

def find_bias(symbol):
    data =yf.download(symbol, period="5d",interval="15m")
    data=data.reset_index()
    
    bias = ta.trend.ADXIndicator(data['High'], data['Low'], data["Close"])
    
    average = bias.adx()
    plus = bias.adx_pos()
    minus = bias.adx_neg()
    aroon = bias.aroon_indicator()
    
    return [average, plus, minus, aroon]

print(find_bias('TSLA'))