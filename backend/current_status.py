import argparse
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from backend import supertrend
from backend import graph
from backend import trend

"""parser = argparse.ArgumentParser()
parser.add_argument("symbol", help="The symbol you want the bot to focus on")
args = parser.parse_args()

symbol = args.symbol"""

#!OVERRIDE
symbol = "EUR"
t = supertrend.Bot(symbol, secType='CASH')

data = t.analysis()

print(t.print_positions())

graph.plot(data, symbol)