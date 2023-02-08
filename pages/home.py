from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc


# Connect to main app.py file
from app import app
from app import server

trueOnlyLogoUri = app.get_asset_url('./img/true_only_logo.png')
trueOnlyLabel = app.get_asset_url('./img/true_only_label.png')
homeIcon = app.get_asset_url('./img/home_icon.svg')
searchIcon = app.get_asset_url('./img/search_icon.svg')
bellIcon = app.get_asset_url('./img/bell_icon.svg')
reputationIcon = app.get_asset_url('./img/reputation_icon.svg')
closeIcon = app.get_asset_url('./img/close_icon.svg')

layout = html.Div(className='col-contents', children=[
    html.Div(id='', className='', children=[
        html.H1(id='lib-title', className='',
                children='Cost management for life'),
    ]),
    dbc.Row(
        dbc.Col("In this web app we try to manage the life cost")
    )
])
