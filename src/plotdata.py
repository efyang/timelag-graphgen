import colorings
import numpy as np


class PlotData:
    def __init__(self, df, title, coloring):
        self.df = df
        self.n = len(df)
        self.title = title
        self.mapping, self.colors, self.colorbar_label = colorings.get_coloring_info(coloring, self.n,
                                                  self.df.index.values)

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

        ax.set_title(column_prefix.upper() + ": " + self.title)
        # generate the graph, returning the plot handle
        return ax.scatter(xs, ys, zs, marker='o', s=size, c=self.colors)

    def update_data(self, ax, offset):
        assert (False)
