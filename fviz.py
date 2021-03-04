import sqlite3
import finviz
from finviz.screener import Screener

filters = ['exch_nasd', 'idx_sp500']  # Shows companies in NASDAQ which are in the S&P500
#stock_list = Screener(filters=filters, table='Valuation', order='price')  # Get the performance table and sort it by price ascending
stock_list = Screener(table='Valuation', order='price')
stock_list.to_sqlite("stock.sqlite3")

import sqlite3
conn = sqlite3.connect('stock.sqlite3')
c = conn.cursor()
c.execute("SELECT * FROM screener_results")
print(c.fetchall())
print(stock_list)
