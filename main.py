import argparse
import datetime
import os
import sys
import time

import alpaca_trade_api as alpaca
import dotenv

import grapher
import supertrend
import trend

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
    
    if args.b:
        last_call = t.strat()[0]
        bias = 'bypassed'
        print("Bias bypassed")
    else:
        bias = trend.find_bias(symbol)
    
        if bias == "buy":
            last_call = "SELL"
        elif bias == "sell":
            last_call = "BUY"
        else:
            print("Neutral Trend. Recommended not to trade")
            sys.exit()
    
    target = args.target
    data = t.analysis()
    grapher = grapher.Grapher(data, symbol)
    
    print(f"[{datetime.datetime.now()}]")
    print(f"Bot started with {bias} bias on {symbol}")
    
    if not (t.trading_window() or args.w):
        print("Waiting for trading window to open")
    
    grapher.plot()
    
    if args.w:
        print("Window bypassed")
    
    #Main Loop
    while True:
        if t.trading_window() or args.w:
            current_call = t.strat()[0]
            
            if len(t.get_positions()) == 0:                
                if last_call == current_call:
                    pass
                
                elif current_call == "BUY":
                    last_call = current_call
                    t.submit_order("BUY", target)
                    t.print_positions()
                
                else:
                    last_call = current_call
                    t.submit_order("SELL", target)
                    t.print_positions()
            else:
                if current_call != last_call:
                    t.close_all()
            
            grapher.update(t)
        
        else:
            t.close_all()
            time.sleep(0.5)
