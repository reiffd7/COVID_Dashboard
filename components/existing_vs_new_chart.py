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



def existing_vs_new_chart(state="US"):

    df = StatesDataFrame().df
    df['date'] = pd.DatetimeIndex(df['date']).strftime("%Y-%m-%d")
    if state == 'United States':
        data = df.groupby('date').sum()[['positive', 'new positive cases (last 7 days)']]
        data = data.reset_index().sort_values(by='date')
    else:
        ny = df[df['state'] == 'NY']
        ca = df[df['state'] == 'CA']
        data = df[df['state'] == state]
        data = data[['date', 'positive', 'new positive cases (last 7 days)']]
        ny = ny[['date', 'positive', 'new positive cases (last 7 days)']]
        ca = ca[['date', 'positive', 'new positive cases (last 7 days)']]
    ys = np.log(data['new positive cases (last 7 days)'])
    xs = np.log(data['positive'])
    length = math.ceil(max(max(ys), max(xs)))
    annotation_x = length+1
    annotation_y = length+1
    template_new = "%{customdata} new cases on %{text}<extra></extra>"
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=xs,
            y=ys,
            text = data['date'],
            name="Existing vs. New Cases",
            line={"color": "#FFCF00"},
            customdata = [human_format(x) for x in data['new positive cases (last 7 days)'].to_numpy()],
            hovertemplate=template_new

        )
    )
    fig.add_trace(
        go.Scatter(
            x=list(range(0, length+1)),
            y=list(range(0, length+1)),
            mode="lines",
            text = None,
            name="Exponential Growth",
            line= dict(color='#941B0C', dash='dash'),
            

        )
    )
    fig.add_annotation(
        x=annotation_x,
        y=annotation_y,
        text='Exponential Growth',
        font={'size': 10},
        xshift=-65,
        showarrow=False
    )
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
        #         paper_bgcolor="black",
        plot_bgcolor="rgba(0,0,0,0)",
        #         plot_bgcolor="black",
        # xaxis_title="Number of Days",
        yaxis={"linecolor": "rgba(0,0,0,0)"},
        hoverlabel={"font": {"color": "black"}},
        xaxis_showgrid=False,
        yaxis_showgrid=False,
        font=dict(family="Roboto, sans-serif", size=10, color="#f4f4f4"),
        yaxis_title="New Cases Last Week (Log)",
        xaxis_title="Total Existing Cases (Log)"
    )
    return fig