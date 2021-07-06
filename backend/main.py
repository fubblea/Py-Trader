import argparse
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import alpaca_trade_api as alpaca
import dotenv

from backend import supertrend
from backend.watchlist import get_watchlist

#Matty the trading bot

if __name__ == '__main__':    
    parser = argparse.ArgumentParser()
    parser.add_argument("target", help="Target shares")
    parser.add_argument("--b", help="Bypass bias", action="store_true")
    args = parser.parse_args()
    
    dotenv.load_dotenv()
    api = alpaca.REST(os.getenv("API_KEY"), os.getenv("SECRET_KEY"), os.getenv("ENDPOINT"))
    
    watchlist = get_watchlist()
    print(f"Watching {watchlist}")
    active_bots = []
    
    if api.get_clock().is_open:
        for symbol in watchlist:
            active_bots.append(supertrend.Bot(symbol, bias_bypass=args.b))
    else:
        print("Market Closed")
        sys.exit()
    
    #Main Loop
    while True:
        for bot in active_bots:
            bot.evaluate()