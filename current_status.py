import argparse

import supertrend
import graph
import trend

parser = argparse.ArgumentParser()
parser.add_argument("symbol", help="The symbol you want the bot to focus on")
args = parser.parse_args()

symbol = args.symbol
t = supertrend.Bot(symbol)

data = t.analysis(symbol)

print(f"{trend.find_bias(symbol)} bias")
print(t.get_positions())

graph.plot(data, symbol)