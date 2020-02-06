import csv

def import_names_from_file(import_type):

    companies_list = []
    # test
    if import_type == 0:
        filename = 'test_companies.txt'
    # full
    if import_type == 1:
        filename = 'companies.txt'

    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in (list(reader)):
            companies_list.append(row)

    # print (companies_list)
    return companies_list
