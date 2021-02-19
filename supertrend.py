import numpy as np
import yfinance as yf
import pandas_datareader as pdr
import pandas as pd
import alpaca_trade_api as alpaca
import os
import dotenv
class Bot(object):    
    def __init__ (self, symbol):
        dotenv.load_dotenv()
        
        self.key = os.getenv("API_KEY")
        self.secret = os.getenv("SECRET_KEY")
        self.alpaca_endpoint = os.getenv("ENDPOINT")
        self.api = alpaca.REST(self.key, self.secret, self.alpaca_endpoint)
        self.symbol = symbol
        self.current_order = None
        
    def submit_order(self, side, target, stop_price):
            
        if side == "BUY":
            self.current_order = self.api.submit_order(symbol=self.symbol, 
                                                       qty=target, 
                                                       side='buy',
                                                       time_in_force='gtc',
                                                       type='market',
                                                       order_class='oto',
                                                       stop_loss=dict(stop_price=stop_price))
            
        elif side == "SELL":
            self.current_order = self.api.submit_order(symbol=self.symbol, 
                                                       qty=target, 
                                                       side='sell',
                                                       time_in_force='gtc',
                                                       type='market',
                                                       order_class='oto',
                                                       stop_loss=dict(stop_price=stop_price))
            
    def analysis(self, symbol):    
        data =yf.download(symbol, period="5h",interval="30m")
        data=data.reset_index(drop=True)

        data['tr0'] = abs(data["High"] - data["Low"])
        data['tr1'] = abs(data["High"] - data["Close"].shift(1))
        data['tr2'] = abs(data["Low"]- data["Close"].shift(1))
        data["TR"] = round(data[['tr0', 'tr1', 'tr2']].max(axis=1),2)
        data["ATR"]=0.00
        data['BUB']=0.00
        data["BLB"]=0.00
        data["FUB"]=0.00
        data["FLB"]=0.00
        data["ST"]=0.00

        # Calculating ATR 
        for i, row in data.iterrows():
            if i == 0:
                data.loc[i,'ATR'] = 0.00 #data['ATR'].iat[0]
            else:
                data.loc[i,'ATR'] = ((data.loc[i-1,'ATR'] * 9)+data.loc[i,'TR'])/10

        data['BUB'] = round(((data["High"] + data["Low"]) / 2) + (3 * data["ATR"]),2)
        data['BLB'] = round(((data["High"] + data["Low"]) / 2) - (3 * data["ATR"]),2)


        # FINAL UPPERBAND = IF( (Current BASICUPPERBAND < Previous FINAL UPPERBAND) or (Previous Close > Previous FINAL UPPERBAND))
        #                     THEN (Current BASIC UPPERBAND) ELSE Previous FINALUPPERBAND)


        for i, row in data.iterrows():
            if i==0:
                data.loc[i,"FUB"]=0.00
            else:
                if (data.loc[i,"BUB"]<data.loc[i-1,"FUB"])|(data.loc[i-1,"Close"]>data.loc[i-1,"FUB"]):
                    data.loc[i,"FUB"]=data.loc[i,"BUB"]
                else:
                    data.loc[i,"FUB"]=data.loc[i-1,"FUB"]

        # FINAL LOWERBAND = IF( (Current BASIC LOWERBAND > Previous FINAL LOWERBAND) or (Previous Close < Previous FINAL LOWERBAND)) 
        #                     THEN (Current BASIC LOWERBAND) ELSE Previous FINAL LOWERBAND)

        for i, row in data.iterrows():
            if i==0:
                data.loc[i,"FLB"]=0.00
            else:
                if (data.loc[i,"BLB"]>data.loc[i-1,"FLB"])|(data.loc[i-1,"Close"]<data.loc[i-1,"FLB"]):
                    data.loc[i,"FLB"]=data.loc[i,"BLB"]
                else:
                    data.loc[i,"FLB"]=data.loc[i-1,"FLB"]



        # SUPERTREND = IF((Previous SUPERTREND = Previous FINAL UPPERBAND) and (Current Close <= Current FINAL UPPERBAND)) THEN
        #                 Current FINAL UPPERBAND
        #             ELSE
        #                 IF((Previous SUPERTREND = Previous FINAL UPPERBAND) and (Current Close > Current FINAL UPPERBAND)) THEN
        #                     Current FINAL LOWERBAND
        #                 ELSE
        #                     IF((Previous SUPERTREND = Previous FINAL LOWERBAND) and (Current Close >= Current FINAL LOWERBAND)) THEN
        #                         Current FINAL LOWERBAND
        #                     ELSE
        #                         IF((Previous SUPERTREND = Previous FINAL LOWERBAND) and (Current Close < Current FINAL LOWERBAND)) THEN
        #                             Current FINAL UPPERBAND


        for i, row in data.iterrows():
            if i==0:
                data.loc[i,"ST"]=0.00
            elif (data.loc[i-1,"ST"]==data.loc[i-1,"FUB"]) & (data.loc[i,"Close"]<=data.loc[i,"FUB"]):
                data.loc[i,"ST"]=data.loc[i,"FUB"]
            elif (data.loc[i-1,"ST"]==data.loc[i-1,"FUB"])&(data.loc[i,"Close"]>data.loc[i,"FUB"]):
                data.loc[i,"ST"]=data.loc[i,"FLB"]
            elif (data.loc[i-1,"ST"]==data.loc[i-1,"FLB"])&(data.loc[i,"Close"]>=data.loc[i,"FLB"]):
                data.loc[i,"ST"]=data.loc[i,"FLB"]
            elif (data.loc[i-1,"ST"]==data.loc[i-1,"FLB"])&(data.loc[i,"Close"]<data.loc[i,"FLB"]):
                data.loc[i,"ST"]=data.loc[i,"FUB"]

        # Buy Sell Indicator
        for i, row in data.iterrows():
            if i==0:
                data["ST_BUY_SELL"]="NA"
            elif (data.loc[i,"ST"]<data.loc[i,"Close"]) :
                data.loc[i,"ST_BUY_SELL"]="BUY"
            else:
                data.loc[i,"ST_BUY_SELL"]="SELL"
        
        return data

    def strat(self, symbol):
        data = self.analysis(symbol)
        
        trigger = data.iloc[-1, -1]
        stop_price = data["ST"].iloc[-1]
        return [trigger, stop_price]