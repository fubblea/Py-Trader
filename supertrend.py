import datetime
import os
import time

import alpaca_trade_api as alpaca
import dotenv
import numpy as np
import pandas as pd
import pandas_datareader as pdr
import yfinance as yf

import e_atr


class Bot(object):    
    def __init__ (self, symbol):
        dotenv.load_dotenv()
        
        self.key = os.getenv("API_KEY")
        self.secret = os.getenv("SECRET_KEY")
        self.alpaca_endpoint = os.getenv("ENDPOINT")
        self.api = alpaca.REST(self.key, self.secret, self.alpaca_endpoint)
        self.symbol = symbol
        self.current_order = None
     
    def get_positions(self):
        print("Open Positions:")
        time.sleep(1)
        print(self.api.list_positions())
    
    def submit_order(self, side, target):
        if side == "BUY":
            self.current_order = self.api.submit_order(symbol=self.symbol, 
                                                       qty=target, 
                                                       side='buy',
                                                       time_in_force='fok',
                                                       type='market')
            
            print(f"[{datetime.datetime.now()}]")
            print(f"Bought {target} shares in {self.symbol}")
            
        elif side == "SELL":
            self.current_order = self.api.submit_order(symbol=self.symbol, 
                                                       qty=target, 
                                                       side='sell',
                                                       time_in_force='fok',
                                                       type='market')
            print(f"[{datetime.datetime.now()}]")
            print(f"Sold {target} shares in {self.symbol}")
            
    def analysis(self, symbol):    
        data =yf.download('MSFT', period="1d",interval="15m")
        data=data.reset_index(drop=True)
        
        multiplier = 3
        period = 10

        data["ATR"]=0.00
        data['SMA']=0.00
        data['EMA']=0.00
        data['BUB']=0.00
        data["BLB"]=0.00
        data["FUB"]=0.00
        data["FLB"]=0.00
        data["ST"]=0.00

        e_atr.eATR(data, period)
        
        data['BUB'] = round(((data["High"] + data["Low"]) / 2) + (multiplier * data["EMA"]),2)
        data['BLB'] = round(((data["High"] + data["Low"]) / 2) - (multiplier * data["EMA"]),2)


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
        return [trigger]
