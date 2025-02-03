import datetime as dt
import csv
import ConfigFile
from os.path import exists


def import_data_from_file(company_name, mode, day_param):

    # print(company_name)
    config_dict = ConfigFile.load_config()

    selenium_url = config_dict['selenium_url']
    two_year_span = int(config_dict['two_year_span'])
    offset = int(config_dict['offset'])
    super_data = []
    i = 0

    today_string = str(dt.datetime.now().date()).replace("-", "")

    if mode == 3:
        root = 'lse'
    elif mode == 4:
        root = 'nasdaq'
    elif mode == 5:
        root = 'dax'
    else:
        root = 'ALL'

    filename = selenium_url + root + '/'+company_name+'.mst'  # BOS data

    if exists(filename):
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            super_data.clear()
            f.readline()

            for row in reversed(list(reader)):
                if row[2] == '' or row[3] == '' or row[4] == '' or row[5] == '':
                    continue
                if (int(row[1]) >= int(today_string) - two_year_span - offset - day_param) and int(row[1]) <= (int(today_string) - offset - day_param):
                    super_data.append(row)
                    i += 1
                if (int(row[1]) < int(today_string) - two_year_span - offset - day_param):
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
