import plotly
import plotly.plotly as py
import plotly.graph_objs as go
# from plotly.offline import download_plotlyjs

import pandas_datareader as web
from datetime import datetime

df = web.DataReader("aapl", 'morningstar').reset_index()

trace = go.Candlestick(x=df.Date,
                       open=df.Open,
                       high=df.High,
                       low=df.Low,
                       close=df.Close)
data = [trace]
# plotly.offline.iplot(data, filename='simple_candlestick')

plotly.offline.plot(
    {
        "data": data,
        "layout": go.Layout(
            title="Hello World",
            yaxis=dict(
                range=[-80000, 1000]
            ))
    },
    auto_open=True)
