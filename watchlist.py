import yahoo_fin.stock_info as yf
import pandas as pd

def get_watchlist():
    day_gainers = pd.DataFrame(yf.get_day_gainers())
    
    target_pc_change = 20
    target_volume = 1000000
    
    watchlist = []
    
    for index, row in day_gainers.iterrows():
        if row['% Change'] >= target_pc_change and row['Volume'] >= target_volume:
            watchlist.append(row['Symbol'])
    
    return watchlist