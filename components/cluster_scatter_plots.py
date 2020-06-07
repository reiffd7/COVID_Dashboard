import pandas as pd   
import numpy as np   
import plotly.graph_objects as go
import plotly.express as px
from sklearn.cluster import KMeans, AgglomerativeClustering, AffinityPropagation #For clustering
import math

import sys
sys.path.append('../')
from utils import StatesDataFrame


def KmeansClustering(X, nclust=4):
    model = KMeans(nclust)
    model.fit(X)
    clust_labels = model.predict(X)
    return clust_labels



def compare_scatter(criteria1, criteria2):
    df = StatesDataFrame().df
    df = df.fillna(0)
#     df = df[df['date'] == max(df['date'])]
    last_date = max(df.date)
#     df.drop(columns=['index', 'fips'], inplace=True)
#     df = df[['date''state','new positive (per capita)', 'tests last week (per capita)', 
#     'testing rate of change (last 7 days average)', 'positive case pct rate of change (last 7 days average)',
#     'positive cases rate of change (last 7 days average)']]
    df = df[['date', 'state', criteria1, criteria2]]
    df0 = df[df['date'] == last_date]
    states = df0.state
    X_forClust = df0.iloc[:, 2:]
    df0['clusters'] = KmeansClustering(X_forClust)
    # trace0 = go.Heatmap(
    #     x = df0[criteria1],
    #     y = df0[criteria2],
    #     z = df0['clusters'],
    #     zsmooth = "best",
    #     colorscale=['#F5BE05', '#2EC152', '#2E39C1', '#8E2EC1'],
    #     opacity=0.65,
    #     colorbar = {'tickvals': [0, 1, 2, 3]}
    #     )
    trace1 = go.Scatter(
    x = df0[criteria1],
    y = df0[criteria2],
    mode = 'markers+text',
    text = df0['state'],
    marker=dict(
        color = df0['clusters']
    ),
    textposition = 'top center',
    showlegend=False,
    textfont = {'color': 'white'}
    )
    fig = go.Figure()
    # fig.add_trace(trace0)
    fig.add_trace(trace1)
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
        title='{} vs {}'.format(criteria1, criteria2),
        xaxis_title = criteria1,
        yaxis_title = criteria2
    )
    return fig