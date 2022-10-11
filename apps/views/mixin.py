import datetime

import flask
import numpy as np
import pandas as pd

from apps.alpha_vantage.api import AlphaVantage
from apps.services.data_service import DataSvc
from .helpers import LOOKBACK


class _ViewMixin:
    def __init__(self):
        self.request = flask.request
        self.is_htmx_request = 'HX-Request' in flask.request.headers
        self.av = AlphaVantage()
        self.data_service = DataSvc()

    @property
    def segment(self):
        try:

            segment = self.request.path.split('/')[-1]

            if segment == '':
                segment = 'index'

            return segment

        except:
            return None

    @property
    def window(self):
        return self.request.form.get('window')

    @property
    def lookback(self):
        return LOOKBACK.get(self.window)

    def get_start_date(self, date):
        if self.window == 'YTD':
            return pd.to_datetime(datetime.datetime(date.year, 1, 1))
        else:
            start_date = np.busday_offset(np.busday_offset(date.date(), -1), -self.lookback)
            return start_date
