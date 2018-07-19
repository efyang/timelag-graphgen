import argparse
import sys
from colorings import str_to_coloring


class CliArgs:
    def __init__(self, args):
        self.input_file = args.INPUT_FILE
        self.coloring = str_to_coloring(args.coloring)
        self.output_file = args.OUTPUT_FILE
        self.entries_prefix = args.entries_prefix
        self.exits_prefix = args.exits_prefix
        self.data_name = args.data_name
        self.render_flag = "--render" in sys.argv
        custom_lag_length = "--lag" in sys.argv
        if custom_lag_length:
            self.lag_len = int(args.lag_len)
        else:
            self.lag_len = 1


def get_args():
    parser = argparse.ArgumentParser(description="Generate colored 3d lag plots of time-series data")
    parser.add_argument("-i", dest="INPUT_FILE")
    parser.add_argument("--coloring", dest="coloring")
    parser.add_argument("--render", dest="OUTPUT_FILE", required=False)
    parser.add_argument("entries_prefix")
    parser.add_argument('exits_prefix')
    parser.add_argument('data_name')
    parser.add_argument('--lag', dest="lag_len", required=False)
    args = parser.parse_args()
    return CliArgs(args)
