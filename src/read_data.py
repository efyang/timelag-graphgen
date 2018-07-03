import pandas as pd
import numpy as np


def process_df(df, prefix, lag_n):
    return reshape_data(prefix, extract_times(df), df[prefix+"_t0"], lag_n)


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
