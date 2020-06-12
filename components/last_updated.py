import pandas as pd
from datetime import date
import sys
sys.path.append('../')
from utils import StatesDataFrame

today = date.today()



try:
    data = pd.read_csv('https://covidtracking.com/api/v1/states/daily.csv', parse_dates=['date']).sort_index()
    last_updated = max(data['date'])

except:
    last_updated = 'Error'


del data
