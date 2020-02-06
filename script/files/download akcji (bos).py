import datetime as dt
import urllib.request
import os
import zipfile

seleniumfolder = 'C:/selenium/'


def start():
    while True:
        main()
        break


def main():
    manage_download_all()  # bos


def manage_download_all():
    filename = seleniumfolder + "ALL" + '.zip'
    filename_2 = seleniumfolder + "TRYPLN" + '.csv'
    today = dt.datetime.now().date()
    if os.path.exists(filename) and os.path.exists(filename_2):
        filetime = dt.datetime.fromtimestamp(os.path.getmtime(filename))
        filetime_2 = dt.datetime.fromtimestamp(os.path.getmtime(filename_2))
        if filetime.date() != today:
            os.remove(filename)
        if filetime_2.date() != today:
            os.remove(filename_2)
        if filetime.date() == today and filetime_2.date() == today:
            return

    fullfilename = os.path.join(seleniumfolder, "ALL" + '.zip')
    fullfilename_2 = os.path.join(seleniumfolder, "TRYPLN" + '.csv')
    if not os.path.exists(seleniumfolder):
        os.makedirs(seleniumfolder)
        os.makedirs(seleniumfolder + "ALL")
    urllib.request.urlretrieve('http://bossa.pl/pub/metastock/mstock/mstall.zip', fullfilename)
    print("downloaded ALL")

    urllib.request.urlretrieve('https://stooq.pl/q/d/l/?s=trypln&i=d', fullfilename_2)
    print("downloaded TRYPLN")
    if os.path.exists(filename):
        zip_ref = zipfile.ZipFile(seleniumfolder + "ALL" + '.zip', 'r')
        zip_ref.extractall(seleniumfolder + "ALL")
        zip_ref.close()


start()
