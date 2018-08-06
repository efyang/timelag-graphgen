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


class DayPreprocessedSSFile(FileFormat):
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
        self.df = pd.read_csv(file_path, sep='|')
        self.preprocessed = False

    def preprocess(self):
        self.df['date'] = self.df['date'].apply(
            time_offset.us_notation_long_to_date)
        self.df['date'] = pd.to_datetime(self.df['date'])
        self.df = self.df.drop(
            ['year', 'county'], axis=1).groupby(['state', 'caretype',
                                                 'date']).sum()

        # determine aggregate total
        self.df = self.df.append(
            self.df.groupby(['state', 'date']).sum().assign(caretype="PTC")
            .groupby(['state', 'caretype', 'date']).sum())

        # fill in missing dates
        self.df = self.df.groupby(['state', 'caretype']).apply(lambda d: d.reset_index(level=['state','caretype'], drop=True).resample('D').sum())

        self.preprocessed = True

    def to_dayms_dataformat(self):
        if not self.preprocessed:
            self.preprocess()
        return dataformat.DayMSData(self.df)

    def to_dataformat(self):
        return self.to_dayms_dataformat()


fileformat_map_str = {
    "weekss": WeekPreformatSSFile,
    "weekssp": WeekPreprocessedSSFile,
    "dayss": DayAggregateSSFile,
    "dayssp": DayPreprocessedSSFile,
    "weekms": WeekMSFile,
    "dayms": DayMSFile,
}


def str_to_format(s):
    try:
        i = fileformat_map_str[s.lower().replace(' ', '').replace('_', '')]
        return i
    except KeyError:
        raise Exception("No such coloring: " + s)
