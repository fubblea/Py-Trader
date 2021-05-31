import backtrader as bt
import datetime

cerebro = bt.Cerebro()
cerebro.broker.setcash(10000.0)
    
data = bt.feeds.YahooFinanceData(dataname='AAPL',
                                  fromdate=datetime.date(2017, 1, 1),
                                  todate=datetime.date(2017, 12, 31))
    
print(data)
    
cerebro.adddata(data)
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.run()
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.plot()