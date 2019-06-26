import time
import datetime as dt
import smtplib
import requests
import csv
import sys
import urllib.request
import os
import zipfile
import pandas as pd
from datetime import timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

super_data = []
price_channel = []
#super_data = [10,20,20,20,10,20,10,30,10,10,10,20,20,15,10,20,10]
#super_data = [1,2,1,2,3,2,3,4,3,4,5,4,5,6,5,6,7]
#https://stooq.pl/q/d/l/?s=alr&i=d - link do sciągniecia
#super_data = [7,6,7,6,5,6,5,4,5,4,3,4,3,2,3,2,1]
#time laps and block_size (stock days per stock days in time laps) and block_step
#5 stock days = 1 week      [1]     {1}     20% (rozmiar bloku) 20% (5)-liczba bloków
#10 stock days = 2 weeks    [1]     {1}     10% (rozmiar bloku) 10% (10)-liczba bloków
#20 stock days = 1 month    [2]1     {1}1     10% (rozmiar bloku) 5%  (20)-liczba bloków
#60 stock days = 3 months   [10]2    {2}1     16% (rozmiar bloku) 3,3%(33)-liczba bloków
#90 stock days = 6 months   [15]3    {3}1     16% (rozmiar bloku) 3,3%(33)-liczba bloków
#180stock days = 1 year     [30]6    {5}1     16% (rozmiar bloku) 2,7%(36)-liczba bloków
#540stock days = 3 years    [90]18    {15}3    16% (rozmiar bloku) 2,7%(36)-liczba bloków
#900stock days = 5 years    [150]30   {25}5    16% (rozmiar bloku) 2,7%(36)-liczba bloków
#1800stock days = 10 years  [300]60   {50}10    16% (rozmiar bloku) 2,7%(36)-liczba bloków

#HOW TO CHECK -> MUST: liczba calkowita <- (lime_lapse-stock_days)/block_step

#time_laps = [5,10,20,30,]
#block_size = [1,1,1,1,]
#block_size_list=[1,1,2,10,15,30,90,150,300]
block_size_list=[1,1,1,2,3,6,18,30,60]
#step_list=[1,1,1,2,3,5,15,25,50]
step_list=[1,1,1,1,1,1,3,5,10]
index_list = ["WIG20","WIG30","mWIG40","sWIG80","ALL"]
time_list=[[5,"1 week"],[10,"2 weeks"],[20,"1 month"],[60,"3 months"],[90,"6 months"],[180,"1 year"],[540,"3 years"],[900,"5 years"],[1800,"10 years"]]
company_name=[["HYDROTOR", "HDR", ""],["VIVID","VVD", ""], ["DECORA","DCR", ""],
              ["AMICA","AMC","mWIG40"],["BUDIMEX","BDX","mWIG40"],["BENEFIT","BFT","mWIG40"],["HANDLOWY","BHW","mWIG40"],["BORYSZEW","BRS","mWIG40"],["INTERCARS","CAR","mWIG40"],["CIECH","CIE","mWIG40"],["CIGAMES","CIG","mWIG40"],["COMARCH","CMR","mWIG40"],["AMREST","EAT","mWIG40"],["FAMUR","FMF","mWIG40"],["FORTE","FTE","mWIG40"],["GETINOBLE","GNB","mWIG40"],["GPW","GPW","mWIG40"],["GTC","GTC","mWIG40"],["KETY","KTY","mWIG40"],["LCCORP","LCC","mWIG40"],["LIVECHAT","LVC","mWIG40"],["BOGDANKA","LWB","mWIG40"],["MABION","MAB","mWIG40"],["MEDICALG","MDG","mWIG40"],["NETIA","NET","mWIG40"],["ORBIS","ORB","mWIG40"],["PFLEIDER","PFL","mWIG40"],["POLIMEXMS","PXM","mWIG40"],["SANOK","SNK","mWIG40"],["STALPROD","STP","mWIG40"],["URSUS","URS","mWIG40"],["WIRTUALNA","WPL","mWIG40"],["WAWEL","WWL","mWIG40"],
              ["ALIOR", "ALR", "WIG20"],
              #["BZWBK", "BZW", "WIG20"],
              ["CCC", "CCC", "WIG20"],["CDPROJEKT","CDR", "WIG20"],["CYFRPLSAT","CPS","WIG20"],["ENERGA","ENG","WIG20"],["EUROCASH","EUR","WIG20"],["JSW","JSW","WIG20"],["KGHM","KGH","WIG20"],["LPP","LPP","WIG20"],["LOTOS","LTS","WIG20"],["MBANK","MBK","WIG20"],["ORANGEPL","OPL","WIG20"],["PEKAO","PEO","WIG20"],["PGE","PGE","WIG20"],["PGNIG","PGN","WIG20"],["PKNORLEN","PKN","WIG20"],["PKOBP","PKO","WIG20"],["PZU","PZU","WIG20"],["TAURONPE","TPE","WIG20"],
              ["ASSECOPOL","ACP","WIG30"],["GRUPAAZOTY","ATT","WIG30"],["DINOPL","DNP","WIG30"],["ENEA","ENA","WIG30"],["INGBSK","ING","WIG30"],["KERNEL","KER","WIG30"],["KRUK","KRU","WIG30"],["MILLENNIUM","MIL","WIG30"],["PKPCARGO","PKP","WIG30"],["PLAY","PLY","WIG30"],
              ["KREZUS", "KZS", "sWIG80"], ["BOS", "BOS", "sWIG80"], ["ECHO", "ECH", "sWIG80"], ["SKARBIEC", "SKH", "sWIG80"],["MENNICA","MNC", ""],["PGSSOFT","PSW", ""],["IDEABANK","PSW", ""]]

