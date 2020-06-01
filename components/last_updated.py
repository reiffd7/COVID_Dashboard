import pandas as pd
from datetime import date
import sys
sys.path.append('../')
from utils import StatesDataFrame

today = date.today()



try:
    data = StatesDataFrame().df
    last_updated = today

except:
    last_updated = 'Error'


del data
