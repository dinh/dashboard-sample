import os


class StockURLs:
    DEFAULT_INDICES = ['QQQ', 'SPY', 'IWM']

    def __init__(self, key=None, bucket=None):
        self.api_key = key if key else os.getenv('STOCK_API_KEY')
        self.bucket = bucket if bucket else os.getenv('DATA_BUCKET')
        self._api_url = "https://www.alphavantage.co/query?function={function}&" \
                        "symbol={symbol}&apikey={key}&outputsize={output}"
        self._bucket_url = "s3://{bucket}/{function}/{symbol}"

    def get_market_stock_url_s3(self):
        _FUNCTION = 'TIME_SERIES_DAILY'
        return self._bucket_url.format(bucket=self.bucket, function=_FUNCTION, symbol='MARKET_DATA')

    def get_daily_stock_series_url(self, symbol, output='compact'):
        _FUNCTION = 'TIME_SERIES_DAILY'
        return self._api_url.format(function=_FUNCTION, symbol=symbol, key=self.api_key, output=output)

    def get_daily_stock_series_url_s3(self, symbol):
        _FUNCTION = 'TIME_SERIES_DAILY'
        return self._bucket_url.format(bucket=self.bucket, function=_FUNCTION, symbol=symbol)

    def get_daily_adjusted_stock_series_url(self, symbol, output='compact'):
        _FUNCTION = 'TIME_SERIES_DAILY_ADJUSTED'
        return self._api_url.format(function=_FUNCTION, symbol=symbol, key=self.api_key, output=output)

    def get_search_url(self, search_string):
        _FUNCTION = 'SYMBOL_SEARCH'
        return 'https://www.alphavantage.co/query?function={function}&keywords={keyword}&apikey={api_key}'.format(
            function=_FUNCTION, keyword=search_string, api_key=self.api_key)