favorite=[["BOS", "BOS", "sWIG80"], ["CIGAMES","CIG","mWIG40"], ["DECORA","DCR", ""], ["ECHO", "ECH", "sWIG80"], ["EUROCASH","EUR","WIG20"], ["GETINOBLE","GNB","mWIG40"], ["KGHM","KGH","WIG20"], ["KREZUS", "KZS", "sWIG80"], ["SKARBIEC", "SKH", "sWIG80"], ["VIVID","VVD", ""]] 
all_companies = []
interesting_companies = []
under_price_channel = []
in_price_channel = []
over_price_channel = []

def start():
    while True:
        main()
        #return

def main ():

    company_symbol = "";
    block_size = 0;
    block_step = 0;
    time_lapse = 0;
    temp_list=[];
    auto=0;
    
    print("Please choose analysis option:")
    print ("(1) 1 company on 1 period")
    print ("(2) All companies on 1 period (1 years)")
    print ("(3) All companies on all periods")

    choice = input()

    if choice in {"1","2","3"}:
        auto = int(choice)-1
    else:
        print("FDUCK YOU !!!! PANDA NOT APPROVE \o\   \o/   /o/")
        return
    
    
    if (auto==0):#Jedna spolka; jeden okres
        company_symbol_spec=""
        company_symbol,block_size,block_step,time_lapse = menu()
        for i in range(len(company_name)):
            #print(company_symbol.upper(),company_name[i][1])
            if (company_symbol.upper()==company_name[i][1]):
                company_name_spec=company_name[i][0]
                #print("True")
        print (block_size,block_step,time_lapse)
        manage_download_all() #bos
        #manage_download(company_symbol) #stooq
        import_data_from_file(time_lapse,company_symbol,company_name_spec)
        #print("2222")
        #print (super_data[0][1])
        generating_raports(company_symbol,block_size,block_step,time_lapse,auto)
        #generate_raport_to_file(company_symbol,block_size,block_step,time_lapse)
        #print("23232323")
        #generate_output_raport(company_symbol,block_size,block_step,time_lapse,auto)
        negerate_interesting_companies_to_file()
    #print (company_symbol)
    
    elif(auto==1):#Wszystkie spolki; jeden okres (1 year)
        for i in range(len(company_name)):
        #for i in range(2):
            company_symbol = company_name[i][1]
            print(company_symbol, company_name[i][0])
            block_size=6#30
            block_step=1#5
            time_lapse=180#180
            manage_download_all() #bos
            #manage_download(company_symbol) #stooq
            import_data_from_file(time_lapse,company_symbol,company_name[i][0])
            #print (super_data[0][1])
            generating_raports(company_symbol,block_size,block_step,time_lapse,auto)
            #print (super_data[0][1])
            #generate_raport_to_file(company_symbol,block_size,block_step,time_lapse)
            #generate_output_raport(company_symbol,block_size,block_step,time_lapse,auto)
            negerate_interesting_companies_to_file()
            print(i)
        #terminate()
    elif(auto==2):#Wszystkie spolki; wszystkie okresy
        j=0
        for i in range(len(company_name)):
            j+=1
            #print ("(",j,")",company_name[i][0],"-",company_name[i][1])
            #temp_list.append(company_name[i][1])
            company_symbol = (company_name[i][1]).lower()
            #company_symbol = "vvd"
            #print(company_symbol)
            for k in range(len(time_list)):
            #for k in range(6):
                block_size=block_size_list[k]
                block_step=step_list[k]
                time_lapse=time_list[k][0]
                print(block_size,block_step,time_lapse,company_symbol)
                manage_download_all() #bos
                #manage_download(company_symbol) #stooq
                import_data_from_file(time_lapse,company_symbol,company_name[i][0])
                generating_raports(company_symbol,block_size,block_step,time_lapse,auto)
                #generate_raport_to_file(company_symbol,block_size,block_step,time_lapse)
                #generate_output_raport(company_symbol,block_size,block_step,time_lapse,auto)
                negerate_interesting_companies_to_file()
            print(i)
            #break
            
    print("UP UP's: ")
    for i in range(len(interesting_companies)):
        print(interesting_companies[i])
    print("Under Price channel: ")
    for i in range(len(under_price_channel)):
        print(under_price_channel[i][0]," Lower:" ,"{0:.2f}".format(under_price_channel[i][1]), " Now: ", under_price_channel[i][2], " Perc under" , "{0:.2f}".format(100-(under_price_channel[i][2]/under_price_channel[i][1])*100))
    print("In Price channel: ")
    for i in range(len(in_price_channel)):
        print(in_price_channel[i][0]," Lower:" ,"{0:.2f}".format(in_price_channel[i][1])," Higher:" ,"{0:.2f}".format(in_price_channel[i][2]), " Now: ", in_price_channel[i][3], " Avg channel price: ", "{0:.2f}".format((in_price_channel[i][2]+in_price_channel[i][1])/2), " Perc under/over avg channel:" , "{0:.2f}".format(in_price_channel[i][3]/((in_price_channel[i][2]+in_price_channel[i][1])/2)))
    print("Over Price channel: ")
    for i in range(len(over_price_channel)):
        print(over_price_channel[i][0]," Higher:" ,"{0:.2f}".format(over_price_channel[i][1]), " Now: ", over_price_channel[i][2], " Perc over" , "{0:.2f}".format(((over_price_channel[i][2]/over_price_channel[i][1])*100)-100))
    #print(price_channel)
    interesting_companies.clear()
    #print(price_channel)
    price_channel.clear()
    under_price_channel.clear()
    in_price_channel.clear()
    over_price_channel.clear()
    #print("ech")
    #stooq_logging(company_symbol,time_lapse)
    #analyze_data(block_size,block_step,"volume")
    #analyze_data(block_size,block_step,"end_price")
    #generate_raport_to_file(company_symbol,block_size,block_step,time_lapse)
    #generate_output_raport(company_symbol,block_size,block_step,time_lapse)
    #analyze_price()
    #print (super_data)



