import datetime

import numpy as np
import pandas as pd

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


def get_start_date(date, window='10Y'):
    if window == 'YTD':
        return pd.to_datetime(datetime.datetime(date.year, 1, 1))
    else:
        start_date = np.busday_offset(np.busday_offset(date.date(), -1), -LOOKBACK.get(window))
        return start_date
