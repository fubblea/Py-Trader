import argparse
import os
import sys

import alpaca_trade_api as alpaca
import dotenv

import supertrend

#Matty the trading bot

#Change 1

def get_watchlist(api):
    watchlist = api.get_watchlists()[0]
    print(watchlist)
    symbols = []
    
    try:
        for item in watchlist.assets:
            symbols.append(item['symbol'])
    
        return symbols
    except AttributeError:
        print("Watchlist Empty")
        sys.exit()

if __name__ == '__main__':    
    parser = argparse.ArgumentParser()
    parser.add_argument("target", help="Target shares")
    parser.add_argument("--b", help="Bypass bias", action="store_true")
    args = parser.parse_args()
    
    dotenv.load_dotenv()
    api = alpaca.REST(os.getenv("API_KEY"), os.getenv("SECRET_KEY"), os.getenv("ENDPOINT"))
    
    #TODO Fix watchlist not working
    watchlist = get_watchlist(api)
    
    #Watchlist Override
    watchlist = ['TSLA', 'NVDA']
    active_bots = []
    
    if api.get_clock().is_open():
        for symbol in watchlist:
            active_bots.append(supertrend.Bot(symbol, api, target=args.target, bias_bypass=args.b))
    else:
        print("Market Closed")
        sys.exit()
    
    #Main Loop
    while True:
        for bot in active_bots:
            bot.evaluate()