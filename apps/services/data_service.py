import logging

import awswrangler as wr
import pandas as pd

from apps.alpha_vantage.api import AlphaVantage

logger = logging.getLogger(__name__)


class DataSvc:
    def __init__(self):
        self.s3 = wr.s3
        self.av = AlphaVantage()

    @property
    def urls(self):
        return self.av.urls

    def get_last_modified(self, path):
        return self.s3.describe_objects(path).get(path).get('LastModified').date()

    def get_daily_stock_data_from_api(self, path, symbol):
        logger.info(f"loading from api: {symbol}")
        df, meta = self.av.get_daily_stock_series_adjusted(symbol, outputsize='full')
        df['symbol'] = symbol
        self.s3.to_parquet(df, path, index=True)
        return df, meta

    def get_daily_stock_series(self, symbol):
        s3_key = self.urls.get_daily_stock_series_url_s3(symbol)
        if self.s3.does_object_exist(s3_key):
            # Timezone really should be a system setting, but leaving here
            today = pd.Timestamp.utcnow().date()
            last_modified = self.get_last_modified(s3_key)
            if today == last_modified:
                logger.info(f"loading from s3: {s3_key}")
                df = self.s3.read_parquet(s3_key)
                return df
            else:
                return self.get_daily_stock_data_from_api(s3_key, symbol)[0]
        else:
            return self.get_daily_stock_data_from_api(s3_key, symbol)[0]

    def get_market_data_from_api(self):
        logger.info(f"loading from api: Market Data")
        s3_key = self.urls.get_market_stock_url_s3()
        dfs = []
        for symbol in self.urls.DEFAULT_INDICES:
            df, meta = self.av.get_daily_stock_series_adjusted(symbol, outputsize='full')
            df['symbol'] = symbol
            dfs.append(df)
        df = pd.concat(dfs)
        df.index.name = 'asof'
        self.s3.to_parquet(df, s3_key, index=True)
        return df

    def get_market_stock_series(self, columns=None):
        if columns is None:
            columns = ['asof', 'symbol', 'close']
        s3_key = self.urls.get_market_stock_url_s3()
        if self.s3.does_object_exist(s3_key):
            today = pd.Timestamp.utcnow().date()
            last_modified = self.get_last_modified(s3_key)
            if today == last_modified:
                logger.info(f"loading from s3: {s3_key}")
                df = self.s3.read_parquet(s3_key, columns=columns)
                return df
            else:
                df = self.get_market_data_from_api()
                return df.loc[:, columns[1:]]
        else:
            df = self.get_market_data_from_api()
            return df.loc[:, columns[1:]]
