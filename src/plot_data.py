import pandas
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


def plot_data(ax, column_prefix, title, df):
    n = len(df)
    titles = [column_prefix+"_t"+str(i) for i in range(3)]
    xs = df[titles[0]]
    ys = df[titles[1]]
    zs = df[titles[2]]
    ax.set_xlabel(titles[0])
    ax.set_ylabel(titles[1])
    ax.set_zlabel(titles[2])

    cm = plt.get_cmap("viridis")
    col = np.arange(n)
    size = 15*np.ones(n)

    ax.view_init(elev=20, azim=-65)
    ax.set_title(title)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_zlim(0, 100)

    return ax.scatter(xs, ys, zs, facecolors='None', marker='o', s=size, c=col, cmap=cm)

