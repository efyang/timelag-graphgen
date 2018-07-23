from cli import get_args
from ui import UI
import fileformat

args = get_args()
multistate = args.file_format == fileformat.WeekMSFile or args.file_format == fileformat.DayMSFile
if multistate:
    f = args.file_format(args.input_file)
else:
    f = args.file_format(args.input_file, args.state_id)
data = f.to_dataformat()

# TODO: add preprocess ability

if multistate:
    ss_data = data.get_ss(args.state_id)
else:
    ss_data = data

plot_data = ss_data.to_plotdata(args.caretype, args.coloring)

ui = UI(plot_data, args.limit, args.coloring)
ui.draw(plot_data.n)

if args.render_flag:
    ui.render_animation_to_file(args.output_file)
else:
    ui.show_animation()
