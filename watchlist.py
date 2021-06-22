import sys

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