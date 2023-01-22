import logging
import os
import re

import pandas as pd
import requests

from .urls import AlphaVantageUrls

logger = logging.getLogger(__name__)


class AlphaVantage:

    def __init__(self, key=None, bucket=None):
        self.api_key = key or os.getenv('STOCK_API_KEY')
        self.urls = AlphaVantageUrls(key=key, bucket=bucket)

    @staticmethod
    def rename_cols(df):
        return [re.sub(r'\d+.', '', name).strip(' ') for name in list(df)]

    @staticmethod
    def format_time_pulished_field(df):
        df['time_published'] = pd.to_datetime(df['time_published'])
        df['time_published'] = df['time_published'].dt.strftime("%m/%d/%Y, %H:%M:%S")
        return df

    @staticmethod
    def _get_response(url):
        response = requests.get(url)
        data = response.json()
        if 'Error Message' in data.keys():
            logger.info(data)
        ts_data = data.get(list(data.keys())[1])
        ts_data = {pd.to_datetime(k): {k: float(v)
                                       for k, v in ts_data[k].items()} for k, v in ts_data.items()}
        ts_data = pd.DataFrame.from_dict(ts_data, orient='columns').T
        ts_data.columns = AlphaVantage.rename_cols(ts_data)
        ts_data = ts_data.sort_index()

        meta_data = data.get(list(data.keys())[0])
        return ts_data, meta_data

    def get_daily_stock_series(self, symbol, outputsize="full"):
        url = self.urls.get_daily_stock_series_url(symbol=symbol, outputsize=outputsize)
        return AlphaVantage._get_response(url)

    def get_daily_stock_series_adjusted(self, symbol, outputsize="full"):
        url = self.urls.get_daily_adjusted_stock_series_url(symbol=symbol, outputsize=outputsize)
        return AlphaVantage._get_response(url)

    def get_news_feed(self, **kwargs):
        url = self.urls.get_news_url(**kwargs)
        response = requests.get(url)
        data = response.json()
        df = pd.DataFrame(data["feed"])
        df = AlphaVantage.format_time_pulished_field(df)
        return df
