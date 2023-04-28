from dash import Dash, dcc, html, Input, Output, State, callback_context
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
    html.H1('Import'),
    html.Div(children=[
        dbc.Label("Category", html_for="dropdown"),
        dcc.Dropdown(
            id='categories-dropdown',
            options=[{'label': k, 'value': k} for k in all_options.keys()],
            placeholder="select a category"
        )
    ], className="item-input"),

    html.Div(children=[
        dbc.Label("Source", html_for="dropdown"),
        dcc.Dropdown(
            id='source-dropdown',
            options=[{'label': i, 'value': i} for i in all_options['Input']],
            placeholder="select a source",
        )
    ], className="item-input", id='source-div', style={'display': 'none'}),


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


def summarized_results(reason, category, amount, date, source):
    dict_data = {}
    if category is not None:
        if amount is not None:
            dict_data['category'] = category
            dict_data['reason'] = reason
            dict_data['value'] = amount
            dict_data['import_date'] = date
            dict_data['source'] = source
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
    [Output('cost-reason-dropdown', 'options'),
     Output('source-div', 'style')],
    [Input('categories-dropdown', 'value')])
def set_reason_cost_options(selected_category):
    if selected_category is None:
        return [], {'display': 'none'}
    elif selected_category == 'Cost':
        return [{'label': i, 'value': i} for i in all_options[selected_category]], {'display': 'block'}
    else:
        return [{'label': i, 'value': i} for i in all_options[selected_category]], {'display': 'none'}


@app.callback(
    Output('cost-reason-dropdown', 'value'),
    [Input('cost-reason-dropdown', 'options')])
def set_reason_cost_value(available_options):
    if len(available_options) == 0:
        return None
    else:
        return available_options[0]['value']


@app.callback(
    Output('source-dropdown', 'value'),
    [Input('source-dropdown', 'options'),
     Input('source-div', 'style')])
def set_source_value(available_options, display_source):
    if len(available_options) == 0:
        return None
    elif display_source['display'] == 'none':
        return None
    else:
        return available_options[0]['value']


@app.callback(
    Output('display-selected-values', 'children'),
    [Input('submit-val', 'n_clicks')],
    [State('categories-dropdown', 'value'),
     State('cost-reason-dropdown', 'value'),
     State("dtrue", "value"),
     State('my-date-picker-single', 'date'),
     State('source-dropdown', 'value'),])
def set_display_children(n_clicks, selected_category, selected_cost_reason, input_number, date, source):
    if n_clicks is None:
        return ''

    if n_clicks > 0:
        return summarized_results(selected_cost_reason, selected_category, input_number, date, source)
    else:
        return ''
