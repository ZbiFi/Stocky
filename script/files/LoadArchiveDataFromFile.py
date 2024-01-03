import csv


def loadArchiveDataFromFile(import_type=0):

    archiveData = []
    archiveDataRow = []
    filename = ''
    # test
    if import_type == 0:
        filename = 'output.csv'
    # full
    if import_type == 1:
        filename = 'output.csv'

    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in (list(reader)):
            archiveDataRow = row
            archiveData.append(archiveDataRow)

    return archiveData
