import plotly.graph_objs as go
from plotly.io._kaleido import to_image

from time import time


def text(msg, x, y, textposition='top right', size=20, color='black'):
    _text = go.Scatter(
        x=[x], y=[y],
        mode='text',
        text=[msg],
        textposition=textposition,
        textfont=dict(
            size=size,
            color=color
        ),
        showlegend=False,
        hoverinfo='none'
    )
    return _text


def main():
    fig = go.Figure()

    fig.update_layout(
        width=800,
        height=350,
        xaxis = {
            'range' : [0, 1],    
            'visible': False},
        yaxis = {
            'range' : [0, 1],  
            'visible': False
        },
        plot_bgcolor = 'white'
    )

    fig.add_trace(
        go.Indicator(
            mode = 'gauge',
            value = 5250,
            gauge = {
                'axis': {
                    'visible': False,
                    'range': [4000, 7000]
                }
            },
            gauge_bar = {
                'color': 'blue',
                'thickness': 0.5,
            },
            gauge_steps = [
                {'range': [4000, 5000], 'color': 'green'},
                {'range': [5000, 6000], 'color': 'orange'},
                {'range': [6000, 7000], 'color': 'red'},
            ],
            domain = {'x': [0, 0.3], 'y': [0, 1]}
        )
    )

    fig.add_trace(go.Indicator(
        mode = 'gauge',
        title = {'text': 'Enemy'},
        gauge = {
            'shape': "bullet",
            'axis': {
                'range': [None, 4500],
                'visible': False
            },
            'bgcolor': 'rgba(0, 0, 0, 0)',
            'borderwidth': 1,
        },
        gauge_bar = {
            'color': 'red',
            'thickness': 1,
        },
        value = 1250,
        domain = {'x': [0.45, 1], 'y': [0.25, 0.4]}
    ))

    fig.add_trace(go.Indicator(
        mode = 'gauge',
        title = {'text': 'Claire'},
        gauge = {
            'shape': "bullet",
            'axis': {
                'range': [None, 1500],
                'visible': False
            },
            'bgcolor': 'rgba(0, 0, 0, 0)',
            'borderwidth': 1,
        },
        gauge_bar = {
            'color': 'orange',
            'thickness': 1,
        },
        value = 765,
        domain = { 'x': [0.45, 1], 'y': [0.5, 0.65]}
    ))

    fig.add_trace(text('IGT:', 0.38, 0.75, textposition='top right', size=20))
    fig.add_trace(text('00:38:42', 0.6, 0.75, textposition='top left', size=20))
    fig.add_trace(text('02:13', 1, 0.75, textposition='top left', size=20))
    fig.add_trace(text('▼00:12', 0.8, 0.75, textposition='top left', size=20, color='green'))
    fig.add_trace(text('DA', 0, 0.85, textposition='bottom right', size=20))
    fig.add_trace(text('5250', 0.15, 0.52, textposition='bottom center', size=15))
    fig.add_trace(text('5', 0.15, 0.4, textposition='bottom center', size=40))
    fig.add_trace(text('1250 / 4500', 0.99, 0.32, textposition='middle left', size=18))
    fig.add_trace(text('765 / 1500', 0.99, 0.57, textposition='middle left', size=18))

    fig.write_image('./overlay.png', width=800, height=350, scale=1, engine='kaleido', validate=False)
    # print(f'Build time: {time() - t_build}s')
    # t_render = time()
    # img_bytes = to_image(fig, format='png', width=800, height=350, scale=1, engine='kaleido', validate=False)
    # print(f'Render time: {time() - t_render}s')
    # return img_bytes, 800, 350


if __name__ == '__main__':
    main()