def menu ():
    company = 0;
    block_size = 0;
    block_step = 0;
    time_laps = 0;
    #block_choices = {'1': 1,'2': 1,'3': 2,'4': 10,'5': 15,'6': 30,'7': 90,'8': 150,'9': 300}
    block_choices = {'1': 1,'2': 1,'3': 1,'4': 2,'5': 3,'6': 6,'7': 18,'8': 30,'9': 60}
    time_choices = {'1': "5",'2': "10",'3': "20",'4': "60",'5': "90",'6': "180",'7': "540",'8': "900",'9': "1800"}
    #block_steps = {'1': 1,'2': 1,'3': 1,'4': 2,'5': 3,'6': 5,'7': 15,'8': 25,'9': 50}
    block_steps = {'1': 1,'2': 1,'3': 1,'4': 1,'5': 1,'6': 1,'7': 3,'8': 5,'9': 10}
    #company_shortcuts = {'1': "hdr",'2': "alr",'3': "bzw",'4': "ccc",'5': "cdr",'6': "cps",'7': "eng",'8': "eur",'9': "jsw",'10': "kgh",'11': "lpp",'12': "lts",'13': "mbk",'14': "opl",'15': "peo",'16': "pge",'17': "pgn",'18': "pkn",'19': "pko",'20': "pzu",'21': "tpe"}
    #index_list = ["WIG20","WIG30","mWIG40","sWIG80","ALL"]
    company_symbol = "";
    index = ""
    temp_list = []
#    company_name=[["HYDROTOR", "HDR", "mWIG40"],["ALIOR", "ALR", "WIG20"],["BZWBK", "BZW", "WIG20"],["CCC", "CCC", "WIG20"],["CDPROJEKT","CDR", "WIG20"],["CYFRPLSAT","CPS","WIG20"],["ENERGA","ENG","WIG20"],["EUROCASH","EUR","WIG20"],["JSW","JSW","WIG20"],["KGHM","KGH","WIG20"],["LPP","LPP","WIG20"],["LOTOS","LTS","WIG20"],["MBANK","MBK","WIG20"],["ORANGEPL","OPL","WIG20"],["PEKAO","PEO","WIG20"],["PGE","PGE","WIG20"],["PGNIG","PGN","WIG20"],["PKNORLEN","PKN","WIG20"],["PKOBP","PKO","WIG20"],["PZU","PZU","WIG20"],["TAURONPE","TPE","WIG20"],["ASSECOPOL","ACP","WIG30"],["GRUPAAZOTY","ATT","WIG30"],["DINOPL","DNP","WIG30"],["ENEA","ENA","WIG30"],["INGBSK","ING","WIG30"],["KERNEL","KER","WIG30"],["KRUK","KRU","WIG30"],["MILLENNIUM","MIL","WIG30"],["PKPCARGO","PKP","WIG30"],["PLAY","PLY","WIG30"]]
    #company_name

    for i in range(len (index_list)):
        print ("(",i+1,")",index_list[i])

    index_choice = input()
    #if (index_list[int(index_choice)-1]=="WIG20"):
    #    j=0
    #    for i in range(len (company_name)):
    #        if (company_name[i][2]==index_list[int(index_choice)-1]):
    #            j+=1
    #            print ("(",j,")",company_name[i][0],"-",company_name[i][1])

    temp_list = (menu_index_choice(index_choice))
