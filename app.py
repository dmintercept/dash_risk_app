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

###Dash Styling guide 
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(
    __name__,
     meta_tags=[{"name": "viewport", "content": "width=device-width"}],
     external_stylesheets=external_stylesheets
)
def SetColor(x):
    if x < 0:
        return 'red'
    elif x==0:
        return 'blue'
    else:
        return 'green'
def oscillator(data,short,long,log):
    if log:
        data['fast_MA'] = np.log(data['Close']).rolling(window=short).mean()
        data['fast_MA'] = np.log(data['Close']).rolling(window=long).mean()
    else:
        data['fast_MA'] = data['Close'].rolling(window=short).mean()
        data['slow_MA'] = data['Close'].rolling(window=long).mean()
    data['diff'] = data.fast_MA-data.slow_MA
    data['risk']=((data['diff']-data['diff'].rolling(window=long).mean())/data['diff'].rolling(window=long).std()**1)
    data['risk_diff']=data['risk'].rolling(window=2).apply(lambda x: x[1] - x[0],raw=False)
    return data
def plot(data,pair,term):
    layout = go.Layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    showlegend=True,
    xaxis={'title':'Date'},
    yaxis={'title':pair+' '+term+' Term Oscilator'})
    trace1 = go.Scatter(
                x=data.index,
                y=data.risk,
                mode='markers+lines',
                name='z-score',
                marker=dict(size=4, color = list(map(SetColor, data['risk_diff']))),
                line=dict(color='rgb(200,200,200)')
            )
    data = [trace1]
    return go.Figure(data=data, layout=layout)
def close_plot(data,log,pair):
    layout = go.Layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=True,
        xaxis={'title':'Date'},
        yaxis={'title':pair+' Close'})
    trace1 = go.Scatter(
                x=data.index,
                y=data.Close,
                mode='lines',
                name='Close',
                line=dict(color='blue')
            )
    data = [trace1]
    return go.Figure(data=data, layout=layout)

###parameters
pair = 'BTC/USDT'
exchange = 'poloniex'
time = '4h'
short_short = 20
short_long = 70
long_short = 100
long_long = 700

#initial load of data
data = ccxt_datahandler(pair,exchange,time).resample('720min').last()

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
                                    # html.H4('Long Term Trend', style={"display": "flex", "flex-direction": "column",'margin-top':'0px'}),
                                    dcc.Graph(id="main-graph"),
                                    dcc.Interval(id='graph-update',interval=15*60*1000, n_intervals=0)],
                                    className=" pretty_container",
                                    style={'text-align':'center'}),
                            html.Div(
                                children = [
                                    # html.H4('Short Term Trend', style={"display": "flex", "flex-direction": "column",'margin-top':'0px'}),
                                    dcc.Graph(id="main-graph-2"),
                                    dcc.Interval(id='graph-update-2',interval=15*60 * 1000, n_intervals=0)],
                                    className=" pretty_container",
                                    style={'text-align':'center'}),
                            html.Div(
                                children = [
                                    # html.H4(pair+' Price Chart', style={"display": "flex", "flex-direction": "column",'margin-top':'0px'}),
                                    dcc.Graph(id="main-graph-3"),
                                    dcc.Interval(id='graph-update-3',interval=15*60 * 1000, n_intervals=0)],
                                    className=" pretty_container",
                                    style={'text-align':'center'}),
                            
                        ],
                className = 'wrapper')
@app.callback(dash.dependencies.Output('main-graph', 'figure'),
    [dash.dependencies.Input('graph-update', 'n_intervals')])
def update(n_intervals):
    data = ccxt_datahandler(pair, exchange, time).resample('720min').last()
    return plot(oscillator(data, long_short, long_long, False),pair,'long')

@app.callback(dash.dependencies.Output('main-graph-2', 'figure'),
    [dash.dependencies.Input('graph-update-2', 'n_intervals')])
def update(n_intervals):
    #long term indicator
    return plot(oscillator(data, short_short, short_long, False), pair,'short')

@app.callback(dash.dependencies.Output('main-graph-3', 'figure'),
    [dash.dependencies.Input('graph-update-3', 'n_intervals')])
def update(n_intervals):
    #close
    return close_plot(data, False, pair)

###use log values with rolling means as it could be a better representation with the mean removing the slightly linear increase
if __name__ == "__main__":
    app.run_server(debug=True,port=8005)

