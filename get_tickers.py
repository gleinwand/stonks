import config
import finnhub as fh
import yfinance as yf
import csv
from datetime import datetime
from progress.bar import Bar

BASE_DIR = "historical_stock_prices"
START_DATE = "2019-06-01"
END_DATE = datetime.today().strftime('%Y-%m-%d')

print(f"Getting data between {START_DATE} and {END_DATE}")

# Setup client
fclient = fh.Client(api_key=config.api_key)

# Get all US symbols
symbols=fclient.stock_symbols('US')
symbols_list=[s['symbol'] for s in symbols]

# TODO: Jk, looks like trying to get it all at once leads to death
#data=yf.download(symbols_list, START_DATE, END_DATE,threads=2)
#data.to_csv(BASE_DIR + "/all_stock_data.csv")
#bar = Bar('downloading', max=len(symbols_list))
#for s in symbols_list:
#    sdata=data.loc[:, (slice(None), s)]
#    sdata.columns = sdata.columns.droplevel(1)
#    
#    # Only include stocks that have at least one non-null value
#    if sdata.notnull().values.any():
#        sdata.to_csv(BASE_DIR + f"/{s}.csv",index=False)
#    bar.next()
#bar.finish()

# Download historical data from yfinance
bar = Bar('downloading', max=len(symbols))
for s in symbols_list:
    data = yf.download(s, START_DATE, END_DATE, progress=False)
    if not data.empty:
        data.to_csv(BASE_DIR + f"/{s}.csv")
    bar.next()
bar.finish()
