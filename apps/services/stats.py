import numpy as np


def calc_drawdown(df):
    df = df + 1
    dd = np.maximum.accumulate(df)
    return -1 * ((dd / df) - 1)


def calc_cum_returns(df):
    df = (1 + df.pct_change()).cumprod() - 1
    return df.fillna(0)
