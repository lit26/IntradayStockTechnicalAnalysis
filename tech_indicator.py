import pandas as pd
import plotly.graph_objs as go

####### STUDIES TRACES ######
def tech_indicator_plot(df, study, fig):
    return eval(study)(df, fig)

def tech_indicator_subplot(df, study):
	return eval(study)(df)

# Moving average
def moving_average_trace(df, fig):
    MA = df["Close"].rolling(window=5).mean()
    trace = go.Scatter(
        x=df["Date"], y=MA, mode="lines", showlegend=False, name="MA",
        line=dict(width=1)
    )
    fig.append_trace(trace, 1, 1)  # plot in first row
    return fig

# Exponential moving average
def e_moving_average_trace(df, fig):
    EMA = df["Close"].rolling(window=20).mean()
    trace = go.Scatter(
        x=df["Date"], y=EMA, mode="lines", showlegend=False, name="EMA",
        line=dict(width=1)
    )
    fig.append_trace(trace, 1, 1)  # plot in first row
    return fig


# Bollinger Bands
def bollinger_trace(df, fig, window_size=10, num_of_std=5):
    price = df["Close"]
    rolling_mean = price.rolling(window=window_size).mean()
    rolling_std = price.rolling(window=window_size).std()
    upper_band = rolling_mean + (rolling_std * num_of_std)
    Lower_band = rolling_mean - (rolling_std * num_of_std)

    trace = go.Scatter(
        x=df["Date"], y=upper_band, mode="lines", showlegend=False, name="BB_upper",
        line=dict(width=1)
    )

    trace2 = go.Scatter(
        x=df["Date"], y=rolling_mean, mode="lines", showlegend=False, name="BB_mean",
        line=dict(width=1)
    )

    trace3 = go.Scatter(
        x=df["Date"], y=Lower_band, mode="lines", showlegend=False, name="BB_Lower",
        line=dict(width=1)
    )

    fig.append_trace(trace, 1, 1)  # plot in first row
    fig.append_trace(trace2, 1, 1)  # plot in first row
    fig.append_trace(trace3, 1, 1)  # plot in first row
    return fig

# Accumulation Distribution
def accumulation_trace(df):
    df["Volume"] = ((df["Close"] - df["Low"]) - (df["High"] - df["Close"])) / (
        df["High"] - df["Low"]
    )
    trace = go.Scatter(
        x=df["Date"], y=df["Volume"], mode="lines", showlegend=False, name="Accumulation",
        line=dict(width=1)
    )
    return trace


# Commodity Channel Index
def cci_trace(df, ndays=5):
    TP = (df["High"] + df["Low"] + df["Close"]) / 3
    CCI = pd.Series(
        (TP - TP.rolling(window=10, center=False).mean())
        / (0.015 * TP.rolling(window=10, center=False).std()),
        name="cci",
    )
    trace = go.Scatter(
    	x=df["Date"], y=CCI, mode="lines", showlegend=False, name="CCI",
    	line=dict(width=1)
    )
    return trace


# Price Rate of Change
def roc_trace(df, ndays=5):
    N = df["Close"].diff(ndays)
    D = df["Close"].shift(ndays)
    ROC = pd.Series(N / D, name="roc")
    trace = go.Scatter(
    	x=df["Date"], y=ROC, mode="lines", showlegend=False, name="ROC",
    	line=dict(width=1)
    )
    return trace


# Stochastic oscillator %K
def stoc_trace(df):
    SOk = pd.Series((df["Close"] - df["Low"]) / (df["High"] - df["Low"]), name="SO%k")
    trace = go.Scatter(
    	x=df["Date"], y=SOk, mode="lines", showlegend=False, name="SO%k",
    	line=dict(width=1)
    )
    return trace


# Momentum
def mom_trace(df, n=5):
    M = pd.Series(df["Close"].diff(n), name="Momentum_" + str(n))
    trace = go.Scatter(
    	x=df["Date"], y=M, mode="lines", showlegend=False, name="MOM",
    	line=dict(width=1)
    )
    return trace


# Pivot points
def pp_trace(df, fig):
    PP = pd.Series((df["High"] + df["Low"] + df["Close"]) / 3)
    R1 = pd.Series(2 * PP - df["Low"])
    S1 = pd.Series(2 * PP - df["High"])
    R2 = pd.Series(PP + df["High"] - df["Low"])
    S2 = pd.Series(PP - df["High"] + df["Low"])
    R3 = pd.Series(df["High"] + 2 * (PP - df["Low"]))
    S3 = pd.Series(df["Low"] - 2 * (df["High"] - PP))
    trace = go.Scatter(
    	x=df["Date"], y=PP, mode="lines", showlegend=False, name="PP",
    	line=dict(width=1)
    )
    trace1 = go.Scatter(x=df["Date"], y=R1, mode="lines", showlegend=False, name="R1",
    	line=dict(width=1)
    )
    trace2 = go.Scatter(x=df["Date"], y=S1, mode="lines", showlegend=False, name="S1",
    	line=dict(width=1)
    )
    trace3 = go.Scatter(x=df["Date"], y=R2, mode="lines", showlegend=False, name="R2",
    	line=dict(width=1)
    )
    trace4 = go.Scatter(x=df["Date"], y=S2, mode="lines", showlegend=False, name="S2",
    	line=dict(width=1)
    )
    trace5 = go.Scatter(x=df["Date"], y=R3, mode="lines", showlegend=False, name="R3",
    	line=dict(width=1)
    )
    trace6 = go.Scatter(x=df["Date"], y=S3, mode="lines", showlegend=False, name="S3",
    	line=dict(width=1)
    )
    fig.append_trace(trace, 1, 1)
    fig.append_trace(trace1, 1, 1)
    fig.append_trace(trace2, 1, 1)
    fig.append_trace(trace3, 1, 1)
    fig.append_trace(trace4, 1, 1)
    fig.append_trace(trace5, 1, 1)
    fig.append_trace(trace6, 1, 1)
    return fig



