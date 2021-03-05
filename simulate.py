import sqlite3
import pandas as pd
from point_and_figure import PNF

conn = sqlite3.connect('stock_prices.sqlite3')
conn.row_factory = sqlite3.Row
c = conn.cursor()
c.execute("select * from prices where ticker='AMZN' order by date asc")
rows = c.fetchall()
row_list = []
for row in rows:
    d = dict(zip(row.keys(), row))
    row_list.append(d)

chart = PNF(row_list, 30, 3)
for row in chart.pnf:
    print(row)
chart.plot()
