import pandas as pd
import numpy as np
import statsmodels.api as sm
lowess = sm.nonparametric.lowess
idx = pd.IndexSlice


class DataFormat:
    def __init__(self, df, lagged=False):
        self.df = df
        self.lagged = lagged
        self.lag_units = None

    def create_lag_cols(self, lag_units, multistate=False):
        if not self.lagged:
            if multistate:
                base_groups = ['state', 'caretype']
            else:
                base_groups = ['caretype']
            grouping = self.df.groupby(base_groups)
            lag_0 = self.df
            lag_1 = grouping.shift(lag_units)
            lag_2 = grouping.shift(2 * lag_units)

            self.df = pd.concat([lag_0, lag_1, lag_2], axis=1)
            self.df.columns = [
                'entries_t0', 'exits_t0', 'entries_t1', 'exits_t1',
                'entries_t2', 'exits_t2'
            ]
            self.lagged = True
            self.lag_units = lag_units


class WeekSSData(DataFormat):
    def __init__(self, df, state_id, lagged=False):
        self.state_id = state_id
        super().__init__(df, lagged=lagged)

    def create_lag_cols(self, lag_units):
        super().create_lag_cols(lag_units, multistate=False)

    # TODO: if already lagged, the entire lagged column will be NaN again:
    # need to delete and regen
    def apply_lowess_all_cols(self):
        was_lagged = False
        if self.lagged:
            was_lagged = True
            self.df = self.df.drop(
                ["entries_t1", "exits_t1", "entries_t2", "exits_t2"], axis=1)
            self.lagged = False

        def apply_lowess_single_col(col):
            t = np.arange(len(col))
            # "missing" is so that NaN values aren't dropped
            z = lowess(col, t, missing="none")
            return col - z[:, 1]
        self.df = self.df.groupby(['caretype']).apply(lambda df: df.apply(apply_lowess_single_col))

        if was_lagged:
            self.create_lag_cols(self.lag_units)


# class DaySSData(DataFormat):
# def __init__(self, df, state_id):
# self.state_id = state_id
# super().__init__(df)


class WeekMSData(DataFormat):
    def __init__(self, df, lagged=False):
        super().__init__(df, lagged=False)

    def create_lag_cols(self, lag_units):
        super().create_lag_cols(lag_units, multistate=True)

    def get_national_total(self):
        # min_count to 1 makes empty return NaN instead of 0
        ret = WeekSSData(
            self.df.reset_index(level="state", drop=True).groupby(
                ['caretype', 'date']).sum(min_count=1),
            "NAT",
            lagged=self.lagged)
        ret.lag_units = self.lag_units
        return ret

    # returns list of WeekSSData
    def split_to_ss(self):
        return [
            WeekSSData(self.df.loc[state], state, lagged=self.lagged)
            for state in self.df.index.get_level_values('state').unique()
        ]

    def get_ss(self, state_id):
        ret = WeekSSData(
            self.df.loc[state_id],
            state_id,
            lagged=self.lagged)
        ret.lag_units = self.lag_units
        return ret


# class DayMSData(DataFormat):
# def __init__(self, df):
# super().__init__(df)
