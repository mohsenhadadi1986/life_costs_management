
from dash.dependencies import Input, Output
from dash import html, dcc


# Connect to main app.py file
from app import app
from app import server
import pages.home as home
import pages.insert as importer 
import pages.analytics as analytics
import pages.report as report
import components.sidebar as sidebar


app.layout = html.Div(className='container',
                      children=[
                          dcc.Location(id='url', refresh=False),
                          html.Div(className='col-sidebar', children=[
                              sidebar.layout
                          ]),
                          html.Div(id='page-content', className='container-contents', children=[
                              home.layout
                          ])
                      ])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/import':
        return importer.layout
    if pathname == '/apps/analytics':
        return analytics.layout
    if pathname == '/apps/year':
        return report.layout
    else:
        return home.layout


if __name__ == '__main__':
    app.run_server(debug=True)
