import csv


def import_names_from_file(import_type):

    companies_list = []
    filename = ''
    # test
    if import_type == 0:
        filename = 'test_companies.txt'
    # full
    if import_type == 1:
        filename = 'companies.txt'
    # owned for emails
    if import_type == 2:
        filename = 'companies_newconnect.txt'

    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in (list(reader)):
            companies_list.append(row[0])

    # print (companies_list)
    return companies_list

def import_email_and_companies():

    data_list = []
    filename = 'companies_owned.txt'

    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in (list(reader)):
            data_list.append(row)
    return data_list