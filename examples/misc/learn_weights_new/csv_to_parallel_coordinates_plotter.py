import plotly.graph_objs as go
import plotly
import pandas as pd



def generate_plot(path, auto_open = True):
    df = pd.read_csv('result/'+path+'.csv')

    min_max = df['score'].agg(['min', 'max'])

    dimensions = []
    for dimension in df.columns.values:

        if dimension != 'score':
            dimensions.append(
                dict(range=[0, 1], label=dimension, values=df[dimension])
            )
        else:
            dimensions.append(
                dict(range=[0, min_max.max()], label=dimension, values=df[dimension])
            )
    line = dict(color = df['score'],
                colorscale = 'Viridis',
                showscale = True,
                reversescale = False,
                cmin=0,
                cmax=min_max.max()
                )

    data = [
        go.Parcoords(
            line = line,
            dimensions = dimensions
        )
    ]

    layout = go.Layout(
        plot_bgcolor = '#E5E5E5',
        paper_bgcolor = '#E5E5E5'
    )

    fig = go.Figure(data = data, layout = layout)
    plotly.offline.plot(fig, filename='result/'+path+'.html', auto_open=auto_open)
    #plotly.offline.plot(fig, filename = 'parcoords-basic.html')
    #py.iplot(fig, filename = 'parcoords-basic')


if __name__ == '__main__':
    generate_plot("training_final_result_where_1_avg")