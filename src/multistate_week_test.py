import sys
import fileformat
import colorings
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


fname = sys.argv[1]
x = fileformat.WeekMSFile(fname)
y = x.to_weekms_dataformat()
m = y.get_national_total()
p = m.to_plotdata("PTC", colorings.Coloring.DISCRETE_MONTHS)
ax = plt.subplot(projection="3d")
p.plot_data(ax, "entries")
plt.show()
