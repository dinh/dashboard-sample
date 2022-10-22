import datetime
from functools import partial

import pandas as pd


def lookback_n_days(end_dt, n):
    return end_dt - pd.DateOffset(days=n)


def lookback_n_months(end_dt, n):
    return end_dt - pd.DateOffset(months=n)


lookback_1_day = partial(lookback_n_days, n=1)
lookback_5_day = partial(lookback_n_days, n=5)
lookback_1_month = partial(lookback_n_months, n=1)
lookback_3_month = partial(lookback_n_months, n=3)
lookback_6_month = partial(lookback_n_months, n=6)
lookback_1_year = partial(lookback_n_months, n=12)
lookback_3_year = partial(lookback_n_months, n=12 * 3)
lookback_5_year = partial(lookback_n_months, n=12 * 5)
lookback_10_year = partial(lookback_n_months, n=12 * 10)


def get_start_date(date, window='10Y'):
    if window == '1D':
        return lookback_1_day(date)
    if window == '5D':
        return lookback_5_day(date)
    if window == '1M':
        return lookback_1_month(date)
    if window == '3M':
        return lookback_3_month(date)
    if window == '6M':
        return lookback_6_month(date)
    if window == 'YTD':
        return pd.to_datetime(datetime.datetime(date.year, 1, 1))
    if window == '1Y':
        return lookback_1_year(date)
    if window == '3Y':
        return lookback_3_year(date)
    if window == '5Y':
        return lookback_5_year(date)
    if window == '10Y':
        return lookback_10_year(date)
    else:
        raise Exception('Not a valid window')
