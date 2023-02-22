import plotly.graph_objs as go


def x_offset(x, offset=7):
    return x + offset

def draw_bar(x, y, width, height, fillcolor, line_color):
    return dict(
        type = 'rect',
        xref = 'x',
        yref = 'y',
        x0 = x_offset(x), x1=x_offset(x + width),
        y0 = y, y1 = y + height,
        fillcolor = fillcolor,
        line = dict(
            color = line_color
        )
    )


def draw_bar_gauge(x, y, val, max):
    return [
        draw_bar(x, y, max, 10, 'white', 'white'),
        draw_bar(x, y, val, 10, 'red', 'red')
    ]


def draw_text(x, y, text, color='white'):
    return dict(
        type = 'scatter',
        xref = 'x',
        yref = 'y',
        x = [x],
        y = [y],
        text = [text],
        mode = 'text',
        textposition = 'top right',
        textfont = dict(
            family = 'Arial',
            size = 18,
            color = color
            
    )


def main():
    fig = go.Figure()

    layout = go.Layout(
        width = 800,
        height = 280,
        xaxis = dict(
            range = [0, 120],
            visible = False
        ),
        yaxis = dict(
            range = [0, 50],
            visible = False
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        shapes = [
            *draw_bar_gauge(0, 0, 75, 100),
            *draw_bar_gauge(0, 20, 50, 100),
        ]
    )

    fig.update_layout(layout)

    fig.add_trace(
        go.Scatter(
            x = [0, 0],
            y = [20, 0],
            text=['DA', 'HP'],
            mode='text',
            textposition='top right',
            textfont=dict(
                family='arial',
                size=18,
                color='white'
            )
        )
    )

    fig.show()


if __name__ == '__main__':
    main()