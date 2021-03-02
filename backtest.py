import argparse

import supertrend
import graph

parser = argparse.ArgumentParser()
parser.add_argument("symbol", help="The symbol you want the bot to focus on")
args = parser.parse_args()

symbol = args.symbol
t = supertrend.Bot(symbol)

data = t.analysis(symbol)

print(data['ST_BUY_SELL'])

graph.plot(data, symbol)