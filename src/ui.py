from matplotlib.widgets import Slider
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from colorings import Coloring
import calendar


class UI:
    def __init__(self, ss_plotdata, limit, coloring):
        self.ss_plotdata = ss_plotdata
        self.n = self.ss_plotdata.n
        self.limit = limit
        self.azimuth = 158
        self.elevation = -154
        self.fig = plt.figure()
        self.fig.set_size_inches(17, 9)
        gs = gridspec.GridSpec(
            2, 3, width_ratios=[1, 1, 0.1], height_ratios=[1, 0.05], left=0.05)

        self.fig.suptitle(ss_plotdata.title)

        self.entry_ax = plt.subplot(gs[0], projection='3d')
        self.entry_ax.view_init(elev=self.elevation, azim=self.azimuth)
        self.exit_ax = plt.subplot(gs[1], projection='3d')
        self.exit_ax.view_init(elev=self.elevation, azim=self.azimuth)
        # setup colorbar
        self.cb_ax = plt.subplot(gs[2])

        if coloring == Coloring.DISCRETE_MONTHS or coloring == Coloring.DISCRETE_MONTHS_SPLIT_MARKERS or coloring == Coloring.DISCRETE_MONTHS_POLYGONS:
            cbar = self.fig.colorbar(
                ss_plotdata.mapping,
                cax=self.cb_ax,
                label=ss_plotdata.colorbar_label,
                ticks=np.arange(1.5, 13.5, 1))
            cbar.ax.set_yticklabels(calendar.month_abbr[1:])
        else:
            self.fig.colorbar(
                ss_plotdata.mapping,
                cax=self.cb_ax,
                label=ss_plotdata.colorbar_label)

        self.slider_ax = plt.subplot(gs[1, :])

        self.time_slider = Slider(
            self.slider_ax,
            "Time",
            0,
            self.n,
            valinit=ss_plotdata.n,
            valstep=1,
            valfmt=("%0.0f " + ss_plotdata.lag_units))

        self.timestep = 0
        self.time_slider.on_changed(self.update_time)

    def draw(self, offset):
        self.ss_plotdata.update_data(self.entry_ax, self.exit_ax, offset)
        self.set_limit()

    def update_time(self, val):
        self.timestep = int(self.time_slider.val)
        self.draw(self.timestep)
        self.fig.canvas.draw_idle()

    def set_limit(self):
        if self.limit:
            set_all_limits(self.exit_ax, 0, self.limit)
            set_all_limits(self.entry_ax, 0, self.limit)

    def animate(self, k):
        self.timestep += 1
        self.timestep %= self.n
        print('\r{0:.2f}%'.format(100 * self.timestep/self.n), end='')
        self.time_slider.set_val(self.timestep)

    def render_animation_to_file(self, outfile):
        print("Rendering....")
        self.ani = animation.FuncAnimation(self.fig, self.animate, np.arange(0, self.n + 1), interval=20, repeat=False)
        self.ani.save(outfile, writer="ffmpeg")

    def render_image_to_file(self, outfile):
        self.draw(self.n)
        plt.draw()
        self.fig.savefig(outfile)

    def show_animation(self):
        self.ani = animation.FuncAnimation(self.fig, self.animate, np.arange(0, self.n + 1), interval=20, repeat=True)
        plt.show()

    def render_image(self, offset):
        pass


def set_all_limits(ax, dmin, dmax):
    ax.set_xlim(dmin, dmax)
    ax.set_ylim(dmin, dmax)
    ax.set_zlim(dmin, dmax)
