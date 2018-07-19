import sys
import fileformat
import colorings
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

fname = sys.argv[1]
x = fileformat.WeekPreformatSSFile(fname, "TN")
y = x.to_weekss_dataformat()
y.set_lag_amount(2)
z = y.apply_lowess()
p = z.to_plotdata("PTC", colorings.Coloring.DISCRETE_MONTHS)
ax = plt.subplot(projection="3d")
p.plot_data(ax, "entries")
plt.show()