##    if ((index_list[int(index_choice)-1]=="WIG30") or (index_list[int(index_choice)-1]=="WIG20")):
##        j=0
##        for i in range(len (company_name)):
##            if ((company_name[i][2]==index_list[int(index_choice)-1]) or (company_name[i][2]==index_list[int(index_choice)-2])):
##                j+=1
##                print ("(",j,")",company_name[i][0],"-",company_name[i][1])
##                temp_list.append(company_name[i][1])
##                #company_symbol = company_name[i][1].lower()
##
##    if ((index_list[int(index_choice)-1]=="mWIG40") or (index_list[int(index_choice)-1]=="WIG30")):
##        j=0
##        for i in range(len (company_name)):
##            if ((company_name[i][2]==index_list[int(index_choice)-1]) or (company_name[i][2]==index_list[int(index_choice)-2])):
##                j+=1
##                print ("(",j,")",company_name[i][0],"-",company_name[i][1])
##                temp_list.append(company_name[i][1])
##                #print (temp_list)
##                #company_symbol = company_name[i][1].lower()
##    if (index_list[int(index_choice)-1]=="ALL"):
##        j=0
##        for i in range(len (company_name)):
##            j+=1
##            print ("(",j,")",company_name[i][0],"-",company_name[i][1])
##            temp_list.append(company_name[i][1])

    company = int(input())
    
    #print (temp_list)
    company_symbol = (str(temp_list[company-1])).lower()
    #print (company_symbol)
    #company_symbol = company_shortcuts.get(company,'0')
    
    print ("Select timelapse:")

    for i in range(len(time_list)):
        print("(",i+1,")",time_list[i][1])

##    print ("(1) 1 week")
##    print ("(2) 2 weeks")
##    print ("(3) 1 month")
##    print ("(4) 3 months")
##    print ("(5) 6 months")
##    print ("(6) 1 year")
##    print ("(7) 3 years")
##    print ("(8) 5 years")
##    print ("(9) 10 years")

    choice = input()
    block_size = block_choices.get(choice,'0')
    block_step = block_steps.get(choice,'0')
    time_laps = time_choices.get(choice,'0')

    #print ('SIZE: ', block_size, ' Step: ', block_step, ' Symbol: ', company_symbol)

    return (company_symbol,block_size,block_step,time_laps)

def menu_index_choice(index_choice):

    temp_list=[]

    if ((index_list[int(index_choice)-1]=="WIG30") or (index_list[int(index_choice)-1]=="WIG20")):
        j=0
        for i in range(len (company_name)):
            if ((company_name[i][2]==index_list[int(index_choice)-1]) or (company_name[i][2]==index_list[int(index_choice)-2])):
                j+=1
                print ("(",j,")",company_name[i][0],"-",company_name[i][1])
                temp_list.append(company_name[i][1])
                #company_symbol = company_name[i][1].lower()
        return temp_list

    if ((index_list[int(index_choice)-1]=="mWIG40") or (index_list[int(index_choice)-1]=="WIG30")):
        j=0
        for i in range(len (company_name)):
            if ((company_name[i][2]==index_list[int(index_choice)-1]) or (company_name[i][2]==index_list[int(index_choice)-2])):
                j+=1
                print ("(",j,")",company_name[i][0],"-",company_name[i][1])
                temp_list.append(company_name[i][1])
        return temp_list
                #print (temp_list)
                #company_symbol = company_name[i][1].lower()
    if (index_list[int(index_choice)-1]=="ALL"):
        j=0
        for i in range(len (company_name)):
            j+=1
            print ("(",j,")",company_name[i][0],"-",company_name[i][1])
            temp_list.append(company_name[i][1])
        return temp_list
    return


def manage_download_all():

    filename = 'C:/selenium/' + "ALL" + '.zip'
    filename_2 = 'C:/selenium/' + "TRYPLN" + '.csv'
    today = dt.datetime.now().date()
    if os.path.exists(filename) and os.path.exists(filename_2):
        filetime= dt.datetime.fromtimestamp(os.path.getmtime(filename))
        filetime_2= dt.datetime.fromtimestamp(os.path.getmtime(filename_2))
        if filetime.date() != today:
            os.remove(filename)
        if filetime_2.date() != today:
            os.remove(filename_2)
        if filetime.date() == today and filetime_2.date() == today:
            #if os.path.exists(filename) :
            #    zip_ref = zipfile.ZipFile('C:/selenium/' + "ALL" + '.zip', 'r')
            #    zip_ref.extractall('C:/selenium/' + "ALL")
            #    zip_ref.close()
            return;

    fullfilename = os.path.join('C:/selenium/', "ALL" + '.zip')
    fullfilename_2 = os.path.join('C:/selenium/', "TRYPLN" + '.csv')
    urllib.request.urlretrieve('http://bossa.pl/pub/metastock/mstock/mstall.zip', fullfilename)
    print("downloaded ALL")
    urllib.request.urlretrieve('https://stooq.pl/q/d/l/?s=trypln&i=d', fullfilename_2)
    print("downloaded TRYPLN")
    if os.path.exists(filename) :
        zip_ref = zipfile.ZipFile('C:/selenium/' + "ALL" + '.zip', 'r')
        zip_ref.extractall('C:/selenium/' + "ALL")
        zip_ref.close()



