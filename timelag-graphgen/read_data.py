import pandas as pd
import statsmodels.api as sm
lowess = sm.nonparametric.lowess
import time_offset


# return 3xn datadrame, each column is lagged according to prefix
def process_df(df, prefix, lag_n):
    t = extract_times(df)
    y = df[prefix+"_t0"]
    # with lowess smoothing
    # Z = lowess(y, t)
    # return reshape_data(prefix, t, pd.DataFrame(y - Z[:, 1]), df['Start of interval'], lag_n)
    # without lowess smoothing
    return reshape_data(prefix, t, y, df['Start of interval'], lag_n)


# read the original csv file
def read_file(filename):
    df = pd.read_csv(filename)
    return df


# get the time column from the original dataframe
def extract_times(df):
    return df['Time']


# return 3xn datadrame, each column is lagged according to prefix
def reshape_data(prefix, time_col, value_col, date_col, lag_n):
    base = value_col
    lag_1 = value_col.shift(lag_n)
    lag_2 = value_col.shift(2*lag_n)
    # we put everything back together into a nx3 matrix
    df = pd.concat([date_col, base, lag_1, lag_2], axis=1)
    # use the original naming scheme
    df.columns = ["date", prefix+'_t0', prefix+'_t1', prefix+'_t2']
    return df


# find the maximum value in the dataframe, used to determine graph scaling and limits later on
def find_max_val(df, prefix):
    return df[prefix+'_t0'].max()


def find_min_val(df, prefix):
    dmin = df[prefix+'_t0'].min()
    if dmin < 0:
        return dmin
    else:
        return 0
