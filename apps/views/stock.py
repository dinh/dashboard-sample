from apps.views.helpers import _write_html, plot_prices, color_picker
from ._mixin import _ViewMixin


class StockView(_ViewMixin):
    def __init__(self):
        super().__init__()

    @staticmethod
    def _prepare_for_plot(df):
        val = ((df.iloc[-1] / df.iloc[0]) - 1).squeeze()
        df.columns = [
            f"<b>{col}</b><br><sup style='color:{color_picker(val)}'>{val:.2%}</sup>"
            for col in df.columns.to_list()]
        return df

    @property
    def symbol(self):
        _SYMBOL = 'symbol'
        if self.request.method == 'GET':
            return self.request.args.get(_SYMBOL)
        else:
            return self.request.form.get(_SYMBOL)

    def build_daily_stock_chart(self):
        df = self.data_service.get_daily_stock_series(self.symbol)
        if self.window:
            start_date = self.get_start_date(df.index.max())
            df = df.loc[df.index >= start_date, :]
        df = df.loc[:, ['close']]
        df = self._prepare_for_plot(df)
        fig = plot_prices(df, f'{self.symbol} Price')
        return fig

    def get_daily_stock_chart_html(self):
        fig = self.build_daily_stock_chart()
        return _write_html(fig, div_id='daily-chart')
