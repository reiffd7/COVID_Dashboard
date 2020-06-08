# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc    
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
from callbacks import register_desktop_callbacks
from callbacks import register_routes_callbacks
from callbacks import register_cluster_callbacks
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
from utils import STATE_LABELS
from layout import build_desktop_layout


external_stylesheets = [
    # Bootswatch theme
    dbc.themes.SLATE,
    # for social media icons
    "https://use.fontawesome.com/releases/v5.9.0/css/all.css",
]

meta_tags = [
    {
        "name": "description",
        "content": ("Live coronavirus news, statistics, and visualizations"
                    " tracking the number of cases and death toll due to "
                    "COVID-19, with up-to-date testing center information "
                    "by US states and counties. Also provides current "
                    "SARS-COV-2 vaccine progress and treatment research "
                    "across different countries. Sign up for SMS updates."),
    },
    {"name": "viewport",
        "content": "width=device-width, initial-scale=1.0"},
]



app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.config.suppress_callback_exceptions = True

statesJSON = requests.get('https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/us-states.json').json()



colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}


app.layout = build_desktop_layout


################################################################################
#
#    Register callbacks
#
################################################################################

register_routes_callbacks(app)   
register_desktop_callbacks(app)
register_cluster_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True)