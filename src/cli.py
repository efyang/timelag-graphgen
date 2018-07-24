import argparse
import sys
from colorings import str_to_coloring
from fileformat import str_to_format


class CliArgs:
    def __init__(self, args):
        self.input_file = args.INPUT_FILE
        self.file_format = str_to_format(args.file_format)
        self.coloring = str_to_coloring(args.coloring)
        self.state_id = args.state_id
        self.output_file = args.OUTPUT_FILE
        self.caretype = args.caretype
        self.preprocess_out_dir = args.preprocess_out_dir
        self.render_flag = "--render" in sys.argv
        self.render_video = self.render_flag and (".mp4" in args.OUTPUT_FILE)
        self.drop_yearly = "--dropyearly" in sys.argv
        if args.limit:
            self.limit = args.limit
        custom_lag_length = "--lag" in sys.argv
        if custom_lag_length:
            self.lag_len = int(args.lag_len)
        else:
            self.lag_len = 1


def get_args():
    parser = argparse.ArgumentParser(description="Generate colored 3d lag plots of time-series data")
    parser.add_argument("-i", dest="INPUT_FILE")
    parser.add_argument("-f", dest="file_format")
    parser.add_argument("-s", dest="state_id")
    parser.add_argument("--preprocess", dest="preprocess_out_dir", required=False)
    parser.add_argument("--coloring", dest="coloring")
    parser.add_argument("--limit", dest="limit", type=int, required=False)
    parser.add_argument("--caretype", dest="caretype")
    parser.add_argument("--render", dest="OUTPUT_FILE", required=False)
    parser.add_argument('--lag', dest="lag_len", required=False)
    parser.add_argument("--dropyearly", action='store_true', required=False)
    args = parser.parse_args()
    return CliArgs(args)
