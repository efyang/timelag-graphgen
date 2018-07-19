import colorings
import numpy as np

from scipy.spatial import ConvexHull
from matplotlib.tri import Triangulation


class PlotData:
    def __init__(self, df, title, coloring):
        self.df = df
        self.n = len(df)
        self.title = title
        self.coloring = coloring
        self.mapping, self.colors, self.colorbar_label = colorings.get_coloring_info(coloring, self.n,
                                                  self.df['date'])

    def plot_data(self, ax, column_prefix, offset=None):
        # default value workaround
        if offset is None:
            offset = self.n

        titles = [column_prefix + "_t" + str(i) for i in range(3)]

        xs = self.df[titles[0]]
        ys = self.df[titles[1]]
        zs = self.df[titles[2]]
        # set the axial labesl
        ax.set_xlabel(titles[0])
        ax.set_ylabel(titles[1])
        ax.set_zlabel(titles[2])

        # generate the size of the dots (vector of size^2)
        size = 15 * np.ones(self.n)

        if self.coloring == colorings.Coloring.DISCRETE_MONTHS_SPLIT_MARKERS or self.coloring == colorings.Coloring.DISCRETE_MONTHS_POLYGONS:
            d = {"1 2 3": ("+", 'b'), "4 5 6": ("o", 'g'), "7 8 9": ("^", 'r'), "10 11 12": ("D", 'y')}
            for vals, (marker, color) in d.items():
                mask = self.df['date'].apply(lambda x: x.month in map(int, vals.split(" ")))
                adf = self.df[mask]
                print(adf)
                # get the actual columns
                xs = adf[titles[0]]
                ys = adf[titles[1]]
                zs = adf[titles[2]]
                if self.coloring == colorings.Coloring.DISCRETE_MONTHS_POLYGONS:
                    X = np.array(list(zip(xs, ys, zs)))
                    X = X[np.logical_not(np.isnan(zs))]
                    if len(X) > 4:
                        cvx = ConvexHull(X)
                        tri = Triangulation(xs, ys, triangles=cvx.simplices)
                        ax.plot_trisurf(tri, zs, alpha=0.2, color=color)
                    ax.scatter(xs, ys, zs, marker='o', s=size[mask], c=self.colors[mask])
                else:
                    ax.scatter(xs, ys, zs, marker=marker, s=size[mask], c=self.colors[mask])
        else:
            xs = self.df[titles[0]]
            ys = self.df[titles[1]]
            zs = self.df[titles[2]]
            ax.scatter(xs, ys, zs, marker="o", s=size, c=self.colors)

        ax.set_title(column_prefix.upper() + ": " + self.title)

    def update_data(self, ax, offset):
        assert (False)
