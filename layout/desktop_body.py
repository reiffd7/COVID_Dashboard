import dash_bootstrap_components as dbc 
import dash_core_components as dcc       
import dash_html_components as html  
import dash_table
from dash_table.Format import Format

import sys
sys.path.append('../')
from utils import STATE_LABELS
from components import last_updated
from components import stats_table


################ TABS STYLING ####################

font_size = ".9vw"
color_active = "#F4F4F4"
color_inactive = "#AEAEAE"
color_bg = "#010914"

tabs_styles = {
    "flex-direction": "row",
}
tab_style = {
    "padding": "1.3vh",
    "color": color_inactive,
    "fontSize": font_size,
    "backgroundColor": color_bg,
}

tab_selected_style = {
    "fontSize": font_size,
    "color": color_active,
    "padding": "1.3vh",
    "backgroundColor": color_bg,
}


########################################################################
#
#                       Confirm/Death Table
#
########################################################################
stats_tabs = dbc.Card(
    [
        dbc.CardBody(id="stats-table", className="stats-table-col",),
        dbc.CardFooter(  # html.P(
            f"Last Updated {str(last_updated).upper()}",
            className="right-tabs-last-updated-text",
        ),
    ],
    className="stats-table-div",
)



########################################################################
#
#           Us Choropleth Map
#
########################################################################

us_maps_tabs = dbc.Card(
    dbc.CardBody(
        [
            html.Div(
                [
                    html.Div(
                        dcc.Tabs(
                            id="choropleth_criteria",
                            value="tests last week (per capita)",
                            children=[
                                dcc.Tab(
                                    label="Positive Cases Rate of Change",
                                    value="positive cases rate of change (last 7 days average)",
                                    className="confirmed-us-map-tab",
                                    style=tab_style,
                                    selected_style=tab_selected_style,
                                ),
                                dcc.Tab(
                                    label="Testing Per Capita (last ",
                                    value="tests last week (per capita)",
                                    className="testing-us-map-tab",
                                    style=tab_style,
                                    selected_style=tab_selected_style,
                                ),
                            ],
                            style=tabs_styles,
                            colors={
                                "border": None,
                                "primary": None,
                                "background": None,
                            },
                        )
                    ),
                ],
                className="d-flex justify-content-between top-bar-us-map-heading-content",
            ),
            html.Div(
                dcc.Graph(
                    id="choropleth",
                    style={"height": "60vh"},
                ),
                id="map-container",
            ),
        ]
    ),
)



########################################################################
#
#                           Desktop App Body
#
########################################################################

desktop_body = [
    dbc.Row(
        [
            dbc.Col(
                dcc.Dropdown(
                    id="state_picker",
                    options=STATE_LABELS,
                    value="United States",
                    clearable=False,
                    searchable=False,
                    className="states-dropdown",
                ),
                className="states-dropdown-container",
                width=2
            )
        ]
    ),
    dbc.Row(
       [ # Stats col
        dbc.Col(
            stats_tabs, className="right-col-stats-content", width=2
        ),
        # MAPS col
        dbc.Col(
            html.Div(us_maps_tabs),
            className="middle-col-map-content",
            width=8
        )
       ]
    )
]