from dash.dependencies import Input, Output
import dash_table
from dash_table.Format import Format
import plotly.express as px
import requests

import sys
sys.path.append('../')
from utils import StatesDataFrame, COORDS, cosine_sim, StateFlags
from components import compare_scatter


font_size = ".9vw"
color_active = "#F4F4F4"
color_inactive = "#AEAEAE"
color_bg = "#010914"


def register_cluster_callbacks(app):
    @app.callback(
        Output('cluster_scatter', 'figure'),
        [Input('criteria_1', 'value'),
        Input('criteria_2', 'value')])
    def get_cluster_scatter(criteria_1, criteria_2):
        if criteria_1 == None or criteria_2 == None:
            return None
        else:
            return compare_scatter(criteria_1, criteria_2)