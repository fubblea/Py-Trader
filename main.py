import argparse
import datetime
import sys

import supertrend
import trend

#Matty the trading bot

if __name__ == '__main__':    
    parser = argparse.ArgumentParser()
    parser.add_argument("symbol", help="The symbol you want the bot to focus on")
    parser.add_argument("target", help="Target shares")
    args = parser.parse_args()
    
    symbol = args.symbol
    bias = trend.find_bias(symbol)
    
    if bias == "buy":
        last_call = "SELL"
    elif bias == "sell":
        last_call = "BUY"
    else:
        print("Neutral Trend. Recommended not to trade")
        sys.exit()
    
    target = args.target
    t = supertrend.Bot(symbol)
    
    print(f"[{datetime.datetime.now()}]")
    print(f"Bot started with {bias}ing bias on {symbol}")
    
    #Main Loop
    #TODO Fix stop loss function
    #TODO Not covering position
    #TODO Fix supertrend period
    while t.trading_window():
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