def manage_download(company_symbol):

    filename = 'C:/selenium/' + company_symbol + '.csv'

    today = dt.datetime.now().date()
    #print ("dupaduapduapaduap",filename)
    #company_symbol=company_symbol.lower()
    #print (filename,today)
    if os.path.exists(filename) :
        filetime= dt.datetime.fromtimestamp(os.path.getmtime(filename))
        #print(filename,today,filetime.date())
        ##if filetime.date() != today:   #######!!!!! wylaczenie ## sprawdzania aktualnej daty
            #print("False")
        ##    os.remove(filename)    #######!!!!! wylaczenie #

        ##if filetime.date() == today:      #######!!!!! wylaczenie #
        if filetime.date() != "":
            #print("TRUE")
            return;

    fullfilename = os.path.join('C:/selenium/', company_symbol.upper() + '.csv')
    #print(company_symbol)
    #https://www.megaproxy.com/go/https://stooq.pl/q/d/l/?s=hdr&i=d
    #proxy_prefix = "https://www.megaproxy.com/go/"

    urllib.request.urlretrieve('https://stooq.pl/q/d/l/?s='+company_symbol+'&i=d', fullfilename)

    #print(proxy_prefix + 'https://stooq.pl/q/d/l/?s='+company_symbol+'&i=d', fullfilename)
   
    #urllib.request.urlretrieve(proxy_prefix + 'https://stooq.pl/q/d/l/?s='+company_symbol+'&i=d', fullfilename)
    #time.sleep(.5)
    print(company_symbol,"downloaded")

def generating_raports(company_symbol,block_size,block_step,time_lapse,auto):

    #generate_raport_to_file(company_symbol,block_size,block_step,time_lapse)
    generate_output_raport(company_symbol,block_size,block_step,time_lapse,auto)
    
    return
    

def generate_raport_to_file(company_symbol,block_size,block_step,time_lapse,list_of_data_for_log):

    previous_id = 1
    filename = 'C:/selenium/raport.csv'
    if os.path.exists(filename):
        previous_id=int(read_previous_raport())
        previous_id+=1
    append_new_raport(previous_id,company_symbol,block_size,block_step,time_lapse,list_of_data_for_log)
    
def append_new_raport(previous_id,company_symbol,block_size,block_step,time_lapse,list_of_data_for_log):

    filename = 'C:/selenium/raport.csv'
    #print ('dupa')
    
    with open(filename,'a', newline='') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow ([str(previous_id), "COMPANY: ", company_symbol, "TIME LAPSE ",time_lapse, list_of_data_for_log])

