import dash_core_components as dcc
import dash_html_components as html
import dash_table
from components import Header, print_button
from datetime import datetime as dt
from datetime import date, timedelta
import pandas as pd


# Read in COVID Data

url = 'https://covidtracking.com/api/v1/states/daily.csv'
df = pd.read_csv(url, parse_dates=['date']).sort_index()
df = df[['date', 'state', 'fips', 'positive', 'negative', 'death', 'hospitalizedCumulative', 'onVentilatorCumulative']]
df['date'] =  pd.to_datetime(df['date'])



layout_leaderboard = html.Div([
    html.Div([
        # CC Header
        Header(),
        # Date Picker
        html.Div([
            dcc.DatePickerRange(
                id='my-date-picker-range-leaderboard',
                min_date_allowed=dt(2020, 1, 22),
                max_date_allowed=dt(2021, 1, 22),
                initial_visible_month=dt(2020,df['date'].max().to_pydatetime().month, 1),
                start_date = (df['date'].max() - timedelta(6)).to_pydatetime(),
                end_date = df['date'].max().to_pydatetime(),

            ),
        html.Div(id='output-container-date-picker-range-leaderboard')
        ], className="row", style={'marginTop':30, 'marginBottom':15}),
        ## Header Bar
        html.Div([
            html.H6(["Leaderboard"], className="gs-header gs-text-header padded", style={'marginTop': 15})
        ]),
        html.Div([
            dash_table.DataTable(
                id='datatable-leaderboard',
                columns=[{"name": i, "id": i} for i in df.columns],
                editable=False,
                css=[{'selector': '.dash-cell div.dash-cell-value', 'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'}],
                style_table={'maxWidth': '1500px'}, 
                ),
            ], className=" eight columns")
            
        ])
    ])
