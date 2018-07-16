class DataFormat:
    def __init__(self, df, state_id):
        self.df = df


class WeekSSData(DataFormat):
    def __init__(self, df, state_id):
        self.state_id = state_id
        super().__init__(df)

    def lag_process(self, lag_weeks):
        assert(False)


class DaySSData(DataFormat):
    def __init__(self, df, state_id):
        self.state_id = state_id
        super().__init__(df)


class WeekMSData(DataFormat):
    def __init__(self, df):
        super().__init__(df)


class DayMSData(DataFormat):
    def __init__(self, df):
        super().__init__(df)
