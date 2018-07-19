import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib import colors
import numpy as np
from enum import Enum
import time_offset


class Coloring(Enum):
    LINEAR_ALL_TIME = 1
    LINEAR_SEASONAL = 2
    DISCRETE_MONTHS = 3
    DISCRETE_MONTHS_SPLIT_MARKERS = 4
    DISCRETE_MONTHS_POLYGONS = 5


def str_to_coloring(s):
    try:
        i = int(s)
        return Coloring(i)
    except ValueError:
        map_str = {"linear_all_time": 1,
                   "linear_seasonal": 2,
                   "discrete_months": 3,
                   "discrete_months_split_markers": 4,
                   "discrete_months_polygons": 5}
        try:
            i = map_str[s.lower()]
            return Coloring(i)
        except KeyError:
            raise Exception("No such coloring: " + s)


# return the mappable (for the colorbar), color array (for animation),
# and the label for the colorbar
def get_coloring_info(coloring_type, n, dates):
    if coloring_type == Coloring.LINEAR_ALL_TIME:
        cm = plt.get_cmap("viridis")
        mapping, colors = get_colors_cmap_linear(n, cm, False)
        colorbar_label = "Time in weeks"
    elif coloring_type == Coloring.LINEAR_SEASONAL:
        cm = plt.get_cmap("viridis")
        mapping, colors = get_colors_cmap_linear(n, cm, True)
        colorbar_label = "Time in weeks"
    elif coloring_type == Coloring.DISCRETE_MONTHS or coloring_type == Coloring.DISCRETE_MONTHS_SPLIT_MARKERS or coloring_type == Coloring.DISCRETE_MONTHS_POLYGONS:
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
        # repeats every year
        col = np.tile(np.arange(52), n // 52 + 1)[:n]
    else:
        col = np.arange(n)
        # never repeats
    m.set_array(col)

    # get the actual mapping and the array of values so that they can be sliced
    return m, m.to_rgba(col)


# extract a list of month numbers from the date column
def get_months(dates):
    return np.array([x.month for x in dates])


# create a discrete colormap (certain colors for certain months)
def discrete_colormap(months):
    cmap = colors.ListedColormap(['b', 'g', 'r', 'y'])
    bounds = [0, 4, 7, 10, 13]
    norm = colors.BoundaryNorm(bounds, cmap.N)
    m = cm.ScalarMappable(norm=norm, cmap=cmap)
    m.set_array(months)
    return m, m.to_rgba(months)
