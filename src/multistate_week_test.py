import pandas as pd
import sys
import fileformat

fname = sys.argv[1]
x = fileformat.WeekMSFile(fname)
y = x.to_weekms_dataformat()
y.create_lag_cols(1)
# print(proc.ix['CA'])