def generate_output_raport(company_symbol,block_size,block_step,time_lapse,auto):

    risk = ""
    value = 0
    list_of_data_for_log=[]

    end_price_data_string_2,end_price_change,end_price_flow,end_price_trend,end_price_data,end_price_percentage_string,end_price_percentage,min_val,max_val,last_val = analyze_data(company_symbol,block_size,block_step,"end_price",time_lapse)
    volume_data_string_2,volume_change,volume_flow,volume_trend,volume_data,volume_percentage_string,volume_percentage,min_vol,max_vol,last_vol = analyze_data(company_symbol,block_size,block_step,"volume",time_lapse)


    list_of_data_for_log.append(volume_data_string_2)
    list_of_data_for_log.append(volume_change)
    list_of_data_for_log.append(volume_flow)
    list_of_data_for_log.append(volume_trend)
    list_of_data_for_log.append(volume_data)
    list_of_data_for_log.append(volume_percentage_string)
    list_of_data_for_log.append(volume_percentage)
    list_of_data_for_log.append(end_price_data_string_2)
    list_of_data_for_log.append(end_price_change)
    list_of_data_for_log.append(end_price_flow)
    list_of_data_for_log.append(end_price_trend)
    list_of_data_for_log.append(end_price_data)
    list_of_data_for_log.append(end_price_percentage_string)
    list_of_data_for_log.append(end_price_percentage)

    #print (volume,price,auto)
    #print (list_of_data_for_log)                  
    marker = ""
    for i in range (len(time_list)):
        #print ("marker2") 
        if (str(time_list[i][0]) == str(time_lapse)):
            #print ("marker")        
            marker = str(time_list[i][1])
    #print (marker)

    if (last_val/max_val>=90/100):
        risk="LOW"
        value_from_top=float(100-(last_val/max_val*100))
    if (last_val/max_val<90/100) and (last_val/max_val>=70/100):
        risk="MEDIUM"
        value_from_top=float(100-(last_val/max_val*100))
    if (last_val/max_val<70/100) and (last_val/max_val>=60/100):
        risk="HIGH"
        value_from_top=float(100-(last_val/max_val*100))
    if (last_val/max_val<60/100):
        risk="VERY HIGH"
        value_from_top=float(100-(last_val/max_val*100))

    #print("adadadadadadadadad",price_channel)

        
    if (volume_flow=="UP" and end_price_flow =="UP"):
        interesting_companies.append([company_symbol.upper(),marker.upper(),risk,value_from_top])
        price_channel[len(price_channel)-1].append(["RISK:",risk,"VALUE FROM TOP:",value_from_top])

    generate_raport_to_file(company_symbol,block_size,block_step,time_lapse,list_of_data_for_log)
    
    filename = 'C:/selenium/SuperRaport.txt'
    with open(filename,'w', newline='') as f:
        writer = csv.writer(f, delimiter=' ')
        writer.writerow ("********************")
        writer.writerow ("*!*SUPER*!*RAPORT*!*")
        writer.writerow ("********************")
        writer.writerow (["* * * * * * * * * * * ",company_symbol.upper()," * *"])
        writer.writerow ("********************")
        writer.writerow (["* * P E R I O D : * * ",marker.upper()," * *"])
        writer.writerow ("********************")
        writer.writerow ("*!*!*!*VOLUME*!*!*!*")
        if (volume_flow=="UP"):
            writer.writerow ("*********UP*********")
        elif(volume_flow=="DOWN"):
            writer.writerow ("********DOWN********")
        else:
            writer.writerow ("******SIDE******")
        writer.writerow ("*!*!*!*PRICE*!*!*!**")
        if (end_price_flow=="UP"):
            writer.writerow ("*********UP*********")
        elif(end_price_flow=="DOWN"):
            writer.writerow ("********DOWN********")
        else:
            writer.writerow ("******SIDE******")
        writer.writerow ("!!!!!!!!!!!!!!!!!!!!")
        writer.writerow ("********************")

    today = dt.datetime.now().date()
    filename = 'C:/selenium/PriceChannelReport' + str(today) + '.txt'
    #filename = 'C:/selenium/PriceChannelReport' + 'Asss' + '.txt'
    with open(filename,'w', newline='') as f:
        writer = csv.writer(f, delimiter=',')
        for i in range(len(price_channel)):
            #print(price_channel[i])
            writer.writerow (price_channel[i])

##    if (auto==0):
##        filename = 'C:/selenium/SingleCompanyRaport.txt'
##        with open(filename,'w', newline='') as f:
##            writer = csv.writer(f, delimiter=' ')
##            for i in range(len(price_channel)):
##                writer.writerow ([price_channel[i], 'VOLUME TREND:',volume_flow, 'PRICE TREND:', end_price_flow, 'RISK:',risk])
    
    return

def negerate_interesting_companies_to_file():

    filename = 'C:/selenium/interesting_raport.txt'
    if os.path.exists(filename):
        os.remove(filename)
        
    with open(filename,'w', newline='') as f:
    
        writer = csv.writer(f, delimiter=' ')
        for i in range(len(interesting_companies)):
            writer.writerow(interesting_companies[i])
    return

def read_previous_raport ():

    filename = 'C:/selenium/raport.csv'
    previous_id= 0
    temp_list = []
    with open(filename,'r') as f:
        reader =csv.reader(f)
        for row in reversed(list(reader)):
            temp_list.append(row)
            break
            #previous_id = list(reader)[row][0]
    #print (temp_list)
    previous_id = temp_list[0][0]
    return previous_id

def stooq_logging (comp_shortcut,time_lapse):

    time = time_lapse
    company_shortcut = str(comp_shortcut)
    stooq_url = "https://stooq.pl"
    history_url = "/q/d/?s="
    #company_shortcut  = "hdr"
    basic_url = stooq_url+history_url+company_shortcut
    
    stooq_download_url= "https://stooq.pl/q/d/l/?s="
    stooq_download_company_url = company_shortcut
    stooq_download_end_url = "&i=d"
    proxy_prefix = "https://www.megaproxy.com/go/_mp_framed?"
    #download_url = proxy_prefix + stooq_download_url + stooq_download_company_url + stooq_download_end_url
    download_url = stooq_download_url + stooq_download_company_url + stooq_download_end_url

    driver = webdriver.Chrome("C:/Users/zfietkiewicz/Downloads/chromedriver_win32/chromedriver.exe")
    #driver = webdriver.Firefox()

    #driver.get(basic_url)
    #import_all_data_from_page(driver,basic_url)
    driver.get(download_url)
    #r = requests.get(download_url)
    #open('_data.csv', 'wb').write(r.content)


def reading_max_page_stooq(driver):

    max_page_button = driver.find_element_by_partial_link_text('>>')
    href_max_page = max_page_button.get_attribute('href')
    max_page = href_max_page[href_max_page.find("=d&l=")+5:]

    return max_page

