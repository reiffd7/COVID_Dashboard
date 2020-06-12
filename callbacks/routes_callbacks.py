import dash_html_components as html
from dash.dependencies import Input, Output, State

import sys
sys.path.append('../')
from layout import desktop_body, cluster_body, navbar
from utils import StatesDataFrame



def register_routes_callbacks(app):
    

    @app.callback(
        [Output("navbar-content", "children"),
        Output("page-content", "children")],
        [Input("url", "pathname")]
    )  
    def display_page(pathname):
        if pathname == '/':
            return navbar, desktop_body
        elif pathname == '/cluster':
            return navbar, cluster_body
        else:
            return navbar, desktop_body
        