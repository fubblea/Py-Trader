import argparse
import os
import time

import alpaca_trade_api as alpaca
import dotenv

import grapher
import supertrend

#Matty the trading bot

def get_watchlist(api):
    resp = api.get_watchlists()
    symbols = []
    
    for item in resp['assets']:
        symbols.append(item['symbol'])
    
    return symbols

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
    
    watchlist = get_watchlist()
    
    t = supertrend.Bot(symbol, api, target=args.target)
    
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