def import_data_from_file(time_lapse,company_symbol,company_name):

    i = 0;
    #super_data = []
    time_lapse = int (time_lapse)
    #filename = 'C:\\selenium\\'+company_name+'.csv' # stooq data
    filename = 'C:\\selenium\\ALL\\'+company_name+'.mst' # BOS data
    with open(filename,'r') as f:
        reader =csv.reader(f)
        super_data
        super_data.clear()
        #print(super_data)
        f.readline()
        temporary_number=0
        j = 0;
        for row in reversed(list(reader)):
         #   if (j<=temporary_number):            
            if (i<time_lapse):
                super_data.append(row)
                    #print(super_data[0])
                    #print (super_data[i][1])
                i+=1
            else:
                break
          #  j+=1
        #print(super_data)
    for i in range (len(super_data)):
        for j in range (1,len(super_data[i])):
            #if (isinstance(super_data[i][j], str)):
            # print("dupa")
                #break
            #print(super_data)
            super_data[i][j]=float(super_data[i][j])
                #print (super_data[i][j])
    #print (super_data)

#def nagivate_to_next_page(driver,basic_url,page):

#    junk_url = "&i=d&l="
#    page_url = str(page)

#    next_page_url = basic_url+junk_url+page_url

#    return next_page_url

#def import_all_data_from_page(driver,url):

#    i=0
#    max_page = reading_max_page_stooq(driver)

#    while i < int(max_page)-1:
#    while i < 2:
#        current_page_url = nagivate_to_next_page(driver,url,i+1)
#        read_data_array(driver,current_page_url)
#        i+=1

##def read_data_array(driver,url):
##
##    driver.get(url)
##
##    table = driver.find_element_by_id('fth1')
##
##    file_raw_data = []
##
##    file_header = []
##
##    head = table.find_element_by_tag_name('thead')
##    body = table.find_element_by_tag_name('tbody')
##
##
##    head_line = head.find_element_by_tag_name('tr')
##    headers = head_line.find_elements_by_tag_name('td')
##    for header in headers:
##        header_text = header.text
##        file_header.append(header_text)
##
##    #print (file_header,max_page)
##
##    body_rows = body.find_elements_by_tag_name('tr')
##    for row in body_rows:   
##        data = row.find_elements_by_tag_name('td')
##        file_row=[]
##        for datum in data:
##            datum_text = datum.text
##            file_row.append(datum_text)
##        file_raw_data.append(file_row)
##        #print (file_row)
##        super_data.append(file_row)
    
def analyze_data (company_symbol,block_size,block_step,string,time_lapse):

    #print (super_data)
    data_string = string
    data_list = []
    today = dt.datetime.now().date()
    for i in range (len(company_name)):
        if (company_name[i][1]==company_symbol.upper()):
            company_name_ref=company_name[i][0]
    for i in range (len(time_list)):
        #print(time_list[i][0],time_lapse)
        if (int(time_list[i][0])==int(time_lapse)):
            time_lapse_ref=time_list[i][1]
    #print("adadasd",len(data_list))
    #data_string_2 = ""
    #print("SUP",len(super_data))
    if (data_string == "volume"):
        for i in range (len(super_data)):
            #print(super_data[i],i)
            #print ("Volume: ", super_data[i][5])
            #data_list.append(super_data[i][5])  # stooq data
            data_list.append(super_data[i][6])  # stooq data
            data_string_2="VOLUME "
    if (data_string == "end_price"):
        for i in range (len(super_data)):
            #print ("End_price: ", super_data[i][4])
            data_list.append(super_data[i][5])  # stooq data
            #data_list.append(super_data[i][5])  # stooq data
            data_string_2="END PRICE "
        #print(data_list)
        df=pd.DataFrame(data_list)
        lower = float(df.quantile(0.33))
        upper = float(df.quantile(0.66))
        print ("Dolna granica kanału cen: ",lower)
        print ("Górna granica kanału cen: ",upper)
        print ("Wczorajsza cena: ",data_list[0])
        if (data_list[0]<lower):
            under_price_channel.append([company_name_ref,lower,data_list[0]])
        if ((data_list[0]>lower) and (data_list[0]<upper)):
            in_price_channel.append([company_name_ref,lower,upper,data_list[0]])
        if (data_list[0]>upper):
            over_price_channel.append([company_name_ref,upper,data_list[0]])
        price_channel.append([company_name_ref,time_lapse_ref,"END PRICE - PRICE CHANNEL:","<",lower,";",upper,">","LAST END PRICE:",data_list[0]])
        #price_channel += (company_name_ref,time_lapse_ref,"END PRICE - PRICE CHANNEL:",lower,upper,"LAST END PRICE:",data_list[0])
        filename = 'C:/selenium/Raport_Spółki_' + company_name_ref + '.txt'
        #if os.path.exists(filename):
        #    with open(filename,'r') as f:
        #        reader =csv.reader(f)
        #        for row in reversed(list(reader)):
        #            if (row[0]!=str(today):
       #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!                 
        with open(filename,'a', newline='') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow ([str(today),lower,upper,data_list[0]])

        #print(data_list[0])

    min_val=min(data_list)
    max_val=max(data_list)
    #print(len(super_data))
    last_obj=len(super_data)-1
    last_val=data_list[0]
    #print(price_channel)
    blocks = []
    change = ""
    flow= ""
    trend = ""
    data = ""
    percentage_string = ""
    percentage = ""
    #print("DATA LIST", data_list)
    blocks = block_data_to_block(data_list,block_size,block_step)
    #print ("BLOCKS",blocks)
    
    change,flow,trend,data,percentage_string,percentage = analyze_block_trend(blocks,data_string)
    if (len(price_channel)!=0):
        #print(company_name_ref,flow)
        #print(price_channel,data_string,"1")
        #print(price_channel)
        price_channel[len(price_channel)-1].append([data_string_2 + "TREND:",flow])
        #print(price_channel,data_string,"2")
    #if (type_of_analysis == "log"):
    return data_string_2,change,flow,trend,data,percentage_string,percentage,min_val,max_val,last_val
    #if (type_of_analysis == "raport"):
    #    return flow

