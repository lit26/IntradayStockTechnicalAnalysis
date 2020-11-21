import pandas as pd
import plotly.graph_objs as go

# MAIN CHART TRACES (STYLE tab)
def data_plot(df, type_trace):
    return eval(type_trace)(df)

def line_trace(df):
    trace = go.Scatter(
        x=df['Date'], y=df["Close"], mode="lines", showlegend=False, name="line"
    )
    return trace

def candlestick_trace(df):
    return go.Candlestick(
        x=df['Date'],
        open=df["Open"],
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        increasing=dict(line=dict(color="green")),
        decreasing=dict(line=dict(color="red")),
        showlegend=False,
        name="candlestick",
    )