import plotly.graph_objs as go


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
        plot_bgcolor = 'rgba(0, 0, 0, 0)'
    )

    fig.add_trace(go.Scatter(
        x = [0.38], y = [0.75],
        mode='text',
        text = ['IGT:'],
        textposition='top right',
        textfont = {
            'size': 20
        },
        showlegend=False,
        hoverinfo='none',
    )) 

    fig.add_trace(go.Scatter(
        x = [0.6, 1], y = [0.75, 0.75],
        mode='text',
        text = ['00:38:42', '02:13'],
        textposition='top left',
        textfont = {
            'size': 20
        },
        showlegend=False,
        hoverinfo='none',
    )) 

    fig.add_trace(go.Scatter(
        x = [0.8], y = [0.75],
        mode='text',
        text = ['▼00:12'],
        textposition='top left',
        textfont = {
            'size': 20,
            'color': 'green'
        },
        showlegend=False,
        hoverinfo='none',
    )) 

    fig.add_trace(
        go.Indicator(
            mode = 'gauge',
            value = 5250,
            delta = {
                'reference': 5000
            },
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
            domain = {
                'x': [0, 0.3], 'y': [0, 1]
            }
        )
    )


    fig.add_trace(go.Scatter(
        x = [0], y = [0.85],
        mode='text',
        text = ['DA'],
        textposition='bottom right',
        textfont = {
            'size': 20
        },
        showlegend=False,
        hoverinfo='none',
    ))

    fig.add_trace(go.Scatter(
        x = [0.15], y = [0.52],
        mode='text',
        text = ['5250'],
        textposition='bottom center',
        textfont = {
            'size': 15
        },
        showlegend=False,
        hoverinfo='none',
    ))

    fig.add_trace(go.Scatter(
        x = [0.15], y = [0.4],
        mode='text',
        text = ['5'],
        textposition='bottom center',
        textfont = {
            'size': 40
        },
        showlegend=False,
        hoverinfo='none',
    ))


    fig.add_trace(go.Indicator(
        mode = 'gauge',
        title = {
            'text': 'Enemy'
        },
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
        domain = {
            'x': [0.45, 1], 
            'y': [0.25, 0.4]
        }
    ))

    fig.add_trace(go.Scatter(
        x = [0.99], y = [0.32],
        mode='text',
        text = ['1250 / 4500'],
        textposition='middle left',
        textfont = {
            'size': 18
        },
        showlegend=False,
        hoverinfo='none',
    ))


    fig.add_trace(go.Indicator(
        mode = 'gauge',
        title = {
            'text': 'Claire'
        },
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
        domain = {
            'x': [0.45, 1], 
            'y': [0.5, 0.65]
        }
    ))

    fig.add_trace(go.Scatter(
        x = [0.99], y = [0.57],
        mode='text',
        text = ['765 / 1500'],
        textposition='middle left',
        textfont = {
            'size': 18
        },
        showlegend=False,
        hoverinfo='none',
    ))


    

    fig.show()

if __name__ == '__main__':
    main()