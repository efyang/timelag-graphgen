import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib import colors
import numpy as np


def get_colors_cmap_linear(n, cmap, seasonal=False):
    norm = mpl.colors.Normalize()
    m = cm.ScalarMappable(norm=norm, cmap=cmap)
    if seasonal:
        # seasonal coloring
        col = np.tile(np.arange(52), n // 52 + 1)[:n]
    else:
        col = np.arange(n)
    m.set_array(col)

    return m, m.to_rgba(col)


def get_months(dates):
    return dates.apply(lambda x: x[:x.index('/')]).apply(int)


def discrete_colormap(months):
    cmap = colors.ListedColormap(['b', 'g', 'r', 'y'])
    bounds = [1, 3, 6, 9, 12]
    norm = colors.BoundaryNorm(bounds, cmap.N)
    m = cm.ScalarMappable(norm=norm, cmap=cmap)
    m.set_array(months)
    return m, m.to_rgba(months)
