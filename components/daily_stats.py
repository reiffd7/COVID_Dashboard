import pandas as pd   
import numpy as np   
import dash_bootstrap_components as dbc    
import dash_html_components as html  

import sys
sys.path.append('../')
from utils import StatesDataFrame

GREEN = '#0CCE6B'
RED = '#B76D68'




def get_daily_stats(state="US"):
    df = StatesDataFrame().df
    df['date'] = pd.DatetimeIndex(df['date']).strftime("%Y-%m-%d")

    if state=='United States':
        data = df.groupby('date').agg({'positive':'sum', 'new positive cases':'sum', 'positive cases rate of change (last 7 days average)':'mean', 'positive case pct rate of change (last 7 days average)':'mean', 'testing rate of change (last 7 days average)':'mean', 'positive case pct (last 7 days average)': 'mean', 'tests last week': 'sum' })
        # data = df.groupby('date').mean()[['positive cases rate of change (last 7 days average)', 'positive case pct rate of change (last 7 days average)', 'testing rate of change (last 7 days average)']]
        data = data.sort_values(by='date')
        data = data.tail(1)
    else:
        data = df[df['state'] == state][['date','positive', 'new positive cases', 'positive cases rate of change (last 7 days average)', 'positive case pct (last 7 days average)', 'positive case pct rate of change (last 7 days average)', 'tests last week', 'testing rate of change (last 7 days average)']]
        data = data.sort_values(by='date')
        data = data.tail(1)
    positives = int(data['positive'].to_numpy()[0])
    new_positives = int(data['new positive cases'].to_numpy()[0])
    positive_case_roc = data['positive cases rate of change (last 7 days average)'].to_numpy()[0]
    if positive_case_roc > 0.0:
        positive_case_color = RED
    elif positive_case_roc < 0.0:
        positive_case_color = GREEN
    positive_pct = data['positive case pct (last 7 days average)'].to_numpy()[0]
    positive_pct_roc = data['positive case pct rate of change (last 7 days average)'].to_numpy()[0]
    if positive_pct_roc > 0.0:
        positive_pct_color = RED
    elif positive_pct_roc < 0.0:
        positive_pct_color = GREEN
    tests = data['tests last week'].to_numpy()[0]
    testing_roc = data['testing rate of change (last 7 days average)'].to_numpy()[0]
    if testing_roc > 0.0:
        testing_color = GREEN
    elif testing_roc < 0.0:
        testing_color = RED
    stats = {
        'Positive Cases': [positives, new_positives],
        'Existing vs. New Rate of Change': [round(positive_case_roc, 2), positive_case_color],
        'Positive Percentage': [round(positive_pct*100, 2), round(positive_pct_roc, 2), positive_pct_color],
        'Tests Last Week': [int(tests), round(testing_roc, 4), testing_color]
    }
    return stats

def daily_stats(state="US"):
    stats = get_daily_stats(state)
    cards = []
    for key, value in stats.items():
        if key == 'Positive Cases':
            card = dbc.Col(
                dbc.Col(
                    dbc.CardBody(
                        [
                            html.P(
                                f"+ {value[1]:,d} new in last week",
                                className=f"top-bar-perc-change-confirmed",
                            ),
                            html.H1(
                                f"{value[0]:,d}",
                                className=f"top-bar-value-confirmed"
                            ),
                            html.P(
                                f"{key}",
                                className="card-text"
                            )
                        ]
                    ),
                    className=f"top-bar-card-confirmed"
                ),
                width=3,
                className="top-bar-card-body-skinny"
            )
            cards.append(card)
        elif key == 'Positive Percentage':
            card = dbc.Col(
                dbc.Col(
                    dbc.CardBody(
                        [
                            html.P(
                                "{0:.0f}% of last week".format(value[1]),
                                className=f"top-bar-perc-change-confirmed",
                                style = {"color": value[2]}
                            ),
                            html.H1(
                                f"{value[0]}%",
                                className=f"top-bar-value-tested"
                            ),
                            html.P(
                                f"{key}",
                                className="card-text"
                            )
                        ]
                    ),
                    className=f"top-bar-card-tested"
                ),
                width=3,
                className="top-bar-card-body-skinny"
            )
            cards.append(card)
        elif key == 'Tests Last Week':
            card = dbc.Col(
                dbc.Col(
                    dbc.CardBody(
                        [
                            html.P(
                                "{}% of last week".format(value[1]*100),
                                className=f"top-bar-perc-change-confirmed",
                                style = {"color": value[2]}
                            ),
                            html.H1(
                                f"{value[0]:,d}",
                                className=f"top-bar-value-tested"
                            ),
                            html.P(
                                f"{key}",
                                className="card-text"
                            )
                        ]
                    ),
                    className=f"top-bar-card-tested"
                ),
                width=3,
                className="top-bar-card-body-skinny"
            )
            cards.append(card)
        else:
            card = dbc.Col(
                dbc.Col(
                    dbc.CardBody(
                        [
                            html.P(
                                "~",
                                className=f"top-bar-perc-change-confirmed",
                            ),
                            html.H1(
                                f"{value[0]}",
                                className=f"top-bar-value-tested",
                                style = {"color": value[1]}
                            ),
                            html.P(
                                f"{key}",
                                className="card-text"
                            )
                        ]
                    ),
                    className=f"top-bar-card-tested"
                ),
                width=3,
                className="top-bar-card-body-skinny"
            )
            cards.append(card)

    return cards
