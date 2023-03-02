from dash import Dash, dcc, html, Input, Output
from datetime import date
import dash_bootstrap_components as dbc
from app import app
import requests
import flask
import json


def get_data():
    re = requests.get('http://127.0.0.1:5000/api/v1/dropdown_options').content
    response = json.loads(re)
    return response


all_options = get_data()

layout = html.Div([
    html.Div(children=[
        dbc.Label("Category", html_for="dropdown"),
        dcc.Dropdown(
            id='categories-dropdown',
            options=[{'label': k, 'value': k} for k in all_options.keys()],
            placeholder="select a category"
        )
    ], className="item-input"),

    html.Div(children=[
        dbc.Label("Reason", html_for="dropdown"),
        dcc.Dropdown(id='cost-reason-dropdown', placeholder="selec a reason"),
    ], className="item-input"),

    html.Div(children=[
        dbc.Label("Amount", html_for="dropdown"),
        dbc.Input(
            id="dtrue", type="number", placeholder="input with range",
            # min=0, step=1, debounce=True
        ),
    ], className="item-input"),

    html.Div(children=[
        dbc.Label("Date", html_for="dropdown"),
        dcc.DatePickerSingle(
            id='my-date-picker-single',
            date=date.today(),
            placeholder='Select a date',
            display_format='MMMM Y, DD',
            className="date-picker")
    ], className="item-label"
    ),

    html.Hr(),

    html.Div(id='display-selected-values'),
    html.Button("Submit", id="submit-val", className="submit-button")
])


def summarized_results(reason, category, amount, date):
    dict_data = {}
    if category is not None:
        if amount is not None:
            dict_data['category'] = category
            dict_data['reason'] = reason
            dict_data['value'] = amount
            dict_data['import_date'] = date
            print(dict_data)
            response = requests.post(
                'http://127.0.0.1:5000/api/v1/import_data', json=dict_data).content
            return html.Div(children=[
                html.P(
                    reason.upper() + " in the category " + category.upper()
                    + " with amount of " +
                    str(amount) + " € in " + date +
                    " has rgistered. The submit button has trigged."
                ), html.P(json.loads(response)['response'])
            ])
        else:
            return "Please insert an amount"
    else:
        return "Please seletc a category"


@app.callback(
    Output('cost-reason-dropdown', 'options'),
    [Input('categories-dropdown', 'value')])
def set_reason_cost_options(selected_category):
    if selected_category is None:
        return []
    else:
        return [{'label': i, 'value': i} for i in all_options[selected_category]]


@app.callback(
    Output('cost-reason-dropdown', 'value'),
    [Input('cost-reason-dropdown', 'options')])
def set_reason_cost_value(available_options):
    if len(available_options) == 0:
        return ''
    else:
        return available_options[0]['value']


@app.callback(
    Output('display-selected-values', 'children'),
    [Input('categories-dropdown', 'value'),
     Input('cost-reason-dropdown', 'value'),
     Input("dtrue", "value"),
     Input('my-date-picker-single', 'date'),
     Input('submit-val', 'n_clicks'),])
def set_display_children(selected_category, selected_cost_reason, input_number, date, n_clicks):
    # return u'{} in the {} category with amount of {} € in {} has rgistered.'.format(
    #     selected_cost_reason, selected_category, input_number, date
    # )
    if n_clicks:
        return summarized_results(selected_cost_reason,
                                  selected_category, input_number, date)
