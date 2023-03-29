from dash import Dash, dcc, html, Input, Output, dash_table
from datetime import date
import dash_bootstrap_components as dbc
import pandas as pd
import pathlib
from app import app
import requests
import json


def get_report(year):
    re = requests.get(
        'http://127.0.0.1:5000/api/v1/report/{}'.format(year)).content
    response = json.loads(re)
    return response


PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

df = pd.read_csv(DATA_PATH.joinpath('report_{}.csv'.format(2022)))

report_year = [2022, 2023, 2024]


layout = html.Div([
    html.H1('Report'),
    html.Div(children=[
        dbc.Label("Select Year", html_for="dropdown"),
        dcc.Dropdown(
            id='years-dropdown',
            options=report_year,
            value='2022',
            placeholder="select a year"
        )
    ], className="item-input"),
    dash_table.DataTable(data=df.to_dict('records'),
                         columns=[
                         {"name": i, "id": i} for i in df.columns],
                         id='table',
                         style_cell={'textAlign': 'left', 'padding': '5px'},
                         style_as_list_view=True,
                         style_data={
        'color': 'black',
        'backgroundColor': 'white'
    },
        style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(220, 220, 220)',
        }
    ],
        style_header={
        'backgroundColor': 'rgb(210, 210, 210)',
        'color': 'black',
        'fontWeight': 'bold'
    }),
], className="report-container")

# Define the callback function


@app.callback(
    Output('table', 'data'),
    [Input('years-dropdown', 'value')]
)
def update_table(year):
    # Filter the data frame based on the selected value
    if year is None:
        return
    get_report(year)

    PATH = pathlib.Path(__file__).parent
    DATA_PATH = PATH.joinpath("../datasets").resolve()

    df = pd.read_csv(DATA_PATH.joinpath('report_{}.csv'.format(year)))

    return df.to_dict('records')
