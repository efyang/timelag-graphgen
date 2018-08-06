import argparse
import sys
from colorings import colorings_map_str, str_to_coloring
from fileformat import fileformat_map_str, str_to_format


class CliArgs:
    def __init__(self, args):
        self.input_file = args.INPUT_FILE
        self.file_format = str_to_format(args.file_format)
        self.coloring = str_to_coloring(args.coloring)
        self.state_id = args.state_id
        self.output_file = args.OUTPUT_FILE
        self.ppf = args.ppf
        self.caretype = args.caretype
        self.lowess = args.lowess
        self.render_flag = "--render" in sys.argv
        self.render_video = self.render_flag and (".mp4" in args.OUTPUT_FILE)
        self.drop_yearly = "--dropyearly" in sys.argv
        if args.limit:
            self.limit = args.limit
        else:
            self.limit = None
        custom_lag_length = "--lag" in sys.argv
        if not self.ppf:
            self.ppf = 1
        if custom_lag_length:
            self.lag_len = int(args.lag_len)
        else:
            self.lag_len = 1


def get_args():
    parser = argparse.ArgumentParser(description="Generate colored 3d lag plots of time-series data")
    parser.add_argument("-i", dest="INPUT_FILE", required=True)
    parser.add_argument("-f", dest="file_format", required=True, choices=[a for a,b in fileformat_map_str.items()])
    parser.add_argument("-s", dest="state_id", required=True)
    parser.add_argument("--coloring", dest="coloring", required=True, choices=[a for a,b, in colorings_map_str.items()])
    parser.add_argument("--limit", dest="limit", type=int, required=False)
    parser.add_argument("--caretype", dest="caretype", required=True)
    parser.add_argument("--render", dest="OUTPUT_FILE", required=False)
    parser.add_argument('--lag', dest="lag_len", required=False)
    parser.add_argument("--dropyearly", action='store_true', required=False)
    parser.add_argument("--lowess", action='store_true', required=False)
    parser.add_argument('--ppf', dest="ppf", type=int, required=False)
    args = parser.parse_args()
    return CliArgs(args)
