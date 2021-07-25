import psycopg2 as p

import time


def buying():
    boughtCompany = 'Amazon'  # Bot has just bought from this company
    tradeCode = 'AMZN'
    currentPrice = 0
    amountInvested = 0
    numBought = 0

    con = p.connect(
        "dbname='tradingbot' user='postgres' host='localhost' password='password'")
    cur = con.cursor()
    cur.execute("SELECT * FROM company")
    companies = cur.fetchall()
    # print(companies)
    # Checking if the boughtCompany already exists in db
    isPresent = False
    id = 1
    for company in companies:
        id = id + 1
        if (boughtCompany == company):
            isPresent = True

    # Adding company if not present
    if (isPresent == False):
        cur.execute("INSERT INTO public.company (id, name, companyprofit, istrading) VALUES(%s, %s, %s, %s)",
                    (id, boughtCompany, 0, True))
        con.commit()

    # Checking if the company is currently trading
    isTrading = False
    cur.execute("SELECT * FROM graph")
    graphs = cur.fetchall()
    graphId = 1
    tradingGraphId = 0
    for graph in graphs:
        graphId = graphId + 1
        if (boughtCompany == graph[1] and graph[5] == True):
            tradingGraphId = graph[0]
            print(graph[0], graph[1], graph[5])
            # Checks if there are any active trades for boughtCompany.
            isTrading = True

    numPositions = 1
    # Couting the number of existing positions to provide an appropriate id for later
    cur.execute("SELECT * FROM positions")
    positions = cur.fetchall()
    for position in positions:
        numPositions = numPositions + 1

    # Creating a graph in the graph db if open trades don't already exist.
    if (isTrading == False):

        currentTime = time.time()  # Gives the epoch time.
        cur.execute("INSERT INTO graph (id, companyname, lowtick, stockprice, hightick, istrading, tradeid, capital, profit, timeaxis) VALUES(%s, %s, %s,%s, %s, %s,%s, %s, %s, %s)",
                    (graphId, boughtCompany, [0], [0], [0], True, tradeCode, 0, 0, [currentTime]))
        con.commit()

        # Creating a new position to match with the new graph
        currentTime = time.time()  # Gives the epoch time.
        cur.execute("INSERT INTO positions (id, starttime, companyname, openprice, profit, istrading, capital, numbought, graphid) VALUES(%s, %s, %s, %s, %s, %s,%s, %s, %s)",
                    (numPositions, currentTime, boughtCompany, currentPrice, 0, True, amountInvested, numBought, graphId))
        con.commit()
    # If there is already an existing graph, the new position needs to be linked with it. So different queries are written,
    else:
        currentTime = time.time()  # Gives the epoch time.
        cur.execute("INSERT INTO positions (id, starttime, companyname, openprice, profit, istrading, capital, numbought, graphid) VALUES(%s, %s, %s, %s, %s, %s,%s, %s, %s)",
                    (numPositions, currentTime, boughtCompany, currentPrice, 0, True, amountInvested, numBought, tradingGraphId))
        con.commit()
    cur.close()
    con.close()
# End of function
