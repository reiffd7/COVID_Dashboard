import pandas as pd
import numpy as np
import json


with open('web_scraping/states.json', 'r') as f:
    stateAbbrevs = json.load(f)
stateAbbrevs = {v: k for k,v in stateAbbrevs.items()}
with open('web_scraping/statePop.json', 'r') as f:
    statePops = json.load(f)


class AddCalculatedFields(object):

    def __init__(self, df):
        self.df = df
        print('prepping df')
        self.prepDF()
        self.dates = self.df['date'].unique()
        self.states = self.df['state'].unique()

    def prepDF(self):
        self.df.sort_values(by=['state', 'date'], inplace=True)
        self.df = self.df.reset_index()
        self.df['new positive cases'] = self.df.groupby(['state', 'fips'])['positive'].diff(1).fillna(0)
        self.df['new negative cases'] = self.df.groupby(['state', 'fips'])['negative'].diff(1).fillna(0)
        self.df['new positive cases (last 7 days)'] = self.df.groupby(['state', 'fips'])['new positive cases'].apply(lambda x: x.rolling(7, min_periods=0).sum())
        self.df['new negative cases (last 7 days)'] = self.df.groupby(['state', 'fips'])['new negative cases'].apply(lambda x: x.rolling(7, min_periods=0).sum())
        self.df['tests last week'] = self.df['new positive cases (last 7 days)'] + self.df['new negative cases (last 7 days)']
        self.df['tests last week (per capita)'] = self.df.apply(lambda x: x['tests last week']/statePops[stateAbbrevs[x['state']]], axis=1)
        self.df['testing rate of change'] = self.df.groupby(['state', 'fips'])['tests last week (per capita)'].diff(1).fillna(0)
        self.df['testing rate of change (last 7 days average)'] = self.df.groupby(['state', 'fips'])['testing rate of change'].apply(lambda x: x.rolling(7, min_periods=0).mean()).fillna(0)
        self.df['positive case pct'] = self.df['new positive cases (last 7 days)']/self.df['tests last week']
        self.df['positive case pct (last 7 days average)'] = self.df.groupby(['state', 'fips'])['positive case pct'].apply(lambda x: x.rolling(7, min_periods=0).mean()).fillna(0)
        self.df['zero'] = 0.0
        self.df['positive case pct rate of change'] = (self.df['positive case pct'] - self.df.groupby(['state', 'fips'])['positive case pct'].diff(1).fillna(0))/(self.df.groupby(['state', 'fips'])['positive case pct'].diff(1).fillna(0))
        self.df['positive case pct rate of change (last 7 days average)'] = self.df.groupby(['state', 'fips'])['positive case pct rate of change'].apply(lambda x: x.rolling(7, min_periods=0).mean()).fillna(0)
        self.df['positive cases rate of change'] = (self.df['new positive cases (last 7 days)'] - self.df.groupby(['state', 'fips'])['new positive cases (last 7 days)'].shift(1))/(self.df['positive'] - self.df.groupby(['state', 'fips'])['positive'].shift(1)).fillna(0)
        self.df['positive cases rate of change (last 7 days average)'] = self.df.groupby(['state', 'fips'])['positive cases rate of change'].apply(lambda x: x.rolling(7, min_periods=0).mean()).fillna(0)
        # self.df['sensitive_slopeBH'] = self.df.groupby(['state', 'fips'])['slope'].apply(lambda x: x.rolling(10, win_type='blackmanharris', min_periods=0).mean())
        # self.df['sensitive_slopeTriang'] = self.df.groupby(['state', 'fips'])['slope'].apply(lambda x: x.rolling(10, win_type='triang', min_periods=0).mean())
        # self.df['sensitive_slopeBox'] = self.df.groupby(['state', 'fips'])['slope'].apply(lambda x: x.rolling(10, win_type='boxcar', min_periods=0).mean())
        self.df['date'] = pd.to_datetime(self.df['date'].apply(lambda x: str(x).split('T')[0]))
        # self.df = self.df[self.df['date'] >= '2020-04-01']
        # self.dfLeaderboard = self.df[['date', 'state', 'slope_lastWeekAvg', 'positiveRateChange_smooth', 'testsRate_smooth']]
        self.df.sort_values(by='date', inplace=True)
        # if state_filter:
        #     self.df = self.df[self.df['state'].isin(states)]
        #     self.dfLeaderboard = self.dfLeaderboard[self.dfLeaderboard['state'].isin(states)]
