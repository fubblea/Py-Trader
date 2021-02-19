import alpaca_trade_api as alpaca
import sys
import so_trend
import datetime
import print_supress

class SuperTrend(object):
    def __init__ (self, symbol):
        self.key = 'PK1ZBENYCZ4YGCXIHT5P'
        self.secret = 'WPM7Fr3RxYzZrUh4i7rkgxGn9xSuPkUXgFYwliOa'
        self.alpaca_endpoint = 'https://paper-api.alpaca.markets'
        self.api = alpaca.REST(self.key, self.secret, self.alpaca_endpoint)
        self.symbol = symbol
        self.current_order = None
        
        """
        try:
            self.position = int(self.api.get_position(self.symbol).qty)
        except:
            self.position = 0
        """
            
    def submit_order(self, type, target):
            
        if type == "BUY":
            self.current_order = self.api.submit_order(self.symbol, target, 'buy','market','fok')
            
        elif type == "SELL":
            self.current_order = self.api.submit_order(self.symbol, target, 'sell','market','fok')

if __name__ == '__main__':
    #TODO Implement last call through sessions
    #TODO Program reversals
    
    symbol = "GME"
    last_call = "BUY"
    target = 50
    t = SuperTrend(symbol)
    
    print(f"[{datetime.datetime.now()}]")
    print(f"Bot started with focus on {symbol}")
    while True:
        
        with print_supress.suppress_stdout_stderr():
            current_call = so_trend.strat(symbol)
        
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