import inspect
import os
from functools import wraps
from urllib.parse import urlencode


def endpoint_builder(function_param=None):
    def _endpoint_url(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            url = func(*args, **kwargs)
            kwargs['function'] = function_param
            kwargs['apikey'] = args[0].api_key
            for value, arg in zip(args[1:], inspect.getfullargspec(func).args[1:]):
                kwargs[arg] = value
            return url + urlencode(kwargs)

        return wrapper

    return _endpoint_url


class AlphaVantageUrls:
    DEFAULT_INDICES = ['QQQ', 'SPY', 'IWM']

    def __init__(self, key=None, bucket=None):
        self.api_key = key or os.getenv('STOCK_API_KEY')
        self.bucket = bucket or os.getenv('DATA_BUCKET')
        self._base_api_url = "https://www.alphavantage.co/query?"
        self._bucket_url = "s3://{bucket}/{function}/{symbol}"

    @endpoint_builder(function_param='TIME_SERIES_DAILY')
    def get_daily_stock_series_url(self, symbol, **kwargs):
        return self._base_api_url

    @endpoint_builder(function_param='TIME_SERIES_DAILY_ADJUSTED')
    def get_daily_adjusted_stock_series_url(self, symbol, **kwargs):
        return self._base_api_url

    @endpoint_builder(function_param='SYMBOL_SEARCH')
    def get_search_url(self, keywords):
        return self._base_api_url

    @endpoint_builder(function_param='NEWS_SENTIMENT')
    def get_news_url(self, **kwargs):
        return self._base_api_url

    def get_daily_stock_series_url_s3(self, symbol):
        _FUNCTION = 'TIME_SERIES_DAILY'
        return self._bucket_url.format(bucket=self.bucket, function=_FUNCTION, symbol=symbol)

    def get_market_stock_url_s3(self):
        _FUNCTION = 'TIME_SERIES_DAILY'
        return self.get_daily_stock_series_url_s3(symbol='MARKET_DATA')
