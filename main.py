import argparse
import datetime

import print_supress
import mplfinance as mpf
import supertrend
import graph
import pandas as pd

if __name__ == '__main__':    
    parser = argparse.ArgumentParser()
    parser.add_argument("symbol", help="The symbol you want the bot to focus on")
    parser.add_argument("bias", help="Buying or selling bias")
    parser.add_argument("target", help="Target shares")
    args = parser.parse_args()
    
    symbol = args.symbol
    
    if args.bias == "buy":
        last_call = "SELL"
    else:
        last_call = "BUY"
    
    target = args.target
    t = supertrend.Bot(symbol)
    
    print(f"[{datetime.datetime.now()}]")
    print(f"Bot started with {args.bias}ing bias on {symbol}")
    
    #Main Loop
    #TODO Fix stop loss function
    #TODO Not covering position
    while t.trading_window():
           
        with print_supress.suppress_stdout_stderr():
            strat = t.strat(symbol)
            
        current_call = strat[0]
        
        current_call = strat[0]
        
        if current_call == last_call:
            pass
        
        elif current_call == "BUY":
            last_call = current_call
            t.submit_order("BUY", target)
            t.get_positions()
        
        elif current_call == "SELL":
            last_call = current_call
            t.submit_order("SELL", target)
            t.get_positions()
            
    t.close_all()
