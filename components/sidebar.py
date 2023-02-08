from dash import html, dcc
from dash.dependencies import Input, Output


# Connect to main app.py file
from app import app

trueOnlyLogoUri = app.get_asset_url('./img/cost_of_life.png')
homeIcon = app.get_asset_url('./img/home_icon.svg')
searchIcon = app.get_asset_url('./img/import.svg')
analytics = app.get_asset_url('./img/analytics.svg')
report = app.get_asset_url('./img/report.svg')
closeIcon = app.get_asset_url('./img/close_icon.svg')


layout = html.Div([
    html.Div(className='two-logos', children=[
        html.Img(className='true-logo', children=[],
                 src=trueOnlyLogoUri, alt='logo'),
    ]),
    dcc.Link(children=[
        html.Div(className='buttton-label-sidebar', children=[
            html.Img(src=homeIcon),
             html.Div("Home", className='label-side-bar')
             ])
    ], href='/',
        className='link-navigation-button', id='active'),
    dcc.Link(children=[
        html.Div(className='buttton-label-sidebar', children=[
            html.Img(src=searchIcon),
             html.Div("Import", className='label-side-bar')
             ])
    ], href='/apps/import',
        className='link-navigation-button'),
    dcc.Link(children=[
        html.Div(className='buttton-label-sidebar', children=[
            html.Img(src=analytics),
            html.Div("Analytics", className='label-side-bar')
        ])
    ], href='/apps/analytics',
        className='link-navigation-button'
    ),
    dcc.Link(children=[
        html.Div(className='buttton-label-sidebar', children=[
            html.Img(src=report),
            html.Div("Report for Year", className='label-side-bar')
        ])
    ], href='/apps/report',
        className='link-navigation-button'
    ),

], className="nav-bar")
