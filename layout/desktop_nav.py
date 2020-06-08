import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import sys
sys.path.append('../')
from utils import STATE_LABELS


states_dropdown = dbc.Col(
    dcc.Dropdown(
                    id="state_picker",
                    options=STATE_LABELS,
                    value="United States",
                    clearable=False,
                    searchable=False,
                    className="states-dropdown"
                )
)


navbar = [dbc.Row(
        
            # dbc.Col(
            #     html.Img(src="assets/images/covid19-new-logo.png", height="30px")
            # ),
            dbc.Col(
                html.A(
                    dbc.NavbarBrand(
                        [
                            html.P("COVID-19", className="navbar-brand-covid-19-text"),
                            html.P("Analysis", className="navbar-brand-us-cases-text"),
                        ]
                    ),
                    className="page-title-link",
                    href="/",
                )
            ),
        
        align="center",
        no_gutters=True,
    ),
    dbc.NavbarToggler(id="navbar-toggler", className="navbar-toggler-1"),
    dbc.Collapse(states_dropdown, id="navbar-collapse", navbar=True),
    html.Img(id="flag", style={'height':'60px', 'width':'120px', 'padding-right': '10px'})
    # about_bar
    # # dbc.NavbarBrand(about_bar),
]