def block_data_to_block(data_list,block_size,block_step):

    num_of_data = len(data_list)
    block_size = int(block_size)
    step_size = int(block_step)
    #print("DDDDDD",len(data_list))
    #print ("sadasd","num:", num_of_data,"blocksize: ",block_size,"stepsize: ",step_size, "len: ",len(data_list))
    block_data = []
    #print(block_data)
    block_temp = 0
    for i in range (0,len(data_list)-block_size+1,step_size):
        
        #print (i,data_list)
        for j in range (block_size):
            #print(j)
            #print(data_list[i+j])
            block_temp += float(data_list[i+j])
            #print(block_temp)
            #print ("asd",block_data)
        block_data.append(block_temp/block_size)
        #print("asdadad",block_data,len(data_list),block_size)
        block_temp = 0
        #print("IIIIIII",i)
    #print(block_data)
    if (len(data_list)<block_size):
        for j in range (len(data_list)):
            block_temp += float(data_list[j])
        block_data.append(block_temp/len(data_list))
        block_temp = 0
    block_data=block_data[::-1] #reversing list so oldest is first
    #print (block_data)
    return (block_data)

def analyze_block_trend(blocks,data_string):

    #print(blocks,data_string)
    sum = 0
    for i in range(len(blocks)):
        #print(blocks)
        sum += blocks[i] 

    #print(sum,len(blocks))
    average = sum/len(blocks)
    trend = 0
    data = ""
    flow = ""
    risk = ""

    if (data_string=="volume"):
        data="VOLUME"

    if (data_string=="end_price"):
        data="END_PRICE"
        

        
    for i in range(len(blocks)-1):
        if (blocks[i]<blocks[i+1]):
            trend += blocks[i+1]-blocks[i] 
        if (blocks[i]>blocks[i+1]):
            trend -= blocks[i]-blocks[i+1]
            
        #print (i,trend)
    low_border = average*90/100
    high_border = average*110/100
    #print (trend,"AVG",average,low_border,high_border)
    #print("Dupa")
    if (trend>0 and (average + abs(trend)) > high_border ):
        flow="UP"
        #print("dupa")
##        if (last_val/max_val>=max_val*90/100 and data=="END_PRICE"):
##            risk="LOW"
##        if (last_val/max_val<max_val*90/100) and (last_val/max_val>=max_val*70/100 and data=="END_PRICE"):
##            risk="MEDIUM"
##        if (last_val/max_val<max_val*70/100) and (last_val/max_val>=max_val*60/100 and data=="END_PRICE"):
##            risk="HIGH"
##        if (last_val/max_val<max_val*60/100) and data=="END_PRICE":
##            risk="VERY HIGH"
##        print (risk, qwe)
        
        #print (data_string,"UP","LOW BLOCK BORDER:",low_border,"HIGH BLOCK BORDER:",high_border,"AVERAGE BLOCK :",average,"TREND:",trend, "Percentage change: ", trend*100/average, "%")
    if (trend<0 and (average - abs(trend)) < low_border):
        #print("dyupa")
        flow="DOWN"
        #print (data_string,"DOWN","LOW BLOCK BORDER:",low_border,"HIGH BLOCK BORDER:",high_border,"AVERAGE BLOCK :",average,"TREND:",trend, "Percentage change: ", trend*100/average, "%")    
    if (trend==0 or ((average + abs(trend)) <= high_border and (average - abs(trend)) >= low_border)):
        flow="SIDE"
        #print (data_string,"SIDE","LOW BLOCK BORDER:",low_border,"HIGH BLOCK BORDER:",high_border,"AVERAGE BLOCK :",average,"TREND:",trend, "Percentage change: ", trend*100/average, "%")    
    #print ("null",low_border,high_border,average,trend)
    #print(average)
    percentage = str(trend*100/average) + "%"
    #if (data_string=="end_price"):
    #    print (percentage)
    return ("Change: ",flow,"Trend: ",trend,"Percentage change: ",percentage)

start()

