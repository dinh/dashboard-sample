import pandas as pd

from apps.services import stats, window
from .helpers import plot_prices, _write_html, color_picker
from .mixin import _ViewMixin


class MarketView(_ViewMixin):

    def __init__(self):
        super().__init__()

    @property
    def av(self):
        return self.data_service.av

    def get_market_data(self, column='close'):
        df = self.data_service.get_market_stock_series()
        df = pd.concat([df.loc[df.symbol == symbol, [column]] for symbol in self.data_service.urls.DEFAULT_INDICES],
                       axis=1)
        df.columns = self.data_service.urls.DEFAULT_INDICES
        df = df.dropna()
        start_date = window.get_start_date(df.index.max(), self.window)
        df = df.loc[df.index >= start_date, :]
        return df

    @staticmethod
    def _prepare_for_plot(df):
        df.columns = [
            f"<b>{col}</b><br><sup style='color:{color_picker(df[col].iloc[-1])}'>{df[col].iloc[-1]:.2%}</sup>"
            for col in df.columns.to_list()]
        return df

    def build_market_chart(self):
        df = self.get_market_data()
        df = stats.calc_cum_returns(df)
        df = self._prepare_for_plot(df)
        fig = plot_prices(df, "Today's Market").update_layout(yaxis_tickformat='%')
        return fig

    def get_daily_market_chart_html(self, div_id='market-chart'):
        fig = self.build_market_chart()
        return _write_html(fig, div_id=div_id)

    def build_drawdown_chart(self):
        df = self.get_market_data()
        df = stats.calc_cum_returns(df)
        df = stats.calc_drawdown(df)
        df = self._prepare_for_plot(df)
        fig = plot_prices(df, "Drawdown").update_layout(yaxis_tickformat='%')
        return fig

    def get_drawdown_chart_html(self, div_id='market-drawdown'):
        fig = self.build_drawdown_chart()
        return _write_html(fig, div_id=div_id)
