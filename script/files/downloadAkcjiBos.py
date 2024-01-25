import datetime as dt
import glob
import urllib.request
import os
import zipfile
import pandas as pd
import yfinance as yf

import ImportNamesFromFile
import ConfigFile

config_dict = ConfigFile.load_config()
seleniumfolder = config_dict['selenium_url']

def start():
    while True:
        main()
        break


def main():
    manage_download_all()  # bos
    manage_download_yahoo(4)  # nasdaq
    convert_temp_txt_yahoo_to_mst(4)
    manage_download_yahoo(5)  # dax
    convert_temp_txt_yahoo_to_mst(5)

def manage_download_all():
    filename = seleniumfolder + "ALL" + '.zip'
    # filename_2 = seleniumfolder + "TRYPLN" + '.csv'
    today = dt.datetime.now().date()
    if os.path.exists(filename):  # and os.path.exists(filename_2):
        filetime = dt.datetime.fromtimestamp(os.path.getmtime(filename))
        # filetime_2 = dt.datetime.fromtimestamp(os.path.getmtime(filename_2))
        if filetime.date() != today:
            os.remove(filename)
        # if filetime_2.date() != today:
        #     os.remove(filename_2)
        if filetime.date() == today:  # and filetime_2.date() == today:
            return

    fullfilename = os.path.join(seleniumfolder, "ALL" + '.zip')
    # fullfilename_2 = os.path.join(seleniumfolder, "TRYPLN" + '.csv')
    if not os.path.exists(seleniumfolder):
        os.makedirs(seleniumfolder)
        os.makedirs(seleniumfolder + "ALL")
    urllib.request.urlretrieve('http://bossa.pl/pub/metastock/mstock/mstall.zip', fullfilename)
    print("downloaded ALL")

    # urllib.request.urlretrieve('https://stooq.pl/q/d/l/?s=trypln&i=d', fullfilename_2)
    # print("downloaded TRYPLN")
    if os.path.exists(filename):
        zip_ref = zipfile.ZipFile(seleniumfolder + "ALL" + '.zip', 'r')
        zip_ref.extractall(seleniumfolder + "ALL")
        zip_ref.close()

def manage_download_yahoo(mode):

    companies_list = ImportNamesFromFile.import_names_from_file(mode)

    tempFolder = 'temp'
    if mode == 4:
        tempFolder = 'nasdaq_temp'
        print('Downloading NASDAQ companies')
    if mode == 5:
        tempFolder = 'dax_temp'
        print('Downloading DAX companies')

    if not os.path.exists(seleniumfolder + tempFolder):
        os.makedirs(seleniumfolder + tempFolder)

    i = 0

    for company in companies_list:

        tempCompanyFile = seleniumfolder + tempFolder + '/' + company + '_temp.csv'
        i += 1
        progress_bar(i, len(companies_list))

        today = dt.datetime.now().date()
        if os.path.exists(tempCompanyFile):
            filetime = dt.datetime.fromtimestamp(os.path.getmtime(tempCompanyFile))
            if filetime.date() != today:
                os.remove(tempCompanyFile)
            if filetime.date() == today:
                continue

        msft = yf.Ticker(company)

        # get historical market data
        hist = msft.history(period="5y")

        if not os.path.exists(seleniumfolder + tempFolder):
            os.makedirs(seleniumfolder + tempFolder)

        hist.to_csv(tempCompanyFile)

def progress_bar(current, total, bar_length=20):
    fraction = current / total

    arrow = int(fraction * bar_length - 1) * '-' + '>'
    padding = int(bar_length - len(arrow)) * ' '

    ending = '\n' if current == total else '\r'

    print(f'Progress: [{arrow}{padding}] {int(fraction*100)}%', end=ending)

