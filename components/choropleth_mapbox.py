from dash.dependencies import Input, Output
import plotly.express as px
import requests

import sys
sys.path.append('../')
from utils import StatesDataFrame, COORDS

statesJSON = requests.get('https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/us-states.json').json()
color_scale = [
        "#fadc8f",
        "#f9d67a",
        "#f8d066",
        "#f8c952",
        "#f7c33d",
        "#f6bd29",
        "#f5b614",
        "#F4B000",
        "#eaa900",
        "#e0a200",
        "#dc9e00",
    ]



def choropleth_mapbox(state, criteria):
    latest = StatesDataFrame().df
    latest = latest[latest.date == latest.date.max()]
    latest.rename(columns={criteria:'~'}, inplace=True)
    if criteria == 'positive cases rate of change (last 7 days average)':
        colorRange = [-1, 1]
    else:
        colorRange = None
    if state == 'United States':
        fig = px.choropleth_mapbox(latest,
            geojson = statesJSON,
            locations= 'state',
            color = '~',
            color_continuous_scale="RdBu_r",
            range_color = colorRange,
            zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
            template="plotly_dark",
            mapbox_style = 'carto-darkmatter'
            )
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, mapbox = dict(accesstoken='pk.eyJ1IjoicmVpZmZkIiwiYSI6ImNrOHFjaXlmOTAyaW0zamp6ZzI4NmtmMTQifQ.4EOhJ5NJJpawQnnoBXGCkw'))
    else:
        fig = px.choropleth_mapbox(latest,
            geojson = statesJSON,
            locations= 'state',
            color = '~',
            color_continuous_scale="RdBu_r",
            range_color = colorRange,
            zoom=5, center = {"lat": COORDS[state]['lat'], "lon": COORDS[state]['long']},
            template="plotly_dark",
            mapbox_style = 'carto-darkmatter'
            )
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, mapbox= dict(accesstoken = 'pk.eyJ1IjoicmVpZmZkIiwiYSI6ImNrOHFjaXlmOTAyaW0zamp6ZzI4NmtmMTQifQ.4EOhJ5NJJpawQnnoBXGCkw'))
    return fig