from dash.dependencies import Input, Output
import plotly.express as px
import requests
import pandas as pd 

import sys
sys.path.append('../')
from utils import StatesDataFrame, COORDS

statesJSON = requests.get('https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/us-states.json').json()




def choropleth_mapbox(state, criteria):
    latest = pd.read_csv('utils/todays_data.csv')
    latest = latest[latest.date == latest.date.max()]
    latest.rename(columns={criteria:'~'}, inplace=True)
    if criteria == 'positive cases rate of change (last 7 days average)':
        colorRange = [-1, 1]
        color_scale = "RdBu_r"
    elif criteria == 'positive case pct rate of change (last 7 days average)':
        colorRange = [-20, 20]
        color_scale = "RdBu_r"
    else:
        colorRange = None
        color_scale = "GnBu"
    if state == 'United States':
        fig = px.choropleth_mapbox(latest,
            geojson = statesJSON,
            locations= 'state',
            color = '~',
            color_continuous_scale=color_scale,
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
            color_continuous_scale=color_scale,
            range_color = colorRange,
            zoom=5, center = {"lat": COORDS[state]['lat'], "lon": COORDS[state]['long']},
            template="plotly_dark",
            mapbox_style = 'carto-darkmatter'
            )
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, mapbox= dict(accesstoken = 'pk.eyJ1IjoicmVpZmZkIiwiYSI6ImNrOHFjaXlmOTAyaW0zamp6ZzI4NmtmMTQifQ.4EOhJ5NJJpawQnnoBXGCkw'))
    return fig