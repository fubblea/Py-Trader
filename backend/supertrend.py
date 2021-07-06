import datetime
import time

import pandas as pd
import yfinance as yf

from backend import indicators
from backend import print_supress
from backend import trend
from backend import portfolio
from backend import ib_api


class Bot(object):    
    def __init__ (self, symbol, secType='STK', currency='USD', period='2d', interval='15m', lookback=6, multiplier=3, bias_bypass=False, backtest=False):
        """Bot running on the supertrend algorithm

        Args:
            symbol (str): Ticker symbol
            period (str, optional): Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max. Defaults to '2d'.
            interval (str, optional): Valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo. Defaults to '15m'.
            lookback (int, optional): Lookback. Defaults to 10.
            multiplier (int, optional): Multiplier. Defaults to 3.
        """
        self.symbol = symbol
        self.period = period
        self.lookback = lookback
        self.multiplier = multiplier
        self.interval = interval
        self.current_order = None
        self.target = 0
        self.bias_bypass = bias_bypass
        self.backtest = backtest
        self.secType = secType
        
        if secType == 'STK':
            self.exchange = 'SMART'
        elif secType == 'CASH':
            self.exchange = 'IDEALPRO'
        
        self.currency = currency
    
    def close_all(self):
        current_positions = self.get_positions()

        for index, row in current_positions.iterrows():
            if row['Sec Type'] == "STK":
                exchange = 'SMART'
            elif row['Sec Type'] == 'CASH':
                exchange = "IDEALPRO"
                
            if row['Quantity'] < 0:
                ib_api.submit_order(row['Symbol'], 'SELL', row['Quantity'], secType=row['Sec Type'], exchange=exchange)
            elif row['Quantity'] > 0:
                ib_api.submit_order(row['Symbol'], 'BUY', row['Quantity'], secType=row['Sec Type'], exchange=exchange)
            
    def get_positions(self):
        pos = ib_api.read_positions().loc[['DU4129866']]
        pos.reset_index(drop=True, inplace=True)
        
        for index, row in pos.iterrows():
            if row['Quantity'] == 0:
                pos = pos.drop(index)
        
        return pos
        
    def print_positions(self):
        print("Open Positions:")
        print(self.get_positions())
    
    def submit_order(self, side, target):
        self.current_order = ib_api.submit_order(self.symbol, side, target, self.secType, self.exchange, self.currency)
            
    def analysis(self):
        
        if self.backtest == True:
            data = pd.read_csv('backtesting_data.csv')
            data=data.reset_index()
        else:
            with print_supress.suppress_stdout_stderr():
                if self.secType == 'CASH':
                    symbol = self.symbol + self.currency + '=X'
                else:
                    symbol = self.symbol
                
                data =yf.download(symbol, period=self.period,interval=self.interval)
                data=data.reset_index()
        
        multiplier = self.multiplier
        period = self.lookback

        data["ATR"]=0.00
        data['SMA']=0.00
        data['EMA']=0.00
        data['BUB']=0.00
        data["BLB"]=0.00
        data["FUB"]=0.00
        data["FLB"]=0.00
        data["ST"]=0.00

        indicators.eATR(data, period)
        
        data['BUB'] = ((data["High"] + data["Low"]) / 2) + (multiplier * data["EMA"])
        data['BLB'] = ((data["High"] + data["Low"]) / 2) - (multiplier * data["EMA"])


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

    def strat(self):
        if self.secType == 'CASH':
            symbol = self.symbol + self.currency + '=X'
        else:
            symbol = self.symbol
        bias = trend.find_bias(symbol)
        
        data = self.analysis()
        
        trigger = data.iloc[-1, -1]
        
        if self.bias_bypass == True:
            return ['BUY', data]
        
        if len(self.get_positions()) == 0:
            if bias == trigger:
                return [trigger, data]
            else:
                return ['HOLD', data]
        else:
            return [trigger, data]

    def evaluate(self):
        strat = self.strat()
        position = self.get_positions()
        self.target = portfolio.Portfolio(strat[1]).target_shares()
            
        if len(position) == 0:                
            if strat[0] == 'HOLD':
                pass
                
            elif strat[0] == "BUY":
                self.submit_order("BUY", self.target)
                self.print_positions()
                
            else:
                self.submit_order("SELL", self.target)
                self.print_positions()
        else:
            for index, row in position.iterrows():
                if row['Quantity'] > 0 and strat[0] == 'sell':
                    self.close_all()
                    
                if row['Quantity'] < 0 and strat[0] == 'buy':
                    self.close_all()
