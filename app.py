# -*- coding: utf-8 -*-
import datetime
import dash
import plotly
import main_plot
import tech_indicator
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output, State
from fetch_data import fetch_market

import graph_menu

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)

server = app.server
# stock
stocks = ["TSLA","SPY"]
default_stock = stocks[0]
ticker_period = '1d'

# Creates HTML stock price
def get_row(stock):
    stock_data = fetch_market(' '.join(stocks), ticker_period, '1m')
    data = stock_data[stock]
    price = data.loc[data.index[-1], "Close"]
    last_price = data.loc[data.index[-2], "Close"]
    daily_return = (price-last_price)/last_price * 100

    return html.Div(
        children=[
            # Summary
            html.Div(
                id=stock + "summary",
                className="row summary",
                n_clicks=0,
                children=[
                    html.Div(
                        id=stock + "row",
                        className="row",
                        children=[
                            html.P(
                                stock,  # stock name
                                id=stock,
                                className="three-col",
                            ),
                            html.P(
                                price.round(2),  # price value
                                id=stock + "price",
                                className="three-col",
                            ),
                            html.P(
                                daily_return.round(2),  # daily return value
                                id=stock + "return",
                                className="three-col",
                                style={"color": get_color(daily_return)},
                            ),
                        ],
                    )
                ],
            ),
        ]
    )

# color of rates
def get_color(a):
    if a > 0:
        return "#45df7e"
    elif a < 0:
        return "#da5657"
    else:
        return "white"

# Returns graph figure
def get_fig(stock, type_trace, studies, interval):
    stock_data = fetch_market(' '.join(stocks),ticker_period, interval)
    df = stock_data[stock]
    if interval == '1h':
        df['Date'] = stock_data['Date']
    else:
        df['Date'] = stock_data['Datetime']

    subplot_traces = [  # first row traces
        "accumulation_trace",
        "cci_trace",
        "roc_trace",
        "stoc_trace",
        "mom_trace",
    ]
    selected_subplots_studies = []
    selected_first_row_studies = []
    row = 1  # number of subplots

    if studies:
        for study in studies:
            if study in subplot_traces:
                row += 1  # increment number of rows only if the study needs a subplot
                selected_subplots_studies.append(study)
            else:
                selected_first_row_studies.append(study)

    row_scale = {1:[1], 2:[0.8,0.2], 3:[0.6,0.2,0.2], 4:[0.55,0.15,0.15,0.15], 5:[0.4,0.15,0.15,0.15,0.15]}
    row_heights = row_scale[row]
     
    #fig = tools.make_subplots(
    fig = plotly.subplots.make_subplots(
        rows=row,
        shared_xaxes=True,
        shared_yaxes=True,
        cols=1,
        print_grid=False,
        vertical_spacing=0.05,
        row_heights = row_heights
    )

    # Add main trace (style) to figure
    fig.append_trace(main_plot.data_plot(df,type_trace), 1, 1)

    # Add trace(s) on fig's first row
    for study in selected_first_row_studies:
        fig = tech_indicator.tech_indicator_plot(df, study, fig)

    row = 1
    # Plot trace on new row
    for study in selected_subplots_studies:
        row += 1
        fig.append_trace(tech_indicator.tech_indicator_subplot(df, study), row, 1)

    fig.update_layout(
        uirevision="The User is always right",
        autosize=True,
        height=750,
        paper_bgcolor="#21252C",
        plot_bgcolor="#21252C",
        margin=dict(
                t=50,
                l=50,
                b=50,
                r=25
            ),
        xaxis=dict(
                tickformat="%y/%m/%d",
                gridcolor="#3E3F40",
                gridwidth=0.3,
                rangeslider=dict(
                        visible=False
                    )

            ),
        yaxis=dict(
                showgrid=True,
                gridcolor="#3E3F40",
                gridwidth=0.3
            ),
        )

    # subplot style
    row = 1
    for study in selected_subplots_studies:
        row += 1
        fig.update_xaxes(gridcolor="#3E3F40", row=row, col=1)
        fig.update_yaxes(gridcolor="#3E3F40", row=row, col=1)

    return fig

