import csv
import datetime as dt
import glob
import time
import urllib.request
import os
import zipfile
import pandas as pd
import yfinance as yf

from script.files import ImportNamesFromFile

seleniumfolder = 'C:/selenium/'


def start():
    while True:
        main()
        break


def main():
    manage_download_all()  # bos
    # manage_download_lse()
    # convert_temp_txt_yahoo_to_mst()
    # convert_txt_mst()

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

def manage_download_lse():

    companies_list = ImportNamesFromFile.import_names_from_file(4)
    if not os.path.exists(seleniumfolder + '/temp'):
        os.makedirs(seleniumfolder + '/temp')

    i = 0
    print('Downloading NASDAQ companies')
    for company in companies_list:
        i += 1
        print(f'Downloaded {i}/{len(companies_list)}')
        msft = yf.Ticker(company)

        # get historical market data
        hist = msft.history(period="1y")

        if not os.path.exists(seleniumfolder + '/temp'):
            os.makedirs(seleniumfolder + '/temp')
        hist.to_csv(seleniumfolder + '/temp/' + company + '_temp.txt')


def convert_temp_txt_yahoo_to_mst():

    print('Converting txt to mst')

    # us = 1
    # if us == 1:
    #
    #     print('NASDAQ')
    #     #US
    #     tempPathString = seleniumfolder + '/temp'
    #     targetPathString = seleniumfolder + "nasdaq"
    #
    #     if not os.path.exists(targetPathString):
    #         os.makedirs(targetPathString)
    #
    #     for path in glob.glob(tempPathString + '/*.txt'):
    #
    #         f = pd.read_csv(path+"temp.csv")
    #
    #         keep_col = ['<TICKER>', '<DATE>', '<OPEN>','<HIGH>','<LOW>','<CLOSE>','<VOL>']
    #         new_f = f[keep_col]
    #         path = path.replace('.us.txt', '')
    #         path = path.replace(seleniumfolder + stooqPathString, targetPathString)
    #         new_f.to_csv(path + ".mst", index=False)

def convert_txt_mst():

    print('Converting txt to mst')
    uk = 1
    us = 1
    if uk == 1:

        print('LSE')
        #UK
        stooqPathString = 'd_uk_txt/data/daily/uk/lse stocks'
        targetPathString = seleniumfolder + "lse"

        if not os.path.exists(targetPathString):
            os.makedirs(targetPathString)

        for path in glob.glob(seleniumfolder + stooqPathString + '/*.txt'):
            with open(path +'temp.csv', 'w') as csv_file:
                with open(path) as txt_file:
                    txt = txt_file.read() + '\n'
                    csv_file.write(txt)

            if os.path.getsize(path+"temp.csv") > 100:

                f = pd.read_csv(path+"temp.csv")

                keep_col = ['<TICKER>', '<DATE>', '<OPEN>','<HIGH>','<LOW>','<CLOSE>','<VOL>']
                new_f = f[keep_col]
                path = path.replace('.uk.txt', '')
                path = path.replace(seleniumfolder + stooqPathString, targetPathString)
                new_f.to_csv(path + ".mst", index=False)

    if us == 1:

        print('NASDAQ')
        #US
        stooqPathString = 'd_us_txt/data/daily/us/nasdaq stocks'
        targetPathString = seleniumfolder + "nasdaq"

        if not os.path.exists(targetPathString):
            os.makedirs(targetPathString)

        for path in glob.glob(seleniumfolder + stooqPathString + '/*.txt'):
            with open(path +'temp.csv', 'w') as csv_file:
                with open(path) as txt_file:
                    txt = txt_file.read() + '\n'
                    csv_file.write(txt)

            if os.path.getsize(path+"temp.csv") > 100:

                f = pd.read_csv(path+"temp.csv")

                keep_col = ['<TICKER>', '<DATE>', '<OPEN>','<HIGH>','<LOW>','<CLOSE>','<VOL>']
                new_f = f[keep_col]
                path = path.replace('.us.txt', '')
                path = path.replace(seleniumfolder + stooqPathString, targetPathString)
                new_f.to_csv(path + ".mst", index=False)

start()
