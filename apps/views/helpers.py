from io import StringIO

from plotly import express as px

color_picker = lambda ret: "red" if ret < 0 else "green"


def _write_html(fig, div_id=None):
    buffer = StringIO()
    fig.write_html(file=buffer,
                   include_plotlyjs="https://cdn.plot.ly/plotly-latest.min.js",
                   full_html=False,
                   div_id=div_id)
    buffer.seek(0)
    html_str = buffer.read()
    return html_str


def plot_prices(df, title):

    fig = px.line(df)
    fig.update_xaxes(title=None, showgrid=True)
    fig.update_yaxes(ticksuffix=None, showgrid=True, title='Prices')
    fig.update_traces(hovertemplate=None)
    fig.update_layout(template='simple_white',
                      hovermode='x unified', hoverlabel_namelength=-1, autosize=True,
                      legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, title_text=''),
                      title=dict(text=f"<b>{title}</b>", font=dict(family='Helvetica', size=14)))
    return fig


_1MONTH = 21
_1YEAR = 260

LOOKBACK = {
    '1D': 1,
    '5D': 5,
    '1M': _1MONTH,
    '3M': _1MONTH * 3,
    '6M': _1MONTH * 6,
    '1Y': _1YEAR,
    '3Y': _1YEAR * 3,
    '5Y': _1YEAR * 5,
    '10Y': _1YEAR * 10,
}
