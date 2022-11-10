import plotly.express as px

def plot_line(df, columns, **kwargs):
    assert isinstance(columns, list)
    fig = px.line(df[columns], **kwargs)
    fig.show()
