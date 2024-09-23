from datetime import datetime

from filter_data import run_filter, get_missing_for_year, get_missing_for_range

def run_main():
    run_filter()
    get_missing_for_year(2023, 7)
    #get_missing_for_range(datetime(year=2023, month=7, day=1), datetime(year=2023, month=7, day=30))


if __name__ == '__main__':
    run_main()
