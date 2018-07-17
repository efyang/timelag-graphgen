import sys
import fileformat

fname = sys.argv[1]
x = fileformat.WeekPreformatSSFile(fname, "TN")
y = x.to_weekss_dataformat()
print(y.df)
y.apply_lowess_all_cols()
print(y.df)
# y.create_lag_cols(1)
