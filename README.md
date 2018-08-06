# timelag-graphgen
Generate colored graphs/animations of time-series data

## Installation
This program uses python 3. To install all of the dependencies, run:

`pip install -r requirements.txt --user`

## Usage
Call `python timelag-graphgen/main.py ARGS`, where `ARGS` are
* `-i INPUT_FILE` (required)
    * The input data file to use
* `-f FORMAT` (required)
    * The file format that the input data file is in
        * `weekss` - Single state, weekly (csv format) - don't know if this still works?
            * Start of interval
            * Time
            * Entries_KIN_t0
            * Exits_KIN_t0
            * Entries_FC_t0
            * Exits_FC_t0
            * Entries_CC_t0
            * Exits_CC_t0
        * `dayss` - Single state, daily - do not use
        * `dayssp` - Single state, daily, preprocessed - output of preprocess scripts
        * `weekssp` - Single state, weekly, preprocessed - output of preprocess scripts
        * `weekms` - Multistate week file (stata format)
            * state
            * county
            * caretype
            * year
            * admitcount
            * exitcount
            * week2
            * week4
            * geo
            * geo1
        * `dayms` - Multistate day file (csv format, | delimited)
            * date
            * state
            * county
            * caretype
            * admitcount
            * exitcount
            * year
* `-s STATE_ID` (required)
    * The ID of the state (e.g. CA)
* `--coloring COLORING` (required)
    * The coloring type to use; can be one of:
        * `linear_all_time`
        * `linear_seasonal`
        * `discrete_months`
        * `discrete_months_split_markers`
        * `discrete_months_polygons`
* `--limit LIMIT` (optional, defaults to autoscale)
    * The maximum limit to use
* `--caretype CARETYPE` (required)
    * The caretype to view
* `--render OUTPUT_FILE` (optional, defaults to none)
    * Whether to render to an output file, and if so, where
    * If none, then will show interactive animation
    * If mp4, will render animation to mp4 output file
    * If image (only png tested), will render final step to image file
* `--lag LAG_LEN` (optional, defaults to 1)
    * The number of lag steps to use, always in the current time unit
    * e.g. for weekly data `--lag 1` means a lag of 1 week, for daily data it means lag of 1 day
* `--dropyearly` (optional, defaults to false)
    * Whether to drop all data more than a year before the current animation time
* `--lowess` (optional, defaults to false)
    * Whether to use the residuals from lowess smoothing
* `--ppf POINTS_PER_FRAME` (optional, defaults to false)
    * Points to animate per frame - can vastly help in reducing render times (7 for daily data recommended)

### Other useful files
* `render_wave_3.sh`: script used to render wave 3, might be useful to look over
* `preprocess_multi.py` and `preprocess_mult_daily.py`: preprocess multistate files into state-level files
    * Use weekms and dayms files, respectively
    * arg1: input file
    * arg2: output directory
