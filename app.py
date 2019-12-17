##Dash Dependencies
import dash
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

from ccxt_datahandler import ccxt_datahandler
import pandas as pd
import numpy as np
import datetime as dt
import talib

###Dash Styling guide
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(
    __name__,
     meta_tags=[{"name": "viewport", "content": "width=device-width"}],
     external_stylesheets=external_stylesheets
)

server = app.server

app.layout = html.Div(
                ####Main layout of app
                children = [
                            html.Div(
                                #general instructions
                                children=[
                                    html.H1('Market Timing Tracker'),
                                    html.P('Live updating app to track risk associated with entering the market at a given time.')
                                    ],
                                className='wrapper'),
                            html.Div(

                                children = [
                                    html.H4('Short Term Trend Indicator', style={"display": "flex", "flex-direction": "column",'margin-top':'0px'}),
                                    dcc.Graph(id="main-graph"),
                                    dcc.Interval(id='graph-update',interval=4*60*60 * 1000, n_intervals=0)],
                                    className=" pretty_container",
                                    style={'text-align':'center'}),
                            html.Div(

                                children = [
                                    html.H4('Long Term Trend Indicator', style={"display": "flex", "flex-direction": "column",'margin-top':'0px'}),
                                    dcc.Graph(id="main-graph-2"),
                                    dcc.Interval(id='graph-update-2',interval=4*60*60 * 1000, n_intervals=0)],
                                    className=" pretty_container",
                                    style={'text-align':'center'}),
                            html.Div(

                                children = [
                                    html.H4('Logarithmic Price Chart', style={"display": "flex", "flex-direction": "column",'margin-top':'0px'}),
                                    dcc.Graph(id="main-graph-3"),
                                    dcc.Interval(id='graph-update-3',interval=4*60*60 * 1000, n_intervals=0)],
                                    className=" pretty_container",
                                    style={'text-align':'center'}),
                            
                        ],
                className = 'wrapper')
@app.callback(dash.dependencies.Output('main-graph', 'figure'),
    [dash.dependencies.Input('graph-update', 'n_intervals')])
def update(n_intervals):
    data = ccxt_datahandler('ETH/USDT', 'poloniex', '4h')
    data['fast_MA'] = data.Close.rolling(window=10).mean()
    data['slow_MA'] = data.Close.rolling(window=50).mean()
    data['diff'] = data.fast_MA-data.slow_MA
    data['fast_MA'] = talib.SMA(data.Close, timeperiod=50)
    data['slow_MA'] = talib.SMA(data.Close, timeperiod=200)
    data['diff'] = data.fast_MA-data.slow_MA
    data['risk']=((data['diff']/data['diff'].rolling(window=200).std())**1)
    
    data = data.dropna()
    print(data)
    #### use ((fast ma - slow ma/slow ma))/(std (difference/slow mac))
    layout = go.Layout(paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',showlegend=True,xaxis={'title':'Date'},yaxis={'title':'Short Term Oscilator'},yaxis2={'title':'second y','side':'right'})

    trace1 = go.Scatter(x=data.index,
            y=data.risk,
            name='risk',
            )
    trace2 = go.Scatter(x=data.index,
        y=data.risk,
        name='close',
        )
    data = [trace1,trace2]
    return go.Figure(data=data, layout=layout)

@app.callback(dash.dependencies.Output('main-graph-2', 'figure'),
    [dash.dependencies.Input('graph-update-2', 'n_intervals')])
def update(n_intervals):
    data = ccxt_datahandler('ETH/USDT', 'poloniex', '4h')
    data['fast_MA'] = data.Close.rolling(window=10).mean()
    data['slow_MA'] = data.Close.rolling(window=50).mean()
    data['diff'] = data.fast_MA-data.slow_MA
    data['fast_MA'] = talib.SMA(data.Close, timeperiod=300)
    data['slow_MA'] = talib.SMA(data.Close, timeperiod=1200)
    data['diff'] = data.fast_MA-data.slow_MA
    data['risk']=((data['diff']/data['diff'].rolling(window=1200).std())**1)
    
    data = data.dropna()
    print(data)
    #### use ((fast ma - slow ma/slow ma))/(std (difference/slow mac))
    layout = go.Layout(paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',showlegend=True,xaxis={'title':'Date'},yaxis={'title':'Long Term Oscilator'},yaxis2={'title':'second y','side':'right'})

    trace1 = go.Scatter(x=data.index,
            y=data.risk,
            name='risk',
            )
    trace2 = go.Scatter(x=data.index,
        y=data.risk,
        name='close',
        )
    data = [trace1,trace2]
    return go.Figure(data=data, layout=layout)

@app.callback(dash.dependencies.Output('main-graph-3', 'figure'),
    [dash.dependencies.Input('graph-update-3', 'n_intervals')])
def update(n_intervals):
    data = ccxt_datahandler('ETH/USDT', 'poloniex', '4h')    
    data = data.dropna()
    data['log_close'] = np.log(data['Close'])
    layout = go.Layout(paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',showlegend=True,xaxis={'title':'Date'},yaxis={'title':'Logarithmic Price'},yaxis2={'title':'second y','side':'right'})

    trace1 = go.Scatter(x=data.index,
            y=data.log_close,
            name='risk',
            )
    trace2 = go.Scatter(x=data.index,
        y=data.log_close,
        name='close',
        )
    data = [trace1,trace2]
    return go.Figure(data=data, layout=layout)
if __name__ == "__main__":

    app.run_server(debug=True)

