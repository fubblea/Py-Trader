import supertrend
import datetime
import print_supress

if __name__ == '__main__':
    #TODO Implement last call through sessions
    #TODO Program reversals
    #TODO Send commands to running program
    
    symbol = "GME"
    last_call = "SELL"
    target = 500
    t = supertrend.Bot(symbol)
    
    print(f"[{datetime.datetime.now()}]")
    print(f"Bot started with focus on {symbol}")
    while True:
        
        with print_supress.suppress_stdout_stderr():
            current_call = t.strat(symbol)
        
        if current_call == last_call:
            pass
        
        elif current_call == "BUY":
            last_call = current_call
            t.submit_order("BUY", target)
            
            print(f"[{datetime.datetime.now()}]")
            print(f"New Call: Bought {target} shares of {symbol}")
        
        elif current_call == "SELL":
            last_call = current_call
            t.submit_order("SELL", target)
            
            print(f"[{datetime.datetime.now()}]")
            print(f"New Call: Sold {target} shares of {symbol}")