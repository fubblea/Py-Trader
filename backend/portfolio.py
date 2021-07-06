from backend import ib_api
from numpy import floor

class Portfolio():
    def __init__(self, data) -> None:
        self.data = data
        
    def target_shares(self):
        risk = 0.01
        cash = float(ib_api.read_navs().loc['DU4129866']['Value'])
        cost_per_share = self.data['Close'].iloc[-1]
        
        target_shares = (cash * risk) / cost_per_share
        
        if target_shares < 1:
            target_shares = 0
        else:
            target_shares = floor(target_shares)
        
        return target_shares