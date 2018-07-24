import pandas as pd
import sys

fname = sys.argv[1]
df = pd.read_csv(fname).groupby(['caretype', 'date']).sum()
maxes = df.groupby(['caretype']).max().max(axis=1)
sub_max = max([maxes.loc[x] for x in ['PFC', 'PCC', 'POT', 'PKC']])
total_max = maxes.loc['PTC']
print(sub_max, total_max)
