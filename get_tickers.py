import config
import finnhub as fh
import yfinance as yf
import sqlite3
import os
import pandas as pd
from datetime import datetime
from progress.bar import Bar

DB_FILE = "stock_prices.sqlite3"
BASE_DIR = "historical_stock_prices"
START_DATE = "2011-03-01"
END_DATE = "2021-03-01"
#END_DATE = datetime.today().strftime('%Y-%m-%d')
EXCLUDE_MICS = ['OOTC','OTCM','ARCX','BATS']
INCLUDE_MICS = ['XNGS','XNYS','XNCM','XNMS','XASE']

print(f"Getting data between {START_DATE} and {END_DATE}")

# Setup client
fclient = fh.Client(api_key=config.api_key)

# Get all US symbols
symbols=fclient.stock_symbols('US')
mics={}
types={}
for symb in symbols:
    mics[symb['mic']] = mics.get(symb['mic'], 0) + 1
    types[symb['type']] = types.get(symb['type'], 0) + 1

symbols_list=[]
for s in symbols:
    if s['type'] == 'Common Stock' and s['mic'] not in EXCLUDE_MICS:
        symbols_list.append(s['symbol'])

os.remove(DB_FILE)
conn = sqlite3.connect(DB_FILE)

dfs = []

# Download historical data from yfinance
bar = Bar('downloading', max=len(symbols_list))
for s in symbols_list:
    try:
        df = yf.download(s, START_DATE, END_DATE, progress=False)
        if not df.empty:
            df.rename(columns={"Adj Close": "Adj_Close"}, inplace = True)
            df.insert(0, "Ticker", s)
            rounded_df = df.round(2)
            dfs.append(rounded_df)
    except Exception as e:
        print(f"Download failed for {s}:\n")
        print(e)
    bar.next()
bar.finish()

final_df = pd.concat(dfs)
final_df.to_sql('prices', con=conn, if_exists='replace', index = True)