def convert_temp_txt_yahoo_to_mst(mode):

    print('Converting txt to mst')
    tempPathString = seleniumfolder + 'temp'
    targetPathString = seleniumfolder + 'temp2'

    if mode == 4:
        # US
        print('NASDAQ')
        tempPathString = seleniumfolder + 'nasdaq_temp'
        targetPathString = seleniumfolder + "nasdaq"

    if mode == 5:
        # DAX
        print('DAX')
        tempPathString = seleniumfolder + 'dax_temp'
        targetPathString = seleniumfolder + "dax"

    if not os.path.exists(targetPathString):
        os.makedirs(targetPathString)

    for path in glob.glob(tempPathString + '/*.csv'):

        f = pd.read_csv(path)
        path = path.replace('_temp.csv', '')
        path = path.replace(tempPathString, targetPathString)

        today = dt.datetime.now().date()
        if os.path.exists(path + ".mst"):
            filetime = dt.datetime.fromtimestamp(os.path.getmtime(path + ".mst"))
            if filetime.date() != today:
                os.remove(path + ".mst")
            if filetime.date() == today:
                continue

        keep_col = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        new_f = f[keep_col]
        new_f = new_f.add_prefix('<')
        new_f = new_f.add_suffix('>')
        new_f.columns = new_f.columns.str.upper()
        new_f.columns = new_f.columns.str.replace('<DATE>', '<DTYYYYMMDD>')
        new_f.columns = new_f.columns.str.replace('<VOLUME>', '<VOL>')
        new_f.insert(0, '<TICKER>', os.path.basename(path))
        new_f['<DTYYYYMMDD>'] = new_f['<DTYYYYMMDD>'].str.replace('-', '').str.split(' ').str[0]
        new_f.to_csv(path + ".mst", index=False)

# def convert_txt_mst():
#
#     print('Converting txt to mst')
#     uk = 1
#     us = 1
#     if uk == 1:
#
#         print('LSE')
#         #UK
#         stooqPathString = 'd_uk_txt/data/daily/uk/lse stocks'
#         targetPathString = seleniumfolder + "lse"
#
#         if not os.path.exists(targetPathString):
#             os.makedirs(targetPathString)
#
#         for path in glob.glob(seleniumfolder + stooqPathString + '/*.txt'):
#             with open(path +'temp.csv', 'w') as csv_file:
#                 with open(path) as txt_file:
#                     txt = txt_file.read() + '\n'
#                     csv_file.write(txt)
#
#             if os.path.getsize(path+"temp.csv") > 100:
#
#                 f = pd.read_csv(path+"temp.csv")
#
#                 keep_col = ['<TICKER>', '<DATE>', '<OPEN>','<HIGH>','<LOW>','<CLOSE>','<VOL>']
#                 new_f = f[keep_col]
#                 path = path.replace('.uk.txt', '')
#                 path = path.replace(seleniumfolder + stooqPathString, targetPathString)
#                 new_f.to_csv(path + ".mst", index=False)
#
#     if us == 1:
#
#         print('NASDAQ')
#         #US
#         stooqPathString = 'd_us_txt/data/daily/us/nasdaq stocks'
#         targetPathString = seleniumfolder + "nasdaq"
#
#         if not os.path.exists(targetPathString):
#             os.makedirs(targetPathString)
#
#         for path in glob.glob(seleniumfolder + stooqPathString + '/*.txt'):
#             with open(path +'temp.csv', 'w') as csv_file:
#                 with open(path) as txt_file:
#                     txt = txt_file.read() + '\n'
#                     csv_file.write(txt)
#
#             if os.path.getsize(path+"temp.csv") > 100:
#
#                 f = pd.read_csv(path+"temp.csv")
#
#                 keep_col = ['<TICKER>', '<DATE>', '<OPEN>','<HIGH>','<LOW>','<CLOSE>','<VOL>']
#                 new_f = f[keep_col]
#                 path = path.replace('.us.txt', '')
#                 path = path.replace(seleniumfolder + stooqPathString, targetPathString)
#                 new_f.to_csv(path + ".mst", index=False)

start()
