import csv
import pandas as pd
import os
from datetime import datetime

PRE_COVID_START = '2019-06-01'
PRE_COVED_END = '2020-01-01'
COVID_START = '2020-01-01'
END_DATE = datetime.today().strftime('%Y-%m-%d')

base_dir='historical_stock_prices'
for file in os.listdir(base_dir):
    ticker = os.path.splitext(file)[0]
    df = pd.read_csv(base_dir + '/' + file)
    print(df)
