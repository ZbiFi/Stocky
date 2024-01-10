import datetime as dt
from script.files import ConfigFile


def daysInYear(super_data):
    # Active days of company on stock

    config_dict = ConfigFile.load_config()
    year_time_lapse = int(config_dict['one_year_span'])
    offset = int(config_dict['offset'])
    days_in_year = 0
    today_string = str(dt.datetime.now().date()).replace("-", "")

    for i in range(len(super_data)):
        if(int(today_string)-year_time_lapse-offset) > int(super_data[i][1]):
            days_in_year = i
            break

    return days_in_year
