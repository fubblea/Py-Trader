import argparse

import supertrend

parser = argparse.ArgumentParser()
parser.add_argument("symbol", help="The symbol you want the bot to focus on")
parser.add_argument("bias", help="Buying or selling bias")
args = parser.parse_args()

symbol = args.symbol
    
if args.bias == "buy":
    last_call = "SELL"
else:
    last_call = "BUY"

t = supertrend.Bot(symbol)

data = t.analysis(symbol)

print(data['ST_BUY_SELL'])