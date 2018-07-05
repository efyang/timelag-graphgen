import pandas
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


def plot_data(ax, column_prefix, title, df, seasonal=False):
    n = len(df)
    titles = [column_prefix+"_t"+str(i) for i in range(3)]
    xs = df[titles[0]]
    ys = df[titles[1]]
    zs = df[titles[2]]
    ax.set_xlabel(titles[0])
    ax.set_ylabel(titles[1])
    ax.set_zlabel(titles[2])

    cm = plt.get_cmap("viridis")
    size = 15*np.ones(n)
    if seasonal:
        # seasonal coloring
        col = np.tile(np.arange(52), n // 52 + 1)[:n]
    else:
        col = np.arange(n)


    ax.view_init(elev=10, azim=-165)
    ax.set_title(title)
    return ax.scatter(xs, ys, zs, facecolors='None', marker='o', s=size, c=col, cmap=cm)


def set_all_maxes(ax, m):
    ax.set_xlim(0, m)
    ax.set_ylim(0, m)
    ax.set_zlim(0, m)
