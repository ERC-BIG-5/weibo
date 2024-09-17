from datetime import datetime

from filter_data import run_filter, get_missing_for_range, get_missing_for_range

def run_main():
    run_filter()
    # get_missing_for_year(2023, 7)
    # get_missing_for_range(datetime(year=2023, month=6, day=1), datetime(year=2023, month=12, day=3))


if __name__ == '__main__':
    run_main()
