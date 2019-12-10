##Dash Dependencies
import dash
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html

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
                                ###game controls
                                children =[
                                    html.Button('Reset'),
                                    html.Button('New Word'),
                                    html.Button('Hint')
                                    ],
                                className = 'wrapper'),
                            html.Div(
                                ###main graph
                                children = [
                                    html.H4('Risk levels'),
                                    dcc.Graph(id="main-graph")],
                                className="pretty_container")
                            ],
                className = 'wrapper')

if __name__ == "__main__":
    app.run_server(debug=True)
