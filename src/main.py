import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.widgets import Slider
import matplotlib.animation as animation
import numpy as np
import argparse
import sys

from read_data import read_file, process_df, find_max_val, find_min_val
from plot_data import plot_data, set_all_limits, update_data
from colorings import get_coloring_info, str_to_coloring
import time_offset


parser = argparse.ArgumentParser(description="Generate colored 3d lag plots of time-series data")
parser.add_argument("-i", dest="INPUT_FILE")
parser.add_argument("--coloring", dest="coloring")
parser.add_argument("--render", dest="out_file", required=False)
parser.add_argument("entries_prefix")
parser.add_argument('exits_prefix')
parser.add_argument('data_name')
parser.add_argument('--lag', dest="lag_len", required=False)
render_flag = "--render" in sys.argv
custom_lag_length = "--lag" in sys.argv
args = parser.parse_args()

# set the viewpoint
# chosen so that the origin is on the bottom-left side of the figure for
# most easily understandable viewing
azimuth = -100
elevation = 10

fig = plt.figure()
fig.set_size_inches(17, 9)

if custom_lag_length:
    lag_len_weeks = int(args.lag_len)
else:
    lag_len_weeks = 1

gs = gridspec.GridSpec(2, 3, width_ratios=[1, 1, 0.1], height_ratios=[1, 0.05],
                       left=0.05)

df = read_file(args.INPUT_FILE)
df['Start of interval'] = df['Start of interval'].apply(time_offset.us_notation_to_date)
entries_lagged = process_df(df, args.entries_prefix, lag_len_weeks)
exits_lagged = process_df(df, args.exits_prefix, lag_len_weeks)
maxv = max(find_max_val(entries_lagged, args.entries_prefix), find_max_val(exits_lagged, args.exits_prefix))
minv = min(find_min_val(entries_lagged, args.entries_prefix), find_min_val(exits_lagged, args.exits_prefix))
num_timesteps = len(entries_lagged)
coloring = str_to_coloring(args.coloring)
mapping, colors, colorbar_label = get_coloring_info(coloring, len(df), df['Start of interval'])

fig.suptitle("3D Lag Plot For " + args.data_name + "(Autogenerated) Lag=" + str(lag_len_weeks)+" weeks")
ax = plt.subplot(gs[0], projection='3d')
ax.view_init(elev=elevation, azim=azimuth)
plot = plot_data(ax, args.entries_prefix, args.entries_prefix, entries_lagged, colors, coloring)

ax2 = plt.subplot(gs[1], projection='3d')
ax2.view_init(elev=elevation, azim=azimuth)
plot2 = plot_data(ax2, args.exits_prefix, args.exits_prefix, exits_lagged, colors, coloring)

set_all_limits(ax, minv, maxv)
set_all_limits(ax2, minv, maxv)


cbaxes = plt.subplot(gs[2])
fig.colorbar(mapping, cax=cbaxes, label=colorbar_label)


slider_ax = plt.subplot(gs[1, :])
time_slider = Slider(slider_ax, "Time", 0, num_timesteps,
                     valinit=num_timesteps, valstep=1, valfmt="%0.0f weeks")
timestep = 0


def update_time(val):
    global timestep
    timestep = time_slider.val
    time = int(time_slider.val)
    update_data(ax, time, args.entries_prefix, entries_lagged, colors, coloring)
    update_data(ax2, time, args.exits_prefix, exits_lagged, colors, coloring)
    set_all_limits(ax, minv, maxv)
    set_all_limits(ax2, minv, maxv)
    fig.canvas.draw_idle()


time_slider.on_changed(update_time)


def animate(k):
    global timestep
    timestep += 1
    timestep %= num_timesteps
    print('\r{0:.2f}%'.format(100 * timestep/num_timesteps), end='')
    time_slider.set_val(timestep)


plt.tight_layout()

if render_flag:
    print("Rendering....")
    ani = animation.FuncAnimation(fig, animate, np.arange(0, num_timesteps), interval=20, repeat=False)
    ani.save(args.out_file, writer="ffmpeg")
else:
    ani = animation.FuncAnimation(fig, animate, np.arange(0, num_timesteps), interval=20, repeat=True)
    plt.show()

