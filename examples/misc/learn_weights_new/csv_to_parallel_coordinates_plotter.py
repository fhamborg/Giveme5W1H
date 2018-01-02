import plotly.graph_objs as go
import plotly
import pandas as pd

df = pd.read_csv("result/training_final_result_what.csv")


dimensions = []
for dimension in df.columns.values:

    dimensions.append(
        dict(range=[0, 1], label=dimension, values=df[dimension])
    )

line = dict(color = df['score'],
            colorscale = 'Viridis',
            showscale = True,
            reversescale = True,
            cmin=0,
            cmax=1
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
plotly.offline.plot(fig)
#plotly.offline.plot(fig, filename = 'parcoords-basic.html')
#py.iplot(fig, filename = 'parcoords-basic')