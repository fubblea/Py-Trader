import argparse
import datetime
import os
import sys
import time

import alpaca_trade_api as alpaca
import dotenv

import grapher
import supertrend

#Matty the trading bot

if __name__ == '__main__':    
    parser = argparse.ArgumentParser()
    parser.add_argument("symbol", help="The symbol you want the bot to focus on")
    parser.add_argument("target", help="Target shares")
    parser.add_argument("--w", help="Bypass trading window", action="store_true")
    parser.add_argument("--b", help="Bypass bias", action="store_true")
    args = parser.parse_args()
    
    symbol = args.symbol
    
    dotenv.load_dotenv()
    api = alpaca.REST(os.getenv("API_KEY"), os.getenv("SECRET_KEY"), os.getenv("ENDPOINT"))
    
    t = supertrend.Bot(symbol, api, period='1d', interval='1m')
    
    target = args.target
    data = t.analysis()
    grapher = grapher.Grapher(data, symbol)
    
    if not (t.trading_window() or args.w):
        print("Waiting for trading window to open")
    
    grapher.plot()
    
    if args.w:
        print("Window bypassed")
    
    #Main Loop
    while True:
        if t.trading_window() or args.w:
            pass
            
            grapher.update(t)
        
        else:
            t.close_all()
            time.sleep(0.5)
