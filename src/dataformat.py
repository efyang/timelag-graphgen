import pandas as pd
import numpy as np
import statsmodels.api as sm
lowess = sm.nonparametric.lowess
idx = pd.IndexSlice


class DataFormat:
    def __init__(self, df, lagged=False):
        self.df = df
        self.lagged = lagged

    # TODO: fix currently wrong (wraps onto)
    def create_lag_cols(self, lag_units, multistate=False):
        if not self.lagged:
            if multistate:
                groups = ['state', 'caretype']
            else:
                groups = ['state']
            grouping = self.df.groupby(groups)
            lag_0 = self.df
            lag_1 = grouping.shift(lag_units)
            lag_2 = grouping.shift(2 * lag_units)

            self.df = pd.concat([lag_0, lag_1, lag_2], axis=1)
            self.df.columns = [
                'entries_t0', 'exits_t0', 'entries_t1', 'exits_t1',
                'entries_t2', 'exits_t2'
            ]
            self.lagged = True


class WeekSSData(DataFormat):
    def __init__(self, df, state_id, lagged=False):
        self.state_id = state_id
        super().__init__(df, lagged=lagged)

    def create_lag_cols(self, lag_units):
        super().create_lag_cols(lag_units, multistate=False)

    # TODO: if already lagged, the entire lagged column will be NaN again:
    # need to delete and regen
    def apply_lowess_all_cols(self):
        for caretype in self.df.index.levels[0]:
            for c in self.df.columns:
                t = np.arange(len(self.df.loc[caretype, c]))
                y = self.df.loc[idx[caretype, :], c]
                # "missing" is so that NaN values aren't dropped
                z = lowess(y, t, frac=0.5, it=2, missing="none")
                rep = pd.Series(y - z[:, 1])
                self.df.loc[idx[caretype, :], c] = rep


# class DaySSData(DataFormat):
# def __init__(self, df, state_id):
# self.state_id = state_id
# super().__init__(df)


class WeekMSData(DataFormat):
    def __init__(self, df, lagged=False):
        super().__init__(df, lagged=False)

    def create_lag_cols(self, lag_units):
        super().create_lag_cols(lag_units, multistate=True)

    def to_national_aggregate(self):
        # min_count to 1 makes empty return NaN instead of 0
        return WeekSSData(
            self.df.reset_index(level="state", drop=True).groupby(
                ['caretype', 'date']).sum(min_count=1),
            "NAT",
            lagged=self.lagged)

    # returns list of WeekSSData
    def split_to_ss(self):
        return []

    def get_ss(self, state_id):
        return WeekSSData(
            self.df.loc[idx[state_id, :], :].reset_index(
                level="state", drop=True),
            state_id,
            lagged=self.lagged)

    # TODO: create aggregate total columns


# class DayMSData(DataFormat):
# def __init__(self, df):
# super().__init__(df)
