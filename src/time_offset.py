import datetime

# we want everything as the offset in days from the date epoch, which we set as
# Jan 1, 1960
DEFAULT_DATE_EPOCH = datetime.date(year=1960, month=1, day=1)


def get_day_offset(d):
    return (d - DEFAULT_DATE_EPOCH).days


def us_notation_to_date(s):
    return datetime.datetime.strptime(s, '%m/%d/%y').date()


def ymd_notation_to_date(s):
    return datetime.datetime.strptime(s, '%y-%m-%d').date()
