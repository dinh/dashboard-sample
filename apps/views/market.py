import pandas as pd

from apps.services.data_service import DataSvc
from ._mixin import _ViewMixin
from .helpers import plot_prices, _write_html, color_picker


class MarketView(_ViewMixin):

    def __init__(self):
        super().__init__()
        self.data_service = DataSvc()

    def get_market_data(self):
        df = self.data_service.get_market_stock_series()
        df = pd.concat([df.loc[df.symbol == symbol, ['close']] for symbol in self.data_service.urls.DEFAULT_INDICES],
                       axis=1)
        df.columns = self.data_service.urls.DEFAULT_INDICES
        return df.dropna()

    @staticmethod
    def _prepare_for_plot(df):
        df.columns = [
            f"<b>{col}</b><br><sup style='color:{color_picker(df[col].iloc[-1])}'>{df[col].iloc[-1]:.2%}</sup>"
            for col in df.columns.to_list()]
        return df

    def build_market_chart(self):
        df = self.get_market_data()
        if self.window:
            start_date = self.get_start_date(df.index.max())
            df = df.loc[df.index >= start_date, :]
        df = (1 + df.pct_change()).cumprod() - 1
        df = df.fillna(0)
        df = self._prepare_for_plot(df)
        fig = plot_prices(df, "Today's Market")
        return fig

    def get_daily_market_chart_html(self, div_id='market-chart'):
        fig = self.build_market_chart()
        return _write_html(fig, div_id=div_id)
