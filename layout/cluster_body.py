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


criterias = ['new positive (per capita)', 'tests last week (per capita)', 
                                            'testing rate of change (last 7 days average)', 'positive case pct rate of change (last 7 days average)',
                                            'positive cases rate of change (last 7 days average)']

########################################################################
#
#           Cluster scatter plot
#
########################################################################


cluster_scatter = dbc.Card(
    dbc.CardBody(
        [
            html.Div(
                [
                    html.Div(
                        dbc.Tabs(
                            children=[
                                dcc.Dropdown(
                                    id="criteria_1",
                                    options=[{'label': i, 'value': i} for i in criterias],
                                    value='new positive (per capita)',
                                    clearable=False,
                                    searchable=False,
                                    className="states-dropdown"
                                ),
                                dcc.Dropdown(
                                    id="criteria_2",
                                    options=[{'label': i, 'value': i} for i in criterias],
                                    value='tests last week (per capita)',
                                    clearable=False,
                                    searchable=False,
                                    className="states-dropdown"
                                ),
                            ],
                        ),   
                        
                    ),
                ],
                className="d-flex justify-content-between top-bar-us-map-heading-content",
            ),
            html.Div(
                dcc.Graph(
                    id="cluster_scatter",
                    style={"height": "60vh"},
                ),
                id="map-container",
            ),
        ]
    ),
)


cluster_body =  cluster_scatter