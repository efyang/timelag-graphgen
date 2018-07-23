import sys
import fileformat
import os

fname = sys.argv[1]
out_dir = sys.argv[2]
x = fileformat.WeekMSFile(fname)
y = x.to_weekms_dataformat()
for state_data in y.split_to_ss():
    filename = state_data.state_id + "_PREPROCESSED.csv"
    path = os.path.join(out_dir, filename)
    print(path)
    state_data.write(path)
