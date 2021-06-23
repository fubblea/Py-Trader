import argparse

from backend import supertrend
from backend import graph
from backend import trend

parser = argparse.ArgumentParser()
parser.add_argument("symbol", help="The symbol you want the bot to focus on")
args = parser.parse_args()

symbol = args.symbol
t = supertrend.Bot(symbol)

if t.trading_window():
    data = t.analysis()

    print(f"{trend.find_bias(symbol)} bias")
    print(t.print_positions())

    graph.plot(data, symbol)

else:
    print("Waiting for trading window to open")
    print(t.print_positions())