import pandas as pd   
import numpy as np   
import dash_bootstrap_components as dbc    
import dash_html_components as html  

import sys
sys.path.append('../')
from utils import StatesDataFrame


def get_daily_stats(state="US"):
    df = StatesDataFrame().df
    df['date'] = pd.DatetimeIndex(df['date']).strftime("%Y-%m-%d")

    if state=='United States':
        data = df.groupby('date').mean()[['positive cases rate of change (last 7 days average)', 'positive case pct rate of change (last 7 days average)', 'testing rate of change (last 7 days average)']]
        data = data.sort_values(by='date')
        data = data.tail(1)
    else:
        data = df[df['state'] == state][['date','positive cases rate of change (last 7 days average)', 'positive case pct rate of change (last 7 days average)', 'testing rate of change (last 7 days average)']]
        data = data.sort_values(by='date')
        data = data.tail(1)
    positive_case_roc = data['positive cases rate of change (last 7 days average)'].to_numpy()[0]
    if positive_case_roc > 0.0:
        positive_case_color = "Red"
    elif positive_case_roc < 0.0:
        positive_case_color = "Green"
    positive_pct_roc = data['positive case pct rate of change (last 7 days average)'].to_numpy()[0]
    if positive_pct_roc > 0.0:
        positive_pct_color = "Red"
    elif positive_pct_roc < 0.0:
        positive_pct_color = "Green"
    testing_roc = data['testing rate of change (last 7 days average)'].to_numpy()[0]
    if testing_roc > 0.0:
        testing_color = "Green"
    elif testing_roc < 0.0:
        testing_color = "Red"
    stats = {
        'Existing vs. New Rate of Change': [round(positive_case_roc, 2), positive_case_color],
        'Positive % Rate of Change': [round(positive_pct_roc, 2), positive_pct_color],
        'Testing Rate of Change': [round(testing_roc, 4), testing_color]
    }
    return stats

def daily_stats(state="US"):
    stats = get_daily_stats(state)
    cards = []
    for key, value in stats.items():
        card = dbc.Col(
            dbc.Col(
                dbc.CardBody(
                    [
                        html.H1(
                            f"{value[0]}",
                            className=f"top-bar-value-{key.lower()}",
                            style = {"color": value[1]}
                        ),
                        html.P(
                            f"{key}",
                            className="card-text"
                        )
                    ]
                ),
                className=f"top-bar-card-{key.lower()}"
            ),
            width=3,
            className="top-bar-card-body"
        )
        cards.append(card)

    return cards
