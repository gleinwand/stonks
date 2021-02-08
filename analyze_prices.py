import csv
import pandas as pd
import os
import math
from datetime import date,datetime
from tabulate import tabulate
from progress.bar import Bar

PRE_COVID_START = '2019-09-01'
PRE_COVID_END = '2020-01-01'
COVID_START = '2020-01-01'
BASE_DIR='historical_stock_prices'

files = os.listdir(BASE_DIR)
data=[]
bar = Bar('reading', max=len(files))
for file in files:
    ticker = os.path.splitext(file)[0]
    df = pd.read_csv(BASE_DIR + '/' + file)

    # Get mean price before COVID
    df_pre=df.loc[(df['Date'] >= PRE_COVID_START) & (df['Date'] <= PRE_COVID_END)]
    df_pre_median=df_pre.median()['Close']
    df_pre_mean=df_pre.mean()['Close']

    # Get min price during covid
    max_date = df['Date'].max()
    df_post=df.loc[(df['Date'] > PRE_COVID_END)]
    df_post_min=df_post.min()['Close']
    df_post_vol=df_post.median()['Volume']

    # Get current price
    df_current=df.loc[(df['Date'] == max_date)].max()
    current_price=df_current['Close']
    # Create dataframe

    if (not math.isnan(df_pre_mean)
        and not math.isnan(df_post_min)
        and not math.isnan(current_price)
        and not math.isnan(df_post_vol)
        and current_price > 0.01
        and current_price != df_post_min
        and df_post_vol > 10000):
        
        percent_covid_dip=100*(df_post_min-df_pre_mean)/df_pre_mean
        recovery_percent=100*(current_price-df_post_min)/df_pre_mean
        data.append([ticker, round(df_pre_median,2), round(df_pre_mean,2), round(df_post_min,2), round(current_price,2), -1*round(percent_covid_dip,2), round(recovery_percent,2)])
    bar.next()
bar.finish()

final_df=pd.DataFrame(data, columns=['Ticker','PreCovidMedianPrice','PreCovidMeanPrice','CovidMinPrice','CurrentPrice','PriceDipPercent','PriceRecoveryPercent'])
sorted_df=final_df.sort_values(by=['PriceRecoveryPercent'],ascending=True,)
print(tabulate(sorted_df, headers='keys', tablefmt='psql'))
sorted_df.to_csv(f"results/covid_dip.csv")
