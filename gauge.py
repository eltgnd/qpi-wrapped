# From https://github.com/andfanilo/social-media-tutorials/tree/master/20230816-stdashboard

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

def plot_gauge(
    indicator_number, indicator_color, indicator_suffix, indicator_title, max_bound
):
    fig = go.Figure(
        go.Indicator(
            value=indicator_number,
            mode="gauge+number",
            domain={"x": [0, 1], "y": [0, 1]},
            number={
                "suffix": indicator_suffix,
                "font.size": 48,
            },
            gauge={
                "axis": {"range": [0, max_bound], "tickwidth": 1},
                "bar": {"color": indicator_color},
            },
            title={
                "text": indicator_title,
                "font": {"size": 26},
                "align": "left",
            },
        )
    )
    fig.update_layout(
        # paper_bgcolor="lightgrey",
        height=198,
        margin=dict(l=20, r=20, t=30, b=0),
    )
    st.plotly_chart(fig, use_container_width=True)
