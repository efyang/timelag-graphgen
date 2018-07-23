from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import colorings

from scipy.spatial import ConvexHull
from matplotlib.tri import Triangulation


# just plot everything
def plot_data(ax, column_prefix, title, df, colors, coloring):
    n = len(df)
    # get the titles of the columns
    titles = [column_prefix + "_t" + str(i) for i in range(3)]

    # set the axial labesl
    ax.set_xlabel(titles[0])
    ax.set_ylabel(titles[1])
    ax.set_zlabel(titles[2])

    # generate the size of the dots (vector of size^2)
    size = 15 * np.ones(n)

    ax.set_title(title)
    # generate the graph, returning the plot handle
    if coloring == colorings.Coloring.DISCRETE_MONTHS_SPLIT_MARKERS or coloring == colorings.Coloring.DISCRETE_MONTHS_POLYGONS:
        d = {
            "1 2 3": ("+", 'b'),
            "4 5 6": ("o", 'g'),
            "7 8 9": ("^", 'r'),
            "10 11 12": ("D", 'y')
        }
        for vals, (marker, color) in d.items():
            mask = df['date'].apply(
                lambda x: x.month in map(int, vals.split(" ")))
            adf = df[mask]
            # get the actual columns
            xs = adf[titles[0]]
            ys = adf[titles[1]]
            zs = adf[titles[2]]

            if coloring == colorings.Coloring.DISCRETE_MONTHS_POLYGONS:
                X = np.array(list(zip(xs, ys, zs)))
                X = X[np.logical_not(np.isnan(zs))]
                if len(X) > 4:
                    cvx = ConvexHull(X)
                    tri = Triangulation(xs, ys, triangles=cvx.simplices)
                    ax.plot_trisurf(tri, zs, alpha=0.2, color=color)
                ax.scatter(
                    xs, ys, zs, marker='o', s=size[mask], c=colors[mask])
            else:
                ax.scatter(
                    xs, ys, zs, marker=marker, s=size[mask], c=colors[mask])
    else:
        xs = df[titles[0]]
        ys = df[titles[1]]
        zs = df[titles[2]]
        ax.scatter(xs, ys, zs, marker="o", s=size, c=colors)

    return None
    # return ax.scatter(xs, ys, zs, marker='o', s=size, c=colors)


def update_data(ax, time, column_prefix, df, colors, coloring):
    # set each title as the column title of the data
    title = ax.title.get_text()
    # clear the data
    ax.cla()
    # replot it (there is no equivalent set_y_data for 3d data
    # and even if there is, not sure if it would actually speed up)
    plot_data(ax, column_prefix, title, df[:time], colors[:time], coloring)


# set all axes to have a specific max
def set_all_limits(ax, dmin, dmax):
    ax.set_xlim(dmin, dmax)
    ax.set_ylim(dmin, dmax)
    ax.set_zlim(dmin, dmax)
