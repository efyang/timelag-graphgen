import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np


def get_colors(n, cmap_id, seasonal=False):
    cmap = plt.get_cmap(cmap_id)
    norm = mpl.colors.Normalize()
    m = cm.ScalarMappable(norm=norm, cmap=cmap)
    if seasonal:
        # seasonal coloring
        col = np.tile(np.arange(52), n // 52 + 1)[:n]
    else:
        col = np.arange(n)
    m.set_array(col)

    return m, m.to_rgba(col)
