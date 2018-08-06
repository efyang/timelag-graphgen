import colorings
from colorings import Coloring
import numpy as np

from scipy.spatial import ConvexHull
from matplotlib.tri import Triangulation


class PlotData:
    def __init__(self, df, title, coloring, caretype, lag_units, drop_yearly):
        self.df = df
        self.n = len(df)
        self.title = title
        self.coloring = coloring
        self.mapping, self.colors, self.colorbar_label = colorings.get_coloring_info(
            coloring, self.n, self.df['date'])
        self.caretype = caretype
        self.drop_yearly = drop_yearly
        self.lag_units = lag_units

    def plot_data(self, ax, column_prefix, offset=None):
        # default value workaround
        if offset is None:
            offset = self.n

        if offset > 0:
            data_portion = self.df[:offset]
            if self.drop_yearly and offset > 0:
                current_date = self.df.loc[offset - 1]['date']
                year_mask = data_portion['date'].apply(
                    lambda x: (current_date - x).days <= 365.25)
                data_portion = data_portion[year_mask]

            titles = [column_prefix + "_t" + str(i) for i in range(3)]
            # set the axial labesl
            ax.set_xlabel(titles[0])
            ax.set_ylabel(titles[1])
            ax.set_zlabel(titles[2])

            # generate the size of the dots (vector of size^2)
            size = 7 * np.ones(len(data_portion))

            if self.coloring == Coloring.DISCRETE_MONTHS_SPLIT_MARKERS or self.coloring == Coloring.DISCRETE_MONTHS_POLYGONS:
                d = {
                    "1 2 3": ("+", 'b'),
                    "4 5 6": ("o", 'g'),
                    "7 8 9": ("^", 'r'),
                    "10 11 12": ("D", 'y')
                }
                for vals, (split_marker, color) in d.items():
                    mask = data_portion['date'].apply(
                        lambda x: x.month in map(int, vals.split(" ")))
                    adf = data_portion[mask]
                    # get the actual columns
                    xs = adf[titles[0]]
                    ys = adf[titles[1]]
                    zs = adf[titles[2]]
                    if self.coloring == Coloring.DISCRETE_MONTHS_POLYGONS:
                        try:
                            X = np.array(list(zip(xs, ys, zs)))
                            if len(X) > 4:
                                cvx = ConvexHull(X)
                                tri = Triangulation(xs, ys, triangles=cvx.simplices)
                                ax.plot_trisurf(tri, zs, alpha=0.2, color=color)
                        except Exception:
                            print("Couldn't draw convex hull")
                    if self.coloring == Coloring.DISCRETE_MONTHS_SPLIT_MARKERS:
                        marker = split_marker
                    else:
                        marker = 'o'
                    ax.scatter(xs, ys, zs, marker=marker, s=size[mask], c=color)
            else:
                xs = data_portion[titles[0]]
                ys = data_portion[titles[1]]
                zs = data_portion[titles[2]]
                if self.drop_yearly:
                    ax.scatter(xs, ys, zs, marker="o", s=size, c=self.colors[:offset][year_mask])
                else:
                    ax.scatter(xs, ys, zs, marker="o", s=size, c=self.colors[:offset])

            ax.set_title(self.caretype + " " + column_prefix.capitalize())

    def update_data(self, entry_ax, exit_ax, offset):
        entry_ax.clear()
        exit_ax.clear()
        self.plot_data(entry_ax, "entries", offset)
        self.plot_data(exit_ax, "exits", offset)
