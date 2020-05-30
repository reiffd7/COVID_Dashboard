# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

statesJSON = requests.get('https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/us-states.json').json()




# Read in COVID Data

url = 'https://covidtracking.com/api/v1/states/daily.csv'
df = pd.read_csv(url, parse_dates=['date']).sort_index()
df = df[['date', 'state', 'fips', 'positive', 'negative', 'death', 'hospitalizedCumulative', 'onVentilatorCumulative']]
df['date'] =  pd.to_datetime(df['date'])

latest = df[df.date == df.date.max()]

fig = px.choropleth_mapbox(latest,
        geojson = statesJSON,
        locations= 'state',
        color = 'positive',
        color_continuous_scale="Viridis",
        zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
        template="plotly_dark",
        mapbox_style = 'carto-positron'
        )
fig.update_layout(margin={"r":200,"t":0,"l":200,"b":0})


def generate_table(dataframe, align, color, max_rows=1000):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ], style={'text-align': align, 'color': color, 'margin-left': 'auto', 'margin-right': 'auto', 'margin-right':'auto'})


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
        options=[{'label': i, 'value': i} for i in latest.state],
        value='AK'
    )], style = {'columnCount': 1, 'margin-left': 'auto', 'width': 200, 'display': 'flex'}),

    dcc.Graph(
        id='choropleth_with_slider'
    ),
    dcc.Slider(
        id='date-slider',
        min=df['date'].min(),
        max=df['date'].max(),
        value=df['date'].min(),
        marks={str(date):str(date) for date in df['date'].unique()},
        step=None
    )
    html.H4(children="COVID Data", style={
            'textAlign': 'center',
            'color': colors['text']}),
    generate_table(df, 'center', colors['text'])
])


@app.callback(
    Output('choropleth_with_slider', 'figure'),
    [Input('date-slider', 'value')])
def update_figure(selected_date):
    filtered_date = df[df.date = selected_date]
    trace = px.choropleth_mapbox(filtered_date,
        geojson = statesJSON,
        locations= 'state',
        color = 'positive',
        color_continuous_scale="Viridis",
        zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
        template="plotly_dark",
        mapbox_style = 'carto-positron'
        )
    return{
        'data' : trace,
        'layout' : dict(
            margin={"r":200,"t":0,"l":200,"b":0},
            transition= {'duration': 500}
        )

    }
    


if __name__ == '__main__':
    app.run_server(debug=True)