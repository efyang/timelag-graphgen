import sys
import fileformat
import plotly
import plotly.graph_objs as go
import datetime

fname = sys.argv[1]
state_id = sys.argv[2]
caretype = sys.argv[3]
outfile = sys.argv[4]

# should be in preprocessed week format
f = fileformat.WeekPreprocessedSSFile(fname, state_id)
d = f.to_weekss_dataformat()
weekly = d.df.loc[caretype]
weekly["net"] = (weekly['entries'] - weekly['exits'])
weekly['cumsum'] = weekly["net"].cumsum()

group_monthly = weekly.groupby([lambda x: x.year, lambda x: x.month])


def regroup_dates(raw):
    raw = raw.reset_index()
    raw['date'] = raw.apply(lambda row: datetime.date(year=row['level_0'], month=row['level_1'], day=1), axis=1)
    del raw['level_0']
    del raw['level_1']
    return raw


initial_value = 0

monthly = regroup_dates(group_monthly.sum().rename(columns={0: 'net'}))
monthly['cumsum'] = initial_value + monthly['net'].cumsum()
monthly['close'] = monthly['cumsum']
monthly['open'] = monthly['close'].shift(1).fillna(initial_value)
monthly['hi'] = initial_value + group_monthly['cumsum'].max().reset_index()['cumsum']
monthly['lo'] = initial_value + group_monthly['cumsum'].min().reset_index()['cumsum']
# get the actual maximums including the endpoints
monthly['hi'] = monthly[['open', 'hi', 'close']].max(axis=1)
monthly['lo'] = monthly[['open', 'lo', 'close']].min(axis=1)

trace = go.Candlestick(
    x=monthly['date'],
    open=monthly['open'],
    high=monthly['hi'],
    low=monthly['lo'],
    close=monthly['close'])
data = [trace]
plotly.offline.plot(
    {
        "data": data,
        "layout": go.Layout(title=state_id + " " + caretype + " MONTHLY")
    },
    auto_open=False,
    filename=outfile)
# print(plotly.offline.plot(
    # {
        # "data": data,
        # "layout": go.Layout(title=state_id + " " + caretype + " MONTHLY")
    # },
    # output_type='div',
    # include_plotlyjs=False))
