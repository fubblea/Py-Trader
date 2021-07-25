import psycopg2 as p

import time


def selling(boughtCompany, tradeCode, numSold, sellPrice):

    con = p.connect(
        "dbname='tradingbot' user='postgres' host='localhost' password='password'")
    cur = con.cursor()

    # Finding the graph for the company
    cur.execute(
        "SELECT * FROM graph WHERE istrading=True AND tradeid= %s", (tradeCode,))
    graph = cur.fetchall()[0]

    id = graph[0]

    cur.execute(
        "SELECT * FROM positions WHERE istrading=True AND graphid= %s AND openprice=%s", (id, sellPrice))
    # Takes the first instace where the condition is satisfied
    # If there are multiple instances wherein the price is the same, it is trading and it's connected to
    # the graph, then the first (oldest) instance is sold. Just easier to code lol

    position = cur.fetchall()[0]

    numLeft = position[7] - numSold
    # print(position, numLeft)
    updateId = position[0]
    if (numLeft == 0):
        cur.execute(
            "UPDATE positions SET istrading=False WHERE istrading=True AND graphid= %s AND openprice = %s AND id=%s", (id, sellPrice, updateId))
        con.commit()
    else:
        cur.execute(
            "UPDATE positions SET numbought=%s WHERE istrading=True AND graphid= %s AND openprice = %s AND id=%s", (numLeft, id, sellPrice, updateId))
        con.commit()

    # If all positions are closed, then graph's isTrading = false. Checking for this
    cur.execute(
        "SELECT * FROM positions WHERE istrading=True AND graphid= %s", (id,))
    positions = cur.fetchall()
    numOpen = 0
    for positionA in positions:
        print('here')
        numOpen = numOpen + 1
        if (numOpen > 0):
            break
    if (numOpen == 0):
        # print('here')
        # Case wherein there are no open positions, graph can be closed.
        cur.execute(
            "SELECT * FROM graph WHERE istrading=True AND tradeid= %s", (tradeCode,))
        graph = cur.fetchall()[0]
        tempId = graph[0]
        compName = graph[1]
        cur.execute(
            "UPDATE graph SET istrading=False WHERE istrading=True AND id= %s", (tempId,))
        con.commit()
        # If there are no graphs active, then the account can be closed.
        cur.execute(
            "UPDATE company SET istrading=False WHERE istrading=True AND name=%s", (compName,))
        con.commit()
    # Printing the list of remaining companies to check

    cur.execute("SELECT * FROM company WHERE istrading=True")
    active = cur.fetchall()
    print(active)

    cur.close()
    con.close()

# End of function


selling('Amazon', 'AMZN', 0, 0)
