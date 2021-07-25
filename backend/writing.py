import psycopg2 as p
from data import companyList

# currentCompany = 'Google'
# trading = True
# code = 'GOOG'
# data = 2
# profit = 0

con = p.connect(
    "dbname='tradebot' user='postgres' host='localhost' password='password'")
cur = con.cursor()
cur.execute("SELECT * FROM company")
companies = cur.fetchall()
id = 0
profit = 0
for currentCompany in companyList:
    exists = False
    id = id + 1
    for c in companies:
        id = id + 1
        if (currentCompany == c[1]):
            exists = True
            print('already exists')

    if (exists == False):
        cur.execute("INSERT INTO company (id, companyname, profit) VALUES(%s, %s, %s)",
                    (id, currentCompany, profit))
        con.commit()
    else:
        print('true')

# cur.execute("SELECT * FROM company")
# companies = cur.fetchall()

# for company in companies:
#     print(company)
#     print(company[0])

cur.close()
con.close()
