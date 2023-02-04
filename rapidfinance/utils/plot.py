import plotly.express as px
import plotly.graph_objects as go


def plot_line(df, columns, **kwargs):
    assert isinstance(columns, list)
    fig = px.line(df[columns], **kwargs)
    fig.show()


def plot_candlestick(df, **kwargs):
    fig = go.Figure(data=[go.Candlestick(x=df.index,
                                         open=df['open'],
                                         high=df['high'],
                                         low=df['low'],
                                         close=df['adjclose'])])
    fig.show()
