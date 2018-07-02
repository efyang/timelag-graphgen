import pandas as pd
import numpy as np


def process_file(filename):
    df = read_file(filename)
    return reshape_data(extract_times(df), extract_entries(df), 1)


def read_file(filename):
    df = pd.read_csv(filename)
    return df


def extract_entries(df):
    return df["Entries_CC_t0"]


def extract_exits(df):
    return df["Exits_CC_t0"]


def extract_times(df):
    return df["Time"]


def reshape_data(time_col, value_col, lag_n):
    nrows = len(time_col)

    base = value_col[:-2 * lag_n]
    lag_1 = value_col[lag_n: -1 * lag_n]
    lag_2 = value_col[2 * lag_n:]
    return pd.concat([base, lag_1, lag_2], axis=1)
