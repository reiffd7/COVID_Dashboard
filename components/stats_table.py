import pandas as pd 
import numpy as np 

import sys 
sys.path.append('../')
from utils import StatesDataFrame


def stats_table(state="US"):
    df = StatesDataFrame().df
    df['date'] = pd.DatetimeIndex(df['date']).strftime("%Y-%m-%d")
    df = df[['date', 'state', 'new positive cases']]
    df.rename(columns={'date': 'Date', 'state': 'State', 'new positive cases': 'Confirmed (Last 7)'}, inplace=True)
    latest = df[df['Date'] == df['Date'].max()]
    if state in ["US", "United States"]:
        data = latest.sort_values(by=['Confirmed (Last 7)'], ascending=False)
    else:
        data = df[df['State'] == state]
        data = data.sort_values(by=['Date'])
    return data

        
    