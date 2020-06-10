import pandas as pd
from datetime import date
import sys
sys.path.append('../')
from utils import StatesDataFrame

today = date.today()



try:
    data = pd.read_csv('utils/todays_data.csv')
    last_updated = max(data['date'])

except:
    last_updated = 'Error'


del data
