import calendar
import csv
import json
from calendar import month
from copy import copy
from datetime import datetime, timedelta, date
from pathlib import Path
from typing import Optional

from consts import output_folder, process, missing_folder, input_folder

output_folder.mkdir(exist_ok=True)
process.mkdir(exist_ok=True)
missing_folder.mkdir(exist_ok=True)

global_state = {}
global_state_file = process / "state_l.json"
if global_state_file.exists():
    global_state = json.load(global_state_file.open())

global_state_dict = {}
global_state_dict_file = process / "state_d.json"
if global_state_dict_file.exists():
    global_state_dict = json.load(global_state_dict_file.open())

def create_state_for_year(year: int) -> list[list[list[bool]]]:
    state = []
    for month in range(1, 13):
        month_state = []
        state.append(month_state)
        for day in range(1, calendar.monthrange(year, month)[1]):
            month_state.append([False for _ in range(24)])
    return state

def create_dict_state_for_year(year: int) -> dict[str,dict[dict[str,bool]]]:
    state = {}
    for month in range(1, 13):
        m_str = date(year,month,1).strftime("%b").lower()
        month_state = state.setdefault(m_str, {})
        for day in range(1, calendar.monthrange(year, month)[1]):
            month_state.setdefault(day, {hour: False for hour in range(24)})
    return state

def run_filter():
    # ITERATE THROUGH ALL CSV FILES AND COLLECT THE EARLIERST FOR EACH HOUR
    collected_years = set()
    for csv_file in input_folder.glob("*/*.csv"):
        # COLLECT
        calendar_sorted_posts = {}
        reader = csv.DictReader(csv_file.open())
        for line in reader:
            # print(line)
            # print(line["发布时间"])
            dt = datetime.strptime(line["发布时间"], "%Y-%m-%d %H:%M")
            # print(dt.month, dt.day, dt.hour)
            c_year = calendar_sorted_posts.setdefault(dt.year, {})
            c_month = c_year.setdefault(dt.month, {})
            c_day = c_month.setdefault(dt.day, {})
            if dt.hour not in c_day:
                c_day[dt.hour] = (dt, line)
            elif dt < c_day[dt.hour][0]:
                c_day[dt.hour] = (dt, line)
            collected_years.add(dt.year)

        # create state list if the year is missing
        for year in collected_years:
            if str(year) not in global_state:
                global_state[str(year)] = create_state_for_year(year)
                global_state_dict[str(year)] = (create_dict_state_for_year(year))

        fieldnames = ["date", "hour"] + list(reader.fieldnames)
        writer = csv.DictWriter(output_folder.joinpath(csv_file.stem + "_auto_filtered.csv").open("w"), fieldnames)
        writer.writeheader()
        for year, year_data in sorted(calendar_sorted_posts.items()):
            for month, month_data in sorted(year_data.items()):
                # print(f"month: {month}")
                for day, day_data in sorted(month_data.items()):
                    # print(f"day: {day}")
                    for hour, hour_data in sorted(day_data.items()):
                        global_state[str(year)][month - 1][day - 1][hour] = True
                        print(f"hour: {hour}")
                        print(hour_data)
                        dt, post = hour_data
                        post["hour"] = hour
                        post["date"] = post["发布时间"]
                        writer.writerow(post)

    json.dump(global_state, global_state_file.open("w"))
    json.dump(global_state_dict, global_state_dict_file.open("w"))

def get_missing_for_year(year: int, month: Optional[int] = None) -> None:
    year_data = global_state[str(year)]
    for month_idx, month_data in enumerate(year_data):
        if month and month_idx + 1 != month:
            continue
        for day_idx, day_data in enumerate(month_data):
            for hour_idx, collected in enumerate(day_data):
                if not collected:
                    print(datetime(year, month_idx + 1, day_idx + 1).strftime("%Y-%m-%d %H:%M"))


def get_missing_for_range(start: datetime, end: datetime) -> None:
    years = list(y + start.year for y in range(end.year - start.year + 1))
    print(years)
    cur_dt = copy(start)
    while cur_dt <= end:
        cur_dt += timedelta(hours=1)
        if not global_state[str(cur_dt.year)][cur_dt.month - 1][cur_dt.day -1][cur_dt.hour]:
            print(cur_dt.strftime("%Y-%m-%d %H:%M"))


if __name__ == "__main__":
    run_filter()
    # get_missing_for_year(2023, 7)
    get_missing_for_range(datetime(year=2023, month=6, day=1), datetime(year=2023, month=12, day=3))
