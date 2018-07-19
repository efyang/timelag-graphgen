import pandas as pd
import numpy as np
import statsmodels.api as sm
import copy
import plotdata
lowess = sm.nonparametric.lowess
idx = pd.IndexSlice


class DataFormat:
    base_groups = []

    def __init__(self, df):
        self.df = df
        self.lag_amount = 1
        self.title_annotation = ""

    def set_lag_amount(self, lag_amount):
        self.lag_amount = lag_amount

    def create_lag_cols(self):
        grouping = self.df.groupby(self.base_groups)
        lag_0 = self.df
        lag_1 = grouping.shift(self.lag_amount)
        lag_2 = grouping.shift(2 * self.lag_amount)

        new = copy.copy(self)

        new.df = pd.concat([lag_0, lag_1, lag_2], axis=1)
        new.df.columns = [
            'entries_t0', 'exits_t0', 'entries_t1', 'exits_t1', 'entries_t2',
            'exits_t2'
        ]
        return new

    def apply_lowess(self):
        def apply_lowess_single_col(col):
            t = np.arange(len(col))
            # "missing" is so that NaN values aren't dropped
            z = lowess(col, t, missing="none")
            return col - z[:, 1]

        new = copy.copy(self)
        new.title_annotation = "(Resid. from Lowess)"
        new.df = self.df.groupby(self.base_groups).apply(
            lambda df: df.apply(apply_lowess_single_col))
        return new


class WeekSSData(DataFormat):
    base_groups = ['caretype']
    lag_units = "Weeks"

    def __init__(self, df, state_id):
        self.state_id = state_id
        super().__init__(df)

    def to_plotdata(self, caretype, coloring):
        title = self.state_id + " " + caretype + ": lag=" + str(
            self.lag_amount) + " " + self.lag_units + " " + self.title_annotation
        return plotdata.PlotData(self.create_lag_cols().df.loc[caretype].reset_index(level="date"),
                                 title, coloring)


# class DaySSData(DataFormat):
# def __init__(self, df, state_id):
# self.state_id = state_id
# super().__init__(df)


class WeekMSData(DataFormat):
    base_groups = ['state', 'caretype']

    def __init__(self, df):
        super().__init__(df)

    def get_national_total(self):
        # min_count to 1 makes empty return NaN instead of 0
        ret = WeekSSData(
            self.df.reset_index(level="state", drop=True).groupby(
                ['caretype', 'date']).sum(min_count=1),
            "NAT")
        ret.lag_amount = self.lag_amount
        return ret

    # returns list of WeekSSData
    def split_to_ss(self):
        return [
            WeekSSData(self.df.loc[state], state)
            for state in self.df.index.get_level_values('state').unique()
        ]

    def get_ss(self, state_id):
        ret = WeekSSData(self.df.loc[state_id], state_id)
        ret.lag_amount = self.lag_amount
        return ret


# class DayMSData(DataFormat):
# def __init__(self, df):
# super().__init__(df)
