from dash import Dash, dcc, html, Input, Output, dash_table
from datetime import date
import dash_bootstrap_components as dbc
import pandas as pd
import pathlib
from app import app
import requests
import json
import io
import base64
import urllib.parse


def get_report_df(year):
    re = requests.get(
        'http://127.0.0.1:5000/api/v1/report/{}'.format(year)).content
    response = json.loads(re)
    if response:
        PATH = pathlib.Path(__file__).parent
        DATA_PATH = PATH.joinpath("../datasets").resolve()
        df = pd.read_csv(DATA_PATH.joinpath('report_{}.csv'.format(year)))
        return df


df = get_report_df(2023)
report_year = [2022, 2023, 2024]
report_type = ['Cost', 'Input', 'Income']


layout = html.Div([
    html.H1('Report'),
    html.Div(children=[
        dbc.Label("Select Year", html_for="dropdown"),
        html.Div(
            [
                dcc.Dropdown(
                    id='years-dropdown',
                    className='costumized-dd',
                    options=[{'label': str(year), 'value': year}
                             for year in report_year],
                    value='2023',
                    placeholder="select a year"
                ),

                dbc.Button(children='Download report',
                           id='report-download',
                           className='btn-report-download'),
            ],
            className='input-button-report-download'
        ),
        dbc.Label("Select report type", html_for="dropdown"),
        html.Div(
            [
                dcc.Dropdown(
                    id='type-report-dropdown',
                    className='costumized-dd',
                    options=[{'label': str(year), 'value': year}
                             for year in report_type],
                    value='',
                    placeholder="select a type"
                ),
            ],
            className='input-button-report-download'
        ),
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


@app.callback(
    Output('table', 'data'),
    [Input('years-dropdown', 'value'),
     Input('type-report-dropdown', 'value')]
)
def update_table(year, report_type):
    # Filter the data frame based on the selected value
    if year is None:
        return

    df = get_report_df(year)
    if report_type == '' or report_type is None:
        return df.to_dict('records')
    else:
        type_df = df[df['TITLE'].str.contains(report_type)].copy()
        type_df.loc['Total'] = type_df.sum(numeric_only=True)
        type_df.loc['Total', 'TITLE'] = 'TOTAL'
        return type_df.to_dict('records')


@app.callback(
    Output('report-download', 'href'),
    Output('report-download', 'download'),
    Output('report-download', 'children'),
    [Input('years-dropdown', 'value')],
    # prevent_initial_call=True
)
def update_download_link(year):
    if year is None:
        return '', '', 'Download report'

    df = get_report_df(year)
    csv_string = df.to_csv(index=False, encoding='utf-8')
    csv_string = "data:text/csv;charset=utf-8," + \
        urllib.parse.quote(csv_string)

    return csv_string, f'report_{year}.csv', f'report_{year}.csv'
