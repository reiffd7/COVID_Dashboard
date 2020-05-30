# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
from CalculatedFields import AddCalculatedFields

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

statesJSON = requests.get('https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/us-states.json').json()




# Read in COVID Data

url = 'https://covidtracking.com/api/v1/states/daily.csv'
df = pd.read_csv(url, parse_dates=['date']).sort_index()
df = df[['date', 'state', 'fips', 'positive', 'negative', 'death', 'hospitalizedCumulative', 'onVentilatorCumulative']]
df['date'] =  pd.to_datetime(df['date'])
df = df[~df['state'].isin(['MP', 'GU', 'AS', 'PR', 'VI'])]
df = AddCalculatedFields(df).df

COVID_metrics = ['positive', 'negative', 'death', 'new positive cases', 'new negative cases', 
                'new positive cases (last 7 days)','new negative cases (last 7 days)', 'tests last week',	
                'tests last week (per capita)',	'testing rate of change', 'testing rate of change (last 7 days average)',	
                'positive case pct', 'positive case pct (last 7 days average)',	'zero',	'positive case pct rate of change',	
                'positive case pct rate of change (last 7 days average)',	'positive cases rate of change',	
                'positive cases rate of change (last 7 days average)']


with open('web_scraping/coords.json', 'r') as f:
    coords = json.load(f)

latest = df[df.date == df.date.max()]


fig = px.choropleth_mapbox(latest,
            geojson = statesJSON,
            locations= 'state',
            color = 'positive cases rate of change (last 7 days average)',
            color_discrete_map = {-1: 'blue', 0: 'white', 1:'red'},
            range_color = [-1, 1],
            zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
            template="plotly_dark",
            mapbox_style = 'carto-positron'
            )
fig.update_layout(margin={"r":200,"t":0,"l":200,"b":0})


# def generate_table(dataframe, align, color, identifier, max_rows=1000):
#     return html.Table([
#         html.Thead(
#             html.Tr([html.Th(col) for col in dataframe.columns])
#         ),
#         html.Tbody([
#             html.Tr([
#                 html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
#             ]) for i in range(min(len(dataframe), max_rows))
#         ])
#     ], id = identifier, style={'text-align': align, 'color': color, 'margin-left': 'auto', 'margin-right': 'auto', 'margin-right':'auto'})


colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Hello Dash',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='Dash: A web application framework for Python.', style={
        'textAlign': 'center',
        'color': colors['text']
    }),
    html.Div([
        dcc.Dropdown(
        id = 'state_picker',
        options=[{'label': i, 'value': i} for i in latest.state],
        value=None
    )], style = {'width': '48%', 'display': 'inline-block'}),
    html.Div([
        dcc.Dropdown(
        id = 'metric_picker',
        options=[{'label': i, 'value': i} for i in COVID_metrics],
        value='new positive cases'
    )], style = {'width': '48%', 'float': 'right', 'display': 'inline-block'}),

    dcc.Graph(
        id='choropleth',
        figure=fig
    ),
    html.Div([
        dcc.Graph(id= 'crossfilter-metric-line')
    ], style = {'width': '49%', 'display': 'inline-block', 'padding': '10 10 10 10'}),
    html.Div([
        dcc.Graph(id= 'crossfilter-metric-line2')
    ], style = {'width': '49%', 'display': 'inline-block', 'padding': '10 10 10 10'}),
    # dcc.Slider(
    #     id='date-slider',
    #     min=df['date'].min(),
    #     max=df['date'].max(),
    #     value=df['date'].min(),
    #     marks={str(date):str(date) for date in df['date'].unique()},
    #     step=None
    # ),
    html.H4(children="COVID Data", style={
            'textAlign': 'center',
            'color': colors['text']}),
    html.Table(children = [
        html.Thead(
            html.Tr([html.Th(col) for col in df.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(df.iloc[i][col]) for col in df.columns
            ]) for i in range(min(len(df), 50))
        ])
    ], id = 'datatable', style={'text-align': 'center', 'color': colors['text'], 'margin-left': 'auto', 'margin-right': 'auto', 'margin-right':'auto'})
])


@app.callback(
    Output('choropleth', 'figure'),
    [Input('state_picker', 'value')])
def update_figure(state):
    if state == None:
        fig = px.choropleth_mapbox(latest,
            geojson = statesJSON,
            locations= 'state',
            color = 'positive cases rate of change (last 7 days average)',
            color_discrete_map = {'-1': 'blue', '0': 'white', '1':'red'},
            range_color = [-1, 1],
            zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
            template="plotly_dark",
            mapbox_style = 'carto-positron'
            )
        fig.update_layout(margin={"r":200,"t":0,"l":200,"b":0})
    else:
        fig = px.choropleth_mapbox(latest,
            geojson = statesJSON,
            locations= 'state',
            color = 'positive cases rate of change (last 7 days average)',
            color_continuous_scale="Viridis",
            zoom=5, center = {"lat": coords[state]['lat'], "lon": coords[state]['long']},
            template="plotly_dark",
            mapbox_style = 'carto-positron'
            )
        fig.update_layout(margin={"r":200,"t":0,"l":200,"b":0})
    return fig


@app.callback(
Output('crossfilter-metric-line', 'figure'),
[Input('state_picker', 'value'),
Input('metric_picker', 'value')])
def update_time_series(state, metric):
    dff = df[df['state'] == state]
    return {
        'data': [dict(
            x=dff['date'],
            y=dff[metric],
            mode='lines+markers'
        )],
        'layout': {
            'height': 225,
            'margin': {'l': 20, 'b': 30, 'r': 10, 't': 10},
            'annotations': [{
                'x': 0, 'y': 0.85, 'xanchor': 'left', 'yanchor': 'bottom',
                'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
                'text': metric
            }],
            'plot_bgcolor' : colors['background']
        }
    }


@app.callback(
    Output('datatable', 'children'),
    [Input('state_picker', 'value')]
)
def update_table(state):
    if state == None:
        df1 = df
        table = [
        html.Thead(
            html.Tr([html.Th(col) for col in df1.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(df1.iloc[i][col]) for col in df1.columns
            ]) for i in range(min(len(df1), 50))
        ])
    ]
    else:
        df1 = df[df['state'] == state]
        table = [
        html.Thead(
            html.Tr([html.Th(col) for col in df1.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(df1.iloc[i][col]) for col in df1.columns
            ]) for i in range(min(len(df1), 50))
        ])
    ]
    return table


    


if __name__ == '__main__':
    app.run_server(debug=True)