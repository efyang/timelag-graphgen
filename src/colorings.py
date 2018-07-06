import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib import colors
import numpy as np
from enum import Enum


class Coloring(Enum):
    LINEAR_ALL_TIME = 1
    LINEAR_SEASONAL = 2
    DISCRETE_MONTHS = 3


def str_to_coloring(s):
    try:
        i = int(s)
        return Coloring(i)
    except ValueError:
        map_str = {"linear_all_time": 1,
                   "linear_seasonal": 2,
                   "discrete_months": 3}
        try:
            i = map_str[s.lower()]
            return Coloring(i)
        except KeyError:
            raise Exception("No such coloring: " + s)



def get_coloring_info(coloring_type, df):
    if coloring_type == Coloring.LINEAR_ALL_TIME:
        cm = plt.get_cmap("viridis")
        mapping, colors = get_colors_cmap_linear(len(df), cm, False)
        colorbar_label = "Time in weeks"
    elif coloring_type == Coloring.LINEAR_SEASONAL:
        cm = plt.get_cmap("viridis")
        mapping, colors = get_colors_cmap_linear(len(df), cm, True)
        colorbar_label = "Time in weeks"
    elif coloring_type == Coloring.DISCRETE_MONTHS:
        dates = df['Start of interval']
        months = get_months(dates)
        mapping, colors = discrete_colormap(months)
        colorbar_label = "Month"
    else:
        raise Exception("No such coloring")
    return mapping, colors, colorbar_label


def get_colors_cmap_linear(n, cmap, seasonal):
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
