import sqlite3

import sqlite3
conn = sqlite3.connect('stock_prices.sqlite3')
c = conn.cursor()
#c.execute("SELECT ticker, date, open, close, high, low, adj_close, volume FROM prices")
c.execute("SELECT * FROM prices where ticker='IPOF'")
print(c.fetchall())
