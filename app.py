import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import yfinance as yf
import pandas as pd
import plotly.express as px
from datetime import datetime as dt

# Initialize the app
app = dash.Dash(__name__)
server = app.server

# Define the layout
app.layout = html.Div(className='container', children=[
    html.Div(className='inputs', children=[
        html.P("Welcome to the Stock Dash App!", className="start"),
        html.Div([
            dcc.Input(id='stock-code', type='text', placeholder='Enter Stock Code'),
        ]),
        html.Div([
            dcc.DatePickerRange(
                id='date-picker-range',
                start_date=dt(2020, 1, 1),
                end_date=dt.today().date()
            ),
        ]),
        html.Div([
            html.Button('Submit', id='submit-button', n_clicks=0)
        ]),
    ]),
    html.Div(className='content', children=[
        html.Div(className='header', children=[
            html.Img(id='company-logo', src=''),
            html.H1(id='company-name', children=''),
        ]),
        html.Div(id='description', className='description_ticker'),
        html.Div(id='graphs-content', children=[
            dcc.Graph(id='stock-graph')
        ]),
        html.Div(id='forecast-content', children=[
            dcc.Graph(id='forecast-graph')
        ])
    ])
])

# Callback to update company info and stock graph
@app.callback(
    [Output('company-logo', 'src'),
     Output('company-name', 'children'),
     Output('description', 'children'),
     Output('stock-graph', 'figure')],
    [Input('submit-button', 'n_clicks')],
    [State('stock-code', 'value'), State('date-picker-range', 'start_date'), State('date-picker-range', 'end_date')]
)
def update_output(n_clicks, stock_code, start_date, end_date):
    if n_clicks > 0 and stock_code:
        ticker = yf.Ticker(stock_code)
        info = ticker.info
        df = ticker.history(start=start_date, end=end_date)
        
        company_logo = info.get('logo_url', '')
        company_name = info.get('shortName', 'N/A')
        company_description = info.get('longBusinessSummary', 'Description not available.')
        
        fig = px.line(df, x=df.index, y=['Open', 'Close'], title=f'{company_name} Stock Price')
        
        return company_logo, company_name, company_description, fig
    else:
        return '', '', '', {}

import os
from dash import Dash

app = Dash(__name__)

# Your app layout and callbacks here

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8050))  # Render provides PORT environment variable
    app.run_server(host='0.0.0.0', port=port)
