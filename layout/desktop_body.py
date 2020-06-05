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
#                       Confirm/Death Table
#
########################################################################
sim_tabs = dbc.Card(
    [
        dbc.CardBody(id="sim-table", className="stats-table-col",),
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
                                    label="Positive Cases ROC",
                                    value="positive cases rate of change (last 7 days average)",
                                    className="confirmed-us-map-tab",
                                    style=tab_style,
                                    selected_style=tab_selected_style,
                                ),
                                dcc.Tab(
                                    label="Positive % ROC",
                                    value="positive case pct rate of change (last 7 days average)",
                                    className="confirmed-us-map-tab",
                                    style=tab_style,
                                    selected_style=tab_selected_style,
                                ),
                                dcc.Tab(
                                    label="Testing Per Capita (last 7) ",
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
                html.Div(
                [dcc.Dropdown(
                    id="state_picker",
                    options=STATE_LABELS,
                    value="United States",
                    clearable=False,
                    searchable=False,
                    className="states-dropdown"
                ),
                html.Img(id="flag", style={'height':'30%', 'width':'30%', 'padding-left': '.5vw'})],
                ),
                className="states-dropdown-container",
                width=2),
            dbc.Col(
                dbc.Row(id="daily-stats", className="top-bar-content"),
                width=10,
                className="top-bar-content-col"
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
        ),
        # Sim table
        dbc.Col(
            sim_tabs, className="right-col-stats-content", width=2
        )
       ],
       no_gutters=True,
       className="middle-map-new-content mt-3"
    ),
    # Chart Section
    dbc.Row(
        [
            dbc.Col(
                html.Div(
                    dbc.Row(
                        [
                            # Chart 1
                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody(
                                        [
                                            html.Div(
                                                id = "existing-vs-new-chart-title",
                                                className="bottom-chart-h1-title"
                                            ),
                                            html.Div(
                                                "Since 1/22",
                                                className="bottom-chart-h2-title"
                                            ),
                                            html.Div(
                                                dcc.Loading(
                                                    dcc.Graph(
                                                        id="existing-vs-new",
                                                        config={"responsive": False},
                                                        style={"height": "20vh"},
                                                        className="top-bottom-left-chart-figure"
                                                    )
                                                ),
                                                id="chart-container"
                                            )
                                        ]
                                    )
                                ),
                                className="top-bottom-left-chart",
                                width=4,
                            ),
                            # Chart 2
                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody(
                                        [
                                            html.Div(
                                                id = "testing-per-capita-chart-title",
                                                className="bottom-chart-h1-title"
                                            ),
                                            html.Div(
                                                "# of tests (last 7 days) divided by population",
                                                className="bottom-chart-h2-title"
                                            ),
                                            html.Div(
                                                dcc.Loading(
                                                    dcc.Graph(
                                                        id="testing-per-capita",
                                                        config={"responsive": False},
                                                        style={"height": "20vh"},
                                                        className="top-bottom-mid-chart-figure"
                                                    )
                                                ),
                                                id="chart-container"
                                            )
                                        ]
                                    )
                                ),
                                className="top-bottom-mid-chart",
                                width=4,
                            ),
                            # Chart 3
                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody(
                                        [
                                            html.Div(
                                                id = "positive-pct-chart-title",
                                                className="bottom-chart-h1-title"
                                            ),
                                            html.Div(
                                                "# of tests (last 7 days) divided by population",
                                                className="bottom-chart-h2-title"
                                            ),
                                            html.Div(
                                                dcc.Loading(
                                                    dcc.Graph(
                                                        id="positive-pct",
                                                        config={"responsive": False},
                                                        style={"height": "20vh"},
                                                        className="top-right-mid-chart-figure"
                                                    )
                                                ),
                                                id="chart-container"
                                            )
                                        ]
                                    )
                                ),
                                className="top-bottom-right-chart",
                                width=4,
                            ),
                        ]
                    )
                ),
            className="bottom-chart-row",
            )
        ]
    )
]