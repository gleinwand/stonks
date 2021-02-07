import csv
import pandas as pd
import os
from datetime import date,datetime

PRE_COVID_START = '2019-06-01'
PRE_COVID_END = '2020-01-01'
COVID_START = '2020-01-01'
BASE_DIR='historical_stock_prices'

files = os.listdir(BASE_DIR)
for file in files[:5]:
    ticker = os.path.splitext(file)[0]
    df = pd.read_csv(BASE_DIR + '/' + file)

    df_pre=df.loc[(df['Date'] >= PRE_COVID_START) & (df['Date'] <= PRE_COVID_END)]

    print(f"TICKER: {ticker}")
    print(f"MIN: {df_pre.min()}")
    print(f"MAX: {df_pre.max()}")
    print(f"MEAN: {df_pre.mean()}")
