import colorings


class PlotData:
    def __init__(self, df, caretype, title, coloring):
        self.df = df.loc[caretype]
        self.n = len(df)
        self.title = title
        self.caretype = caretype
        self.colors = colorings.get_coloring_info(coloring, self.n, self.df.index.values)

    def plot_data(self, ax, offset=self.n):
        assert(False)

    def update_data(self, ax, offset):
        assert(False)


