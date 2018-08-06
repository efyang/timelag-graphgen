import sys
import fileformat
import os

fname = sys.argv[1]
out_dir = sys.argv[2]
x = fileformat.DayMSFile(fname)
y = x.to_dayms_dataformat()
for state_data in y.split_to_ss():
    filename = state_data.state_id + "_DAILY_PREPROCESSED.csv"
    path = os.path.join(out_dir, filename)
    print(path)
    state_data.write(path)