# returns chart div
def chart_div(stock):
    return html.Div(
        id="graph_div",
        className="chart-style twelve columns",
        children=[
            # Menu for stock Graph
            html.Div(
                id="menu",
                className="not_visible",
                children=[
                    # stores current menu tab
                    html.Div(
                        id="menu_tab",
                        children=["Studies"],
                        style={"display": "none"},
                    ),
                    html.Span(
                        "Style",
                        id="style_header",
                        className="span-menu",
                        n_clicks_timestamp=2,
                    ),
                    html.Span(
                        "Studies",
                        id="studies_header",
                        className="span-menu",
                        n_clicks_timestamp=1,
                    ),
                    # Studies Checklist
                    html.Div(
                        id="studies_tab",
                        children=[
                            dcc.Checklist(
                                id="studies",
                                options=[
                                    {
                                        "label": "Accumulation/D",
                                        "value": "accumulation_trace",
                                    },
                                    {
                                        "label": "Bollinger bands",
                                        "value": "bollinger_trace",
                                    },
                                    {"label": "MA", "value": "moving_average_trace"},
                                    {"label": "EMA", "value": "e_moving_average_trace"},
                                    {"label": "CCI", "value": "cci_trace"},
                                    {"label": "ROC", "value": "roc_trace"},
                                    {"label": "Pivot points", "value": "pp_trace"},
                                    {
                                        "label": "Stochastic oscillator",
                                        "value": "stoc_trace",
                                    },
                                    {
                                        "label": "Momentum indicator",
                                        "value": "mom_trace",
                                    },
                                ],
                                value=[],
                            )
                        ],
                        style={"display": "none"},
                    ),
                    # Styles checklist
                    html.Div(
                        id="style_tab",
                        children=[
                            dcc.RadioItems(
                                id="chart_type",
                                options=[
                                    {
                                        "label": "candlestick",
                                        "value": "candlestick_trace",
                                    },
                                    {"label": "line", "value": "line_trace"},
                                ],
                                value="candlestick_trace",
                            )
                        ],
                    ),
                ],
            ),
            # Chart Top Bar
            html.Div(
                className="row chart-top-bar",
                children=[
                    html.Span(
                        id="menu_button",
                        className="inline-block chart-title",
                        children=f"{stock} ☰",
                        n_clicks=0,
                    ),
                    # Dropdown and close button float right
                    html.Div(
                        className="graph-top-right inline-block",
                        children=[
                            html.Div(
                                className="inline-block",
                                children=[
                                    dcc.Dropdown(
                                        className="dropdown-period",
                                        id="dropdown_interval",
                                        options=[
                                            {"label": "1 min", "value": "1m"},
                                            {"label": "2 min", "value": "2m"},
                                            {"label": "5 min", "value": "5m"},
                                            {"label": "15 min", "value": "15m"},
                                            {"label": "30 min", "value": "30m"},
                                            {"label": "1 hour", "value": "60m"}
                                        ],
                                        value="1m",
                                        clearable=False,
                                    )
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            # Graph div
            html.Div(
                dcc.Graph(
                    id="chart",
                    className="chart-graph",
                    config={"displayModeBar": False, "scrollZoom": True},
                )
            ),
        ],
    )

# Dash App Layout
app.layout = html.Div(
    className="row",
    children=[
        # Interval component for live clock
        dcc.Interval(id="interval", interval=1 * 1000, n_intervals=0),
        # # Interval component for ask bid updates
        # dcc.Interval(id="i_bis", interval=1 * 2000, n_intervals=0),
        # Interval component for graph updates
        dcc.Interval(id="i_tris", interval=1 * 2000, n_intervals=0),
        # Right Panel Div
        html.Div(
            className="nine columns div-left-panel",
            children=[
                # Charts Div
                html.Div(
                    id="charts",
                    className="row",
                    children=[
                        html.Div(
                            chart_div('AAPL')
                        ),
                    ],
                ),
            ],
        ),
        # Left Panel Div
        html.Div(
            className="three columns div-right-panel",
            children=[
                # Div for Left Panel App Info
                html.Div(
                    className="div-info",
                    children=[
                        html.H4('Intraday Stock Technical Analysis Platform'),
                        html.P(
                            """
                            This app fetch data from yafoo finance and display prices
                            for stocks as well as Stock Charts for intraday stock analysis.
                            """
                        ),
                    ],
                ),
                # Ask Bid stock Div
                html.Div(
                    className="div-stock-toggles",
                    children=[
                        html.P(
                            id="live_clock",
                            className="three-col",
                            children=datetime.datetime.now().strftime("%H:%M:%S"),
                        ),
                        html.P(className="three-col", children="Price"),
                        html.P(className="three-col", children="%"),
                        html.Div(
                            id="stocks",
                            className="div-price",
                            children=[
                                get_row(stock)
                                for stock in stocks
                            ],
                        ),
                    ],
                ),
            ],
        ),
        
        # Hidden div that stores all clicked charts
        html.Div(id="charts_clicked", style={"display": "none"},children=[','.join(['0']*len(stocks))]),
        # Hidden div that stores all clicked charts
        html.Div(id="pre_charts_clicked", style={"display": "none"},children=[','.join(['0']*len(stocks))]),
    ],
)

# Dynamic Callbacks

# Function to create Graph Figure
def generate_figure_callback(stock):
    def chart_fig_callback(*args):
        t = args[0]
        s = args[1]
        p = args[2]
        current_click = args[3][0].split(',')
        pre_click = args[5][0].split(',')
        for i in range(len(pre_click)):
            if pre_click[i] != current_click[i]:
                fig = get_fig(stocks[i],  t, s, p)
                return [fig,f"{stocks[i]} ☰"]
        
        fig = get_fig(stock,  t, s, p)
        return [fig, f"{stock} ☰"]

    return chart_fig_callback

# Callback to update the actual graph
app.callback(
    [
        Output("chart", "figure"),
        Output("menu_button","children")
    ],
    [
        Input("chart_type", "value"),
        Input("studies", "value"),
        Input("dropdown_interval", "value"),
        Input("charts_clicked","children"),
        Input("i_tris", "n_intervals")
    ],
    [State("pre_charts_clicked","children")],
)(generate_figure_callback(default_stock))

# show or hide graph menu
app.callback(
    Output("menu", "className"),
    [Input("menu_button", "n_clicks")],
    [State("menu", "className")],
)(graph_menu.generate_open_close_menu_callback())

# stores in hidden div name of clicked tab name
app.callback(
    [
        Output("menu_tab", "children"),
        Output("style_header", "className"),
        Output("studies_header", "className"),
    ],
    [
        Input("style_header", "n_clicks_timestamp"),
        Input("studies_header", "n_clicks_timestamp"),
    ],
)(graph_menu.generate_active_menu_tab_callback())

# hide/show STYLE tab content if clicked or not
app.callback(
    Output("style_tab", "style"), [Input("menu_tab", "children")]
)(graph_menu.generate_style_content_tab_callback())

# hide/show MENU tab content if clicked or not
app.callback(
    Output("studies_tab", "style"), [Input("menu_tab", "children")]
)(graph_menu.generate_studies_content_tab_callback())

# returns string containing clicked charts
def check_stock_clicked_callback():
    def check_stock_clicked(*args):
        click_event = list(args[:-2])
        previous_clicked = args[-2]
        click_event = [str(i) for i in click_event]
        click_event = [','.join(click_event)]
        return click_event, previous_clicked
    return check_stock_clicked

# hidden div with all the clicked charts 
app.callback(
    [   
        Output("charts_clicked", "children"),
        Output("pre_charts_clicked","children"),
    ],
    [Input(stock + "summary", "n_clicks") for stock in stocks],
    [
        State("charts_clicked","children"),
        State("pre_charts_clicked","children"),
    ]
)(check_stock_clicked_callback())

# Callback to update live clock
@app.callback(Output("live_clock", "children"), [Input("interval", "n_intervals")])
def update_time(n):
    return datetime.datetime.now().strftime("%H:%M:%S")

if __name__ == "__main__":
    app.run_server(debug=True)
