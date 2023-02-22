import datetime

import dash
from dash import dcc, html
import json
import plotly.graph_objects as go
from dash.dependencies import Input, Output

import zmq

#  Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:5556")
socket.setsockopt_string(zmq.SUBSCRIBE, "")


app = dash.Dash('PySRT Dashbaord')
app.layout = html.Div(
    html.Div([
        html.H4('PySRT Dashboard'),
        dcc.Interval(id='interval', interval=1000),
        html.Div(id='live-update-text'),
        dcc.Graph(id='live-update-graph'),
    ])
)


@app.callback(
    Output('live-update-text', 'children'),
    [Input('interval', 'n_intervals')]
)
def update_data(n):
    return [get_data()]

def calc_igt(igt_struct):
    return igt_struct['IGT_Running_Timer'] - igt_struct['IGT_Cutscene_Timer'] - igt_struct['IGT_Pause_Timer']

def get_data():
    return socket.recv_string()


@app.callback(
    Output('live-update-graph', 'figure'),
    [Input('live-update-text', 'children')]
)
def update_graph_live(data):
    data = json.loads(data[0])

    igt = calc_igt(data['IGT'])
    hp, hp_max = data['Player_HP']['Current_HP'], data['Player_HP']['Max_HP']
    da_rank, da_score = data['DA']['DA_Rank'], data['DA']['DA_Score']

    # Create a trace for the grey rectangle
    trace1 = go.Scatter(
        x=[0, hp_max, hp_max, 0],
        y=[0, 0, 10, 10],
        fill='toself',
        fillcolor='lightgray',
        line={'color': 'lightgray'}, 
        hoverinfo='none'
    )

    # Create a trace for the red rectangle
    trace2 = go.Scatter(
        x=[0, hp, hp, 0],
        y=[0, 0, 10, 10],
        fill='toself',
        fillcolor='red',
        line={'color': 'red'},
        hoverinfo='none'
    )


    # Create the layout for the graph
    layout = go.Layout(
        title='ZMQ Data',
        xaxis={'title': 'X-axis'},
        yaxis={'title': 'Y-axis'},
        shapes=[
            # Add the grey rectangle shape
            {'type': 'rect', 'xref': 'x', 'yref': 'y', 'x0': 0, 'y0': 0, 'x1': hp_max, 'y1': 10,
             'fillcolor': 'lightgray', 'line': {'color': 'lightgray'}},
            # Add the red rectangle shape
            {'type': 'rect', 'xref': 'x', 'yref': 'y', 'x0': 0, 'y0': 0, 'x1': hp, 'y1': 10,
             'fillcolor': 'red', 'line': {'color': 'red'}}
        ]
    )

    # Create the figure and add the traces and layout
    fig = {'data': [trace1, trace2], 'layout': layout}
    return fig



if __name__ == '__main__':
    app.run_server(debug=True)