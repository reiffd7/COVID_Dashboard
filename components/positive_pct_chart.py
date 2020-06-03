import pandas as pd   
import numpy as np   
import plotly.graph_objects as go
import math

import sys
sys.path.append('../')
from utils import StatesDataFrame


def human_format(num):
    """Formats a number and returns a human-readable version of it in string
    form. Ex: 300,000 -> 300k
    :params num: number to be converted to a formatted string
    """
    num = float("{:.3g}".format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return "{}{}".format(
        "{:f}".format(
            num
            ).rstrip("0").rstrip("."), ["", "K", "M", "B", "T"][magnitude]
    )


def human_percentage(num):
    return str(round(num*100, 2)) + '%'


def positive_pct_chart(state="US"):

    df = StatesDataFrame().df
    df['date'] = pd.DatetimeIndex(df['date']).strftime("%Y-%m-%d")
    df = df[df['date'] >= '2020-04-01']
    if state == 'United States':
        data = df.groupby('date').sum()[['tests last week', 'new positive cases (last 7 days)']]
        data['positive case pct'] = data['new positive cases (last 7 days)']/data['tests last week']
        data['positive case pct (last 7 days average)'] = data['positive case pct'].rolling(7, min_periods=0).mean().fillna(0)
        data = data.reset_index().sort_values(by='date')
    else:
        ny = df[df['state'] == 'NY']
        ca = df[df['state'] == 'CA']
        ga = df[df['state'] == 'GA']
        data = df[df['state'] == state]
        data = data[['date', 'positive case pct (last 7 days average)']]
        ny = ny[['date', 'positive case pct (last 7 days average)']]
        ca = ca[['date', 'positive case pct (last 7 days average)']]
        ga = ga[['date', 'positive case pct (last 7 days average)']]
    ys = data['positive case pct (last 7 days average)']
    xs = data['date']
    
    template_new = "%{customdata} tests over last 7 days on %{text}<extra></extra>"
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=xs,
            y=ys,
            text = data['date'],
            name="Positive pct",
            line={"color": "#6822D3"},
            customdata = [human_percentage(x) for x in data['positive case pct (last 7 days average)'].to_numpy()],
            hovertemplate=template_new

        )
    )
    # fig.add_trace(
    #     go.Scatter(
    #         x=list(range(0, length+1)),
    #         y=list(range(0, length+1)),
    #         mode="lines",
    #         text = None,
    #         name="Exponential Growth",
    #         line= dict(color='red', dash='dash'),
            

    #     )
    # )
    # fig.add_annotation(
    #     x=annotation_x,
    #     y=annotation_y,
    #     text='Exponential Growth',
    #     font={'size': 10},
    #     xshift=-65,
    #     showarrow=False
    # )
    # fig.add_trace(
    #     go.Scatter(
    #         x=np.log(ny['positive']),
    #         y=np.log(ny['new positive cases (last 7 days)']),
    #         name="Existing vs. New Cases",
    #         line={"color": "#F4B000"},
    #         customdata = [human_format(x) for x in data['new positive cases (last 7 days)'].to_numpy()],
    #         hovertemplate=template_new

    #     )
    # )
    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 1},
        template="plotly_dark",
        # annotations=annotations,
        autosize=True,
        showlegend=False,
        legend_orientation="h",
        paper_bgcolor="rgba(0,0,0,0)",
                # paper_bgcolor="black",
        plot_bgcolor="rgba(0,0,0,0)",
        #         plot_bgcolor="black",
        # xaxis_title="Number of Days",
        yaxis={"linecolor": "rgba(0,0,0,0)"},
        hoverlabel={"font": {"color": "black"}},
        xaxis_showgrid=False,
        yaxis_showgrid=False,
        font=dict(family="Roboto, sans-serif", size=10, color="#f4f4f4"),
        yaxis_title="Positive %"
        # xaxis_title="Total Existing Cases (Log)"
    )
    return fig