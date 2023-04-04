from dash import Dash, dcc, html, Input, Output, State, callback_context
from datetime import date
import dash_bootstrap_components as dbc
from app import app
import pandas as pd
import numpy as np
import plotly.express as px
import json
import pathlib
import requests


def get_report(year):
    re = requests.get(
        'http://127.0.0.1:5000/api/v1/report/{}'.format(year)).content
    response = json.loads(re)
    return response


PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

df = pd.read_csv(DATA_PATH.joinpath('report_{}.csv'.format(2023)))

report_year = [2022, 2023]

layout = html.Div([
    html.H1('Analytics'),
    html.Div(children=[
        dbc.Label("Select Year", html_for="dropdown"),
        dcc.Dropdown(
            id='years-dropdown',
            options=report_year,
            value='2023',
            placeholder="select a year"
        )
    ], className="item-input"),
    html.Div(children=[
        html.Label('Select Title:'),
        dcc.Dropdown(
            id='title-dropdown',
            # options=[],
            # value=df['TITLE'].unique()[0]
        )
    ], className="item-input"),
    html.Div(children=[
        html.Label('Select Time Range:'),
        dcc.RangeSlider(
            id='time-range-slider',
            min=1,
            max=12,
            step=1,
            marks={i: f'Month {i}' for i in range(1, 13)},
            value=[1, 12]
        )
    ]),
    html.Hr(),
    dcc.Graph(id='plot')
])


@app.callback(
    [Output('title-dropdown', 'options'),
     Output('title-dropdown', 'value')],
    Input('years-dropdown', 'value'),
    # prevent_initial_call=True
)
def set_reason_cost_options(selected_year, df=df):
    if selected_year is None:
        return [], None
    if selected_year == '2023':
        get_report(selected_year)

        PATH = pathlib.Path(__file__).parent
        DATA_PATH = PATH.joinpath("../datasets").resolve()
        df = pd.read_csv(DATA_PATH.joinpath(
            'report_{}.csv'.format(selected_year)))
        return [{'label': i, 'value': i} for i in df['TITLE'].tolist()], df['TITLE'].tolist()[0]
    elif selected_year != 2023:
        get_report(selected_year)

        PATH = pathlib.Path(__file__).parent
        DATA_PATH = PATH.joinpath("../datasets").resolve()
        df = pd.read_csv(DATA_PATH.joinpath(
            'report_{}.csv'.format(selected_year)))
        return [{'label': i, 'value': i} for i in df['TITLE'].tolist()], df['TITLE'].tolist()[0]


@app.callback(Output('plot', 'figure'),
              [
    Input('title-dropdown', 'value'),
                  Input('time-range-slider', 'value')],
    State('years-dropdown', 'value'),
    prevent_initial_call=True)
def set_display_children(title, time_range, year):

    get_report(year)

    PATH = pathlib.Path(__file__).parent
    DATA_PATH = PATH.joinpath("../datasets").resolve()

    df = pd.read_csv(DATA_PATH.joinpath('report_{}.csv'.format(year)))
    filtered_df = df[df['TITLE'] == title].replace(np.nan, 0)
    # select only columns within the time range
    filtered_df = filtered_df.iloc[:, time_range[0]+1:time_range[1]+2]
    x = filtered_df.columns.tolist()
    y = filtered_df.iloc[0, :].tolist() if filtered_df.size > 0 else []
    # Use the new DataFrame to create a Plotly line chart
    fig = px.line(x=x, y=y)
    fig.update_layout(title=title, xaxis_title='time', yaxis_title=title)

    return fig
