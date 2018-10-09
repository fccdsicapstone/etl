import psycopg2

host = "35.237.252.26"
db="broadband"
usr="postgres"
pw="dsi2018dsi2018"

#building connections to postgreSQL
conn = psycopg2.connect(host= host,database=db, user=usr, password=pw)
cur = conn.cursor()

#specify your query
sql = 'select top 10 * from raw.fcc' #example

#execute your query
cur.execute(sql)
rows = cur.fetchall()
print("The number of rows: ", cur.rowcount)


import pandas as pd
#convert to pandas dataframe
df = pd.DataFrame(rows)
