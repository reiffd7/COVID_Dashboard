from dash.dependencies import Input, Output
import dash_table
from dash_table.Format import Format
import plotly.express as px
import requests

import sys
sys.path.append('../')
from utils import StatesDataFrame, COORDS
from components import choropleth_mapbox, stats_table, existing_vs_new_chart

statesJSON = requests.get('https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/us-states.json').json()


font_size = ".9vw"
color_active = "#F4F4F4"
color_inactive = "#AEAEAE"
color_bg = "#010914"

def register_desktop_callbacks(app):
    @app.callback(
        Output('choropleth', 'figure'),
        [Input('state_picker', 'value'),
        Input('choropleth_criteria', 'value')])
    def map_content(state, criteria):
        return choropleth_mapbox(state, criteria)


    @app.callback(
        Output("stats-table", "children"),
        [Input("state_picker", "value")]
    )
    def stats_tab_content(state):
        df = stats_table(state)

        # font_size_heading = ".4vh"
        font_size_body = ".9vw"
        table = dash_table.DataTable(
            data=df.to_dict("records"),
            columns=[
                {"name": "Date", "id": "Date"},
                {"name": "State", "id": "State", "format": Format(group=",")},
                {
                    "name": 'Confirmed (Last 7)',
                    "id": 'Confirmed (Last 7)',
                    "type": "numeric",
                    "format": Format(group=",")
                }
                
            ],
            editable=False,
            sort_action="native",
            sort_mode="multi",
            column_selectable="single",
            style_as_list_view=True,
            # fixed_rows={"headers": True},
            fill_width=True,
            style_table={
                "width": "100%",
                "height": "100vh"},
            style_header={
                "backgroundColor": color_bg,
                "border": color_bg,
                "fontWeight": "bold",
                "font": "Lato, sans-serif",
                "height": "2vw",
                "width": "100%",
                "fill_width": True
            },
            style_cell={
                "font-size": font_size_body,
                "font-family": "Lato, sans-serif",
                "border-bottom": "0.01rem solid #313841",
                "backgroundColor": "#010915",
                "color": "#FEFEFE",
                "height": "2.75vw",
            },
            style_cell_conditional=[
                {
                    "if": {"column_id": "State/County",},
                    "minWidth": "4vw",
                    "width": "4vw",
                    "maxWidth": "4vw",
                },
                {
                    "if": {"column_id": "Confirmed",},
                    "color": "#F4B000",
                    "minWidth": "3vw",
                    "width": "3vw",
                    "maxWidth": "3vw",
                },
                {
                    "if": {"column_id": "Deaths",},
                    "color": "#E55465",
                    "minWidth": "3vw",
                    "width": "3vw",
                    "maxWidth": "3vw",
                },
            ]
        )
        return table


    @app.callback(
        [Output("existing-vs-new", "figure")],
        [Input("state_picker", "value")]
    )
    def existing_vs_new_chart_callback(state):
        fig = existing_vs_new_chart(state)
        return [fig]


    @app.callback(
    [Output("existing-vs-new-chart-title", "children")],
    [Input("state_picker", "value")],
    )                                                   # pylint: disable=W0612
    def confirmed_cases_chart_title_callback(state="United States"):
        if state == "United States":
            return ["U.S. Existing vs. New Cases"]

        return ["{} Existing vs. New Cases".format(state)]




       
