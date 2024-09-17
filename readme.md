# Weibo data collection filter

run.py is the entrance point. It calls the `run_main` where specific functions can be called.

There are 3 useful functions for now:
- `run_filter()`
runs the filter over all csv files in the input folder. The input folder is specified in `consts.py`.

- `get_missing_for_year`
print the missing hours for a whole year and optional

- `get_missing_for_range`
print the missing hours between 2 different times (specified with 2 datetimes)


