import csv


def load_config():

    config_dict = {}
    filename = 'config.txt'

    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in (list(reader)):
            config_dict[row[0]] = row[1]

    #print (config_dict)
    return config_dict


def load_password():

    credentials = []
    filename = 'password.txt' #create file and add in first line senderemail; password; targetemail

    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in (list(reader)):
            credentials.append(row[0])

    #print (config_dict)
    return credentials
