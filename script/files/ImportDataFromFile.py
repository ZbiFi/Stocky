import datetime as dt
import csv
import ConfigFile
from os.path import exists


def import_data_from_file(company_name):

    # print(company_name)
    config_dict = ConfigFile.load_config()

    selenium_url = config_dict['selenium_url']
    two_year_span = int(config_dict['two_year_span'])
    offset = int(config_dict['offset'])
    super_data = []
    i = 0

    today_string = str(dt.datetime.now().date()).replace("-", "")

    filename = selenium_url + 'ALL/'+company_name+'.mst'  # BOS data

    if exists(filename):
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            super_data.clear()
            f.readline()

            for row in reversed(list(reader)):
                if (int(row[1]) >= int(today_string) - two_year_span - offset) and int(row[1]) <= (int(today_string) - offset):
                    super_data.append(row)
                    i += 1
                if (int(row[1]) < int(today_string) - two_year_span - offset):
                    break
                else:
                    continue

        # converting data to float
        for i in range(len(super_data)):
            for j in range(1, len(super_data[i])):
                super_data[i][j] = float(super_data[i][j])

        return super_data

    else:

        print(f' {company_name} is no longer is being traded/watched')
        return []

# import_data_from_file('BENEFIT')
