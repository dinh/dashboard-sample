from io import StringIO

from plotly import express as px

color_picker = lambda ret: "red" if ret < 0 else "green"


def _write_html(fig, div_id=None):
    config = {"responsive": True, "scrollZoom": False,
              "displaylogo": False,
              "modeBarButtonsToRemove": ['pan2d', 'lasso2d', 'zoomIn2d', 'zoomOut2d',
                                         'sendDataToCloud', 'select2d', 'lasso2d',
                                         'drawclosedpath',
                                         'zoom2d', 'autoScale2d',
                                         'toggleSpikelines', 'hoverCompareCartesian',
                                         'hoverClosestCartesian']
              }
    buffer = StringIO()
    fig.write_html(file=buffer,
                   include_plotlyjs="https://cdn.plot.ly/plotly-latest.min.js",
                   full_html=False,
                   div_id=div_id,
                   config=config)
    buffer.seek(0)
    return buffer.read()


def plot_prices(df, title):
    fig = px.line(df)
    fig.update_xaxes(title=None, showgrid=True)
    fig.update_yaxes(title=None, ticksuffix=None, showgrid=True)
    fig.update_traces(hovertemplate=None)
    fig.update_layout(template='simple_white',
                      hovermode='x unified', hoverlabel_namelength=-1, autosize=True,
                      legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, title_text=''),
                      title=dict(text=f"<b>{title}</b>", font=dict(family='Helvetica', size=14)))
    return fig
