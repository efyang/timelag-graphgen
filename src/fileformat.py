import pandas as pd
import time_offset
import dataformat


class FileFormat:
    read_method = None

    def __init__(self, file_path):
        self.df = self.read_method(file_path)


class WeekPreformatSSFile(FileFormat):
    def __init__(self, file_path, state_id):
        self.read_method = pd.read_csv
        self.state_id = state_id
        super().__init__(file_path)

    def generate_time_col(self):
        included_dates = self.df['Start of interval']
        return included_dates.apply(time_offset.us_notation_to_date)

    def preprocess(self):
        time_col = self.generate_time_col()
        self.df = self.df.drop(["Start of interval", "Time"], axis=1)
        self.df["Date"] = time_col
        # TODO: should we do this?
        self.df = self.df.set_index("Date")

    def to_weekss_dataformat(self):
        self.preprocess()
        return dataformat.WeekSSData(self.df, self.state_id)


class DayAggregateSSFile(FileFormat):
    def __init__(self, file_path, state_id):
        self.read_method = pd.read_excel
        self.state_id = state_id
        super().__init__(self, file_path)

    def preprocess(self):
        self.df = self.df.resample('D', on="DATE").sum()

    def to_dayss_dataformat(self):
        self.preprocess()
        return dataformat.DaySSData(self.df, self.state_id)


class WeekMSFile(FileFormat):
    def __init__(self, file_path):
        super().__init__(self, file_path)


class DayMSFIle(FileFormat):
    def __init__(self, file_path):
        super().__init__(self, file_path)
