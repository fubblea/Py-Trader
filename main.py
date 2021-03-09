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
    print(f"Bot started with {bias} bias on {symbol}")
    
    if not (t.trading_window()):
        print("Waiting for trading window to open")
    
    #Main Loop
    #TODO Fix stop loss function
    #TODO Not covering position
    #TODO Fix supertrend period
    while True:
        if t.trading_window():
            strat = t.strat()
                
            current_call = strat[0]
            
            current_call = strat[0]
            
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
        
        else:
            t.close_all()