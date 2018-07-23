import pandas as pd
import time_offset
import dataformat


class FileFormat:
    read_method = None

    def __init__(self, file_path):
        self.df = self.read_method(file_path)
        self.preprocessed = False


class WeekPreprocessedSSFile(FileFormat):
    def __init__(self, file_path, state_id):
        self.read_method = pd.read_csv
        self.state_id = state_id
        super().__init__(file_path)

    def generate_time_col(self):
        included_dates = self.df['date']
        return included_dates.apply(time_offset.ymd_notation_to_date)

    def preprocess(self):
        self.df['date'] = self.generate_time_col()
        self.df = self.df.groupby(['caretype', 'date']).sum()
        self.preprocessed = True

    def to_weekss_dataformat(self):
        if not self.preprocessed:
            self.preprocess()
        return dataformat.WeekSSData(self.df, self.state_id)

    def to_dataformat(self):
        return self.to_weekss_dataformat()


class WeekPreformatSSFile(FileFormat):
    caretype_mapping = {'CC': 'PCC', 'FC': 'PFC', 'KIN': 'PKC'}

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
        self.df["date"] = time_col

        y = pd.DataFrame(self.df.set_index("date").unstack())
        y.index.names = ['caretype', 'date']
        z = y.reset_index()
        z[[
            'name', 'caretype'
        ]] = z['caretype'].apply(lambda x: x.split('_')[:-1]).apply(pd.Series)
        z['caretype'] = z['caretype'].apply(lambda x: self.caretype_mapping[x])
        self.df = z.pivot_table(
            index=['caretype', 'date'], columns='name', values=0)

        self.df = self.df.append(
            self.df.groupby(['date']).sum().assign(caretype="PTC")
            .groupby(['caretype', 'date']).sum())

        self.preprocessed = True

    def to_weekss_dataformat(self):
        if not self.preprocessed:
            self.preprocess()
        return dataformat.WeekSSData(self.df, self.state_id)

    def to_dataformat(self):
        return self.to_weekss_dataformat()


class DayAggregateSSFile(FileFormat):
    def __init__(self, file_path, state_id):
        self.read_method = pd.read_excel
        self.state_id = state_id
        super().__init__(file_path)

    def preprocess(self):
        self.df = self.df.resample('D', on="DATE").sum()
        self.preprocessed = True

    def to_dayss_dataformat(self):
        if not self.preprocessed:
            self.preprocess()
        return dataformat.DaySSData(self.df, self.state_id)

    def to_dataformat(self):
        return self.to_dayss_dataformat()


class WeekMSFile(FileFormat):
    def __init__(self, file_path):
        self.read_method = pd.read_stata
        super().__init__(file_path)

    def generate_time_col(self):
        included_dates = self.df["week2"]
        return included_dates.apply(time_offset.wk_notation_to_date)

    def preprocess(self):
        time_col = self.generate_time_col()
        self.df['week2'] = time_col
        self.df.rename(
            columns={
                'week2': 'date',
                'admitcount': 'entries',
                'exitcount': 'exits'
            },
            inplace=True)
        self.df = self.df.drop(
            ['county', 'year', 'week4', 'geo1', 'geo'],
            axis=1).groupby(['state', 'caretype', 'date']).sum()

        # determine aggregate total
        self.df = self.df.append(
            self.df.groupby(['state', 'date']).sum().assign(caretype="PTC")
            .groupby(['state', 'caretype', 'date']).sum())

        self.preprocessed = True

    def to_weekms_dataformat(self):
        if not self.preprocessed:
            self.preprocess()
        return dataformat.WeekMSData(self.df)

    def to_dataformat(self):
        return self.to_weekms_dataformat()


class DayMSFile(FileFormat):
    def __init__(self, file_path):
        super().__init__(file_path)

    def to_dayms_dataformat(self):
        assert(False)

    def to_dataformat(self):
        return self.to_dayms_dataformat()


def str_to_format(s):
    map_str = {
        "weekss": WeekPreformatSSFile,
        "weekssp": WeekPreprocessedSSFile,
        "dayss": DayAggregateSSFile,
        "weekms": WeekMSFile,
        "dayms": DayMSFile,
    }
    try:
        i = map_str[s.lower().replace(' ', '').replace('_', '')]
        return i
    except KeyError:
        raise Exception("No such coloring: " + s)
