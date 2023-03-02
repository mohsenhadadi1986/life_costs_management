from dash import Dash, dcc, html, Input, Output, dash_table
from datetime import date
import dash_bootstrap_components as dbc
import pandas as pd
import pathlib
from app import app

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

df = pd.read_csv(DATA_PATH.joinpath('report.csv'))

report_year = [2023, 2024]


layout = html.Div([
    html.Div(children=[
        dbc.Label("Select Year", html_for="dropdown"),
        dcc.Dropdown(
            id='years-dropdown',
            options=report_year,
            placeholder="select a year"
        )
    ], className="item-input"),
    dbc.Label('Click a cell in the table:'),
    dash_table.DataTable(df.to_dict('records'), [
                         {"name": i, "id": i} for i in df.columns], id='tbl'),
    dbc.Alert(id='tbl_out'),
], className="report-container")


@app.callback(Output('tbl_out', 'children'), Input('tbl', 'active_cell'))
def update_graphs(active_cell):
    return str(active_cell) if active_cell else "Click the table"
