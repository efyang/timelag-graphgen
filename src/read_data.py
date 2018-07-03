import pandas as pd
import numpy as np
import statsmodels.api as sm
lowess = sm.nonparametric.lowess


def process_df(df, prefix, lag_n):
    t = extract_times(df)
    y = df[prefix+"_t0"]

    # with lowess smoothing
    # Z = lowess(y, t, frac=0.5, it=2)
    # return reshape_data(prefix, t, pd.DataFrame(y - Z[:, 1]), lag_n)
    # without lowess smoothing
    return reshape_data(prefix, t, y, lag_n)


def read_file(filename):
    df = pd.read_csv(filename)
    return df


def extract_times(df):
    return df["Time"]


def reshape_data(prefix, time_col, value_col, lag_n):
    nrows = len(time_col)

    base = value_col
    lag_1 = value_col.shift(lag_n)
    lag_2 = value_col.shift(2*lag_n)
    df = pd.concat([base, lag_1, lag_2], axis=1)
    df.columns = [prefix+'_t0', prefix+'_t1', prefix+'_t2']
    return df


def find_max_val(df, prefix):
    return df[prefix+'_t0'].max()
