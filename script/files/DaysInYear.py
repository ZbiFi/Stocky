import datetime as dt
from script.files import ConfigFile


def days_in_year(super_data):
    # Active days of company on stock

    config_dict = ConfigFile.load_config()
    year_time_lapse = int(config_dict['one_year_span'])

    today_string = str(dt.datetime.now().date()).replace("-", "")

    for i in range(len(super_data)):
        if(int(today_string)-year_time_lapse) > int(super_data[i][1]):
            days_in_year = i
            break


    return days_in_year
