from mpl_toolkits.mplot3d import Axes3D
import numpy as np


# just plot everything
def plot_data(ax, column_prefix, title, df, colors):
    n = len(df)
    # get the titles of the columns
    titles = [column_prefix+"_t"+str(i) for i in range(3)]
    # get the actual columns
    xs = df[titles[0]]
    ys = df[titles[1]]
    zs = df[titles[2]]
    # set the axial labesl
    ax.set_xlabel(titles[0])
    ax.set_ylabel(titles[1])
    ax.set_zlabel(titles[2])

    # generate the size of the dots (vector of size^2)
    size = 15*np.ones(n)

    ax.set_title(title)
    # generate the graph, returning the plot handle
    return ax.scatter(xs, ys, zs, facecolors='None', marker='o', s=size, c=colors)


def update_data(ax, time, column_prefix, df, colors):
    # set each title as the column title of the data
    title = ax.title.get_text()
    # clear the data
    ax.cla()
    # replot it (there is no equivalent set_y_data for 3d data
    # and even if there is, not sure if it would actually speed up)
    plot_data(ax, column_prefix, title, df[:time], colors[:time])


# set all axes to have a specific max
def set_all_maxes(ax, m):
    ax.set_xlim(0, m)
    ax.set_ylim(0, m)
    ax.set_zlim(0, m)
