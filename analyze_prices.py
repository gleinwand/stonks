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
    df_pre_mean=df_pre.mean()['Close']

    # Get min price during covid
    max_date = df['Date'].max()
    df_post=df.loc[(df['Date'] > PRE_COVID_END)]
    df_post_min=df_post.min()['Close']
    df_post_vol=df_post.mean()['Volume']

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
        
        percent_covid_dip=(df_post_min-df_pre_mean)/df_pre_mean
        percent_recovery=(current_price-df_post_min)/current_price
        dip_plus_recovery=percent_covid_dip+percent_recovery
        data.append([ticker, df_post_vol, df_pre_mean, df_post_min, current_price, percent_covid_dip, percent_recovery, dip_plus_recovery])
    
    bar.next()
bar.finish()

final_df=pd.DataFrame(data, columns=['Ticker','MeanVolumePostCovid','PreCovidMean','CovidMin','Current','CovidDip','CovidRecovery','DipPlusRecovery'])
sorted_df=final_df.sort_values(by=['DipPlusRecovery'],ascending=True,)
print(tabulate(sorted_df, headers='keys', tablefmt='psql'))
sorted_df.to_csv(f"results/covid_dip.csv")
