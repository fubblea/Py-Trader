from ibapi.order import *

def submit_order(symbol, action, quantity, secType='STK', exchange='SMART', currency='USD'):
    from ibapi.client import EClient
    from ibapi.wrapper import EWrapper
    from ibapi.contract import Contract

    import threading
    import time
    class IBapi(EWrapper, EClient):
        def __init__(self):
            EClient.__init__(self, self)

        def nextValidId(self, orderId: int):
            super().nextValidId(orderId)
            self.nextorderId = orderId
            print('The next valid order id is: ', self.nextorderId)

        def orderStatus(self, orderId, status, filled, remaining, avgFullPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice):
            print('orderStatus - orderid:', orderId, 'status:', status, 'filled', filled, 'remaining', remaining, 'lastFillPrice', lastFillPrice)
        
        def openOrder(self, orderId, contract, order, orderState):
            print('openOrder id:', orderId, contract.symbol, contract.secType, '@', contract.exchange, ':', order.action, order.orderType, order.totalQuantity, orderState.status)

        def execDetails(self, reqId, contract, execution):
            print('Order Executed: ', reqId, contract.symbol, contract.secType, contract.currency, execution.execId, execution.orderId, execution.shares, execution.lastLiquidity)


    def run_loop():
        app.run()

    app = IBapi()
    app.connect('127.0.0.1', 7497, 123)

    app.nextorderId = None

    #Start the socket in a thread
    api_thread = threading.Thread(target=run_loop, daemon=True)
    api_thread.start()

    #Check if the API is connected via orderid
    while True:
        if isinstance(app.nextorderId, int):
            print('connected')
            break
        else:
            print('waiting for connection')
            time.sleep(1)

    #Create order object
    order = Order()
    order.action = action
    order.totalQuantity = quantity
    order.orderType = 'MKT'
    
    contract = Contract()
    contract.symbol = symbol
    contract.secType = secType
    contract.exchange = exchange
    contract.currency = currency

    #Place order
    app.placeOrder(app.nextorderId, contract, order)
    app.nextorderId += 1 

    app.disconnect()

def read_positions(): #read all accounts positions and return DataFrame with information

    from ibapi.client import EClient
    from ibapi.wrapper import EWrapper
    from ibapi.common import TickerId
    from threading import Thread

    import pandas as pd
    import time

    class ib_class(EWrapper, EClient):

        def __init__(self):
            EClient.__init__(self, self)

            self.all_positions = pd.DataFrame([], columns = ['Account','Symbol', 'Quantity', 'Average Cost', 'Sec Type'])

        def error(self, reqId:TickerId, errorCode:int, errorString:str):
            if reqId > -1:
                print("Error. Id: " , reqId, " Code: " , errorCode , " Msg: " , errorString)

        def position(self, account, contract, pos, avgCost):
            index = str(account)+str(contract.symbol)
            self.all_positions.loc[index]= account, contract.symbol, pos, avgCost, contract.secType

    def run_loop():
        app.run()
    
    app = ib_class()
    app.connect('127.0.0.1', 7497, 123)
    #Start the socket in a thread
    api_thread = Thread(target=run_loop, daemon=True)
    api_thread.start()
    time.sleep(1) #Sleep interval to allow time for connection to server

    app.reqPositions() # associated callback: position
    time.sleep(3)
    current_positions = app.all_positions
    current_positions.set_index('Account',inplace=True,drop=True) #set all_positions DataFrame index to "Account"
    
    app.disconnect()

    return(current_positions)


def read_navs(): #read all accounts NAVs

    from ibapi.client import EClient
    from ibapi.wrapper import EWrapper
    from ibapi.common import TickerId
    from threading import Thread

    import pandas as pd
    import time

    class ib_class(EWrapper, EClient):

        def __init__(self):
            EClient.__init__(self, self)

            self.all_accounts = pd.DataFrame([], columns = ['reqId','Account', 'Tag', 'Value' , 'Currency'])

        def error(self, reqId:TickerId, errorCode:int, errorString:str):
            if reqId > -1:
                print("Error. Id: " , reqId, " Code: " , errorCode , " Msg: " , errorString)

        def accountSummary(self, reqId, account, tag, value, currency):
            index = str(account)
            self.all_accounts.loc[index]=reqId, account, tag, value, currency

    def run_loop():
        app.run()
    
    app = ib_class()
    app.connect('127.0.0.1', 7497, 123)
    #Start the socket in a thread
    api_thread = Thread(target=run_loop, daemon=True)
    api_thread.start()
    time.sleep(1) #Sleep interval to allow time for connection to server

    app.reqAccountSummary(0,"All","NetLiquidation")  # associated callback: accountSummary / Can use "All" up to 50 accounts; after that might need to use specific group name(s) created on TWS workstation
    time.sleep(3)
    current_nav = app.all_accounts
    
    app.disconnect()

    return(current_nav)

def get_bars():
    from ibapi.client import EClient
    from ibapi.client import EClient
    from ibapi.wrapper import EWrapper
    from ibapi.contract import Contract

    import threading
    import time

    class IBapi(EWrapper, EClient):
        def __init__(self):
            EClient.__init__(self, self)
            self.data = [] #Initialize variable to store candle

        def historicalData(self, reqId, bar):
            print(f'Time: {bar.date} Close: {bar.close}')
            self.data.append([bar.date, bar.close])
            
    def run_loop():
        app.run()

    app = IBapi()
    app.connect('127.0.0.1', 7497, 123)

    #Start the socket in a thread
    api_thread = threading.Thread(target=run_loop, daemon=True)
    api_thread.start()

    time.sleep(1) #Sleep interval to allow time for connection to server

    #Create contract object
    eurusd_contract = Contract()
    eurusd_contract.symbol = 'TSLA'
    eurusd_contract.secType = 'STK'
    eurusd_contract.exchange = 'SMART'
    eurusd_contract.currency = 'USD'

    #Request historical candles
    app.reqHistoricalData(1, eurusd_contract, '', '1 W', '1 hour', 'TRADES', 0, 2, False, [])

    time.sleep(5) #sleep to allow enough time for data to be returned

    #Working with Pandas DataFrames
    import pandas

    df = pandas.DataFrame(app.data, columns=['DateTime', 'Close'])
    df['DateTime'] = pandas.to_datetime(df['DateTime'],unit='s') 

    print(df)


    app.disconnect()