# coding: utf8

import csv
import datetime
import smtplib
import ssl
import time
import datetime as dt
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import pandas as pd
from script.files import DBCursos
from script.files import ImportNamesFromFile
from script.files import ImportDataFromFile
from script.files import NumberOfDayMenu
from script.files import DaysInYear
from script.files import ConfigFile
from script.files import SQLDICT

today = dt.datetime.now().date()
todayStr = str(today)
todayStr2 = todayStr.replace("-", "")


data_list = []
lower_list = []
upper_list = []
lets_say_current_list = []
outputsArray = []
date_list = []
curr_2year = []
# companies_list = []
# day_param = 350 # - year
#day_param = 1

config_dict = ConfigFile.load_config()

auto_mode = int(config_dict['auto_mode'])
day_param = NumberOfDayMenu.days_choice(auto_mode)
sendmail = int(config_dict['send_email'])
online_mode = int(config_dict['online_mode'])

if online_mode == 1:
    mydb, mycursor, database_param = DBCursos.main()
else:
    mydb, mycursor, database_param = 0, 0, 0

last_id = -1
last_oid = -1

# sql_data = SQLDICT.getdict()
# querry = sql_data['maxoids']
# mycursor.execute(querry)
# print(mycursor.fetchall())


def select_last_from_mysql_db(table_name):

    sql = "select " + "max(" + table_name + "_oid)" + "," + "max(" + table_name + "_id)" + " from " + database_param + "." + table_name
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    temp1, temp2 = myresult[0]
    if str(temp1) == "None":
        return -1, 0
    else:
        return myresult[0]
    
def writeToFile(data):

    if day_param > 1:
        prefix = str(day_param) + '_multi_'
    else:
        prefix = 'single_'

    dataString = str(datetime.date.today())
    # prefix = ''
    # dataString = ''
    filename = prefix + 'output' + dataString + '.csv'

    with open(filename, 'w', newline='') as csvfile:
        for singleRow in data:
            spamwriter = csv.writer(csvfile)
            row = [str(singleRow).replace('[', '').replace(']', '').replace(',', '|').replace('\'', '').replace('| ', '|').replace('.', ',')]
            spamwriter.writerow(singleRow)

def read_raports():

    # 0 - test 1 - full
    companies_list = ImportNamesFromFile.import_names_from_file(1)
    time_table = []
    timeStart = datetime.datetime.now()
    for k in range(day_param):
        print(str(k) + " from " + str(day_param))
        time_start = time.time()
        for company in companies_list:

            time_comp_start = time.time()
            data_list.clear()
            lower_list.clear()
            upper_list.clear()
            date_list.clear()
            company_data_from_two_years = ImportDataFromFile.import_data_from_file(str(company))
            if k <= len(company_data_from_two_years):
                analyze_data(company, k, company_data_from_two_years)
            time_comp_end = time.time()
            # print(time_comp_end - time_comp_start)

        print(str(round(100 * ((k + 1) / day_param), 3)) + '% Complete')
        if online_mode == 0:
            sortedOutputsArray = sorted(outputsArray, key=lambda x: x[-1])

            payload = []
            reducedList = []
            for output in sortedOutputsArray:
                if 'BUY2' in output or 'SELL' in str(output):
                    reducedList.append(output)
            for record in reducedList:
                print(record)
            payload = reducedList
            if sendmail == 1 and k <= 1:
                sendingMail(payload)

            writeToFile(sortedOutputsArray)
        time_end = time.time()

        time_table.append(time_end - time_start)

    print(time_table)
    timeEnd = datetime.datetime.now()
    print("Done in : " + str(timeEnd-timeStart))

def analyze_data(company_name, day_param_iterator, company_data_from_two_years):

    time_lapse = 10000
    global max_value
    days_in_year = 0
    current_status = ""
    last_status = ""
    previous_status = ""
    max_value = []
    max_value.clear()
    statuses = []
    output = []
    buffor_day_range = 5  # zakres bufforu z pocatku roku uniemozliwiajacy sell
    output.clear()
    low_max_text = ""
    low_max_value = 0
    lets_say_current_list = []
    special_text = ""
    special_value = 0
    temp_value_for_i = 0
    max_value.clear()
    progression = 0
    # skip = False

    days_in_year = DaysInYear.daysInYear(company_data_from_two_years)
    # for i in range(len(super_data)):
    #    if(int(todayStr2)-time_lapse) > int(super_data[i][1]):
    #        days_in_year = i
    #        break

    #  main loop - most heavy in timeload
    time_comp_start = time.time()
    timeJ = []
    for j in range(days_in_year):
        time_j_start = time.time()
        temp_var = days_in_year+j

        for i in range(j, temp_var):  # loop for creating data_list - list of company value in 1 y window offset by j (for 2 years span analysis)
            if i == len(company_data_from_two_years)-1:
                break
            data_list.append(company_data_from_two_years[i][5])

        temp_max_value = 0
        df = pd.DataFrame(data_list)
        lower_list.append(df.quantile(0.33).values.min())
        upper_list.append(df.quantile(0.66).values.min())
        date_list.append(int(company_data_from_two_years[j][1]))  # !!!!!!wrzucic do petli for i->powinno dzialac
        lets_say_current_list.append(data_list[0])
        for k in range(buffor_day_range):
            if float(data_list[len(data_list)-1-k]) > float(temp_max_value):
                temp_max_value = float(data_list[len(data_list)-1-k])
        max_value.append(temp_max_value)
        data_list.clear()
        time_j_end = time.time()
        # print(f'TimeJ: ' + str(time_j_end-time_j_start))
        timeJ.append(time_j_end - time_j_start)

    if len(lets_say_current_list)>0:
        highest = max(lets_say_current_list)
        lowest = min(lets_say_current_list)
    else:
        return

    time_comp_end = time.time()
    # print(f'Main loop: ' + str(time_comp_end-time_comp_start))

    if 1 == 1:

        # print ("Not exists")

        for i in reversed(range(day_param_iterator, len(lower_list))):

            # print(str(check_if_record_already_exist_2(date_list[day_param], company_name)) + " " + str(date_list[day_param]) + " " + str(company_name))

            if float(lets_say_current_list[i]) < float(lower_list[i]):

                special_text = "Perct to bottom price channel"
                special_value = "{0:.2f}".format(100-(float(lets_say_current_list[i])/float(lower_list[i])*100))
                low_max_text = "Min Value"
                low_max_value = lowest
                current_status = "low"
                statuses.append("low")            
                if last_status != current_status:
                    progression = 1
                    previous_status = last_status
                    last_status = current_status
                    
                else:
                    progression += 1
 
            elif float(lets_say_current_list[i]) >= float(lower_list[i]) and (float(lets_say_current_list[i]) <= float(upper_list[i])):

                special_text = "Perct from avg channel price"
                avg = ((float(upper_list[i])+float(lower_list[i]))/2)
                special_value = "{0:.2f}".format(float(lets_say_current_list[i])/avg)
                low_max_text = "Average channel price:"
                low_max_value = avg
                current_status = "in"
                statuses.append("in")
                if last_status != current_status:
                    progression = 1
                    previous_status = last_status
                    last_status = current_status
                else:
                    progression += 1

            elif float(lets_say_current_list[i]) > float(upper_list[i]):

                special_text = "Perct over top price channel"
                special_value = "{0:.2f}".format(((float(lets_say_current_list[i])/float(upper_list[i])*100)-100))
                low_max_text = "Max value"
                low_max_value = highest
                current_status = "upper"
                statuses.append("upper")
                if last_status != current_status:
                    progression = 1
                    previous_status = last_status
                    last_status = current_status
                else:
                    progression += 1

            if previous_status == "":
                previous_status = current_status
        
            temp_value_for_i = i

        # time_end = time.time()

        # print(str(time_end - time_start) + " Time 2 loop in analyze")
        # checking for max range of dates in comp history ex if company is 30 days on market,but users checks for 45days
        if int(day_param_iterator) < len(lower_list):

            output = [date_list[temp_value_for_i], company_name, "Current Value:", lets_say_current_list[temp_value_for_i], "Current status", current_status, "Previous status", previous_status, "Streak", progression, low_max_text, low_max_value, special_text, special_value, "Lower Price Channel", lower_list[temp_value_for_i], "Upper Price Channel", upper_list[temp_value_for_i], max_value[day_param_iterator]]
            # analyze_price_channel(output)
            if online_mode == 1:
                if check_if_record_already_exist(output):
                    print("RECORD ALREADY EXISTS:" + str(output))
                else:
                    global last_oid, last_id
                    insert_into_mysql_db(last_oid, last_id, output)
                    last_oid, last_id = select_last_from_mysql_db("raport")
            else:
                analyze_price_channel(output)
                outputsArray.append(output)

# NOT USED RIGHT NOW
def analyze_price_channel(output):

    text = ""

    # [5] status        [11] prct special value (min/max etc)
    if output[5] == "low":
        if float(output[3]) / float(output[11]) > float(1.10):
            # Cena ponad 10% od dołka(pod kanalem cenonwym)
            # print("Start of rising - BUY")
            # text = "Start of slowly rising - BUY"
            text = "BUY"
        # elif ((float(output[3])/float(output[11])>float(1.10)):
        # text = "Heavy spike up - risky BUY"
            # print("aaaaaaaaaaaa")
                                                                    
        else:
            if int(output[9] > int(10)):
                # Cena jest blisko dołka przez ponad 10 dni (pod kanalem cenonwym)
                # print("Lies deep beneath the ocean - time to buy")
                # text ="Lies deep beneath the ocean - time to buy"
                text = "BUY1"
            else:
                # Cena spadla pod kanal cenonwy
                # print("Starts being cheap - think about buying")
                text = "BUY2"
        # print(output)
        output.append(text)
        # print(output)
    if output[5] == "in":
        if output[7] == "low":
            if float(output[13]) < float(1):
                # Cena wskoczyła w kanał z dołka
                # print("Rised above the bottom line - last moment for buying")
                text = "Late Buying"
            else:
                # Cena jest ponad średnią, ale w kanale - dom. rośnie bo wyszła z dołka
                # print("Stable and going up - should be expensive soon")
                text = "Close to Sell"
        if output[7] == "upper":
            if float(output[13]) < float(1):
                # Cena jest w kanale - ale spada poniżej średniej - dom. była wczesniej nad kanałek
                # print("Going down - should be cheap soon")
                text = "Close to Buy"
            else:
                # Cena spadła do kanału z gorki
            
                # print("Starting to decline - last moment for selling")
                text = "Late Selling"
        output.append(text)
    if (output[5] == "upper") and (float(output[3]) > float(output[18])):
        if float(output[3]) / float(output[11]) > float(0.9):
            # Cena buduje szczyt - jestes w topie lub w 10% odleglosci od niego
            # print("Making summit - SELL!")
            text = "SELL"
        else:
            if int(output[9] > int(10)):
                # cena zrobila szczyt i utrzymuje wartosc wieksza niz 10% od szczytu ale wciaz jest droga
                # print("Goind down - time to sell")
                text = "SELL1"
            else:
                # cena spadla o wiecej niz 10% od szczytu w ostatnich dniach( <10 ergo. szybko),ale wciaz jest droga
                # print("Expensive but far from heaven - think of selling")
                text = "SELL2"
        output.append(text)
    elif (output[5] == "upper") and (float(output[3]) <= float(output[18])):
        # Cena odbija ale jest ryzyko ze sell w stosunku do buya bedzie na -
        # text = "Starting to rise - risky Buy"
        text = "Selling not adviced - possible High Buying Price"
        output.append(text)
    # print("")
    return


def main():

    global last_oid, last_id, max_value
    if online_mode == 1:
        last_oid, last_id = select_last_from_mysql_db("raport")

    max_value = []
    read_raports()


def insert_into_mysql_db(last_oid_param, last_id_param, output):

    temp_oid = last_oid_param+1
    temp_id = last_id_param+1
    sql = "INSERT INTO raport (raport_oid, raport_id, date, company_name, current_value, current_status,previous_status,Streak,special_value,Perct_special_value,bottom_price_channel, upper_price_channel, max_value) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    # val = (temp_oid,temp_id,"20190205","Hydrotor","20","low","in","5","15","20","50","100")

    val = (temp_oid, temp_id, output[0], output[1], output[3], output[5], output[7], output[9], output[11], output[13], output[15], output[17], output[18])
    mycursor.execute(sql, val)
    mydb.commit()


def check_if_record_already_exist(output):

    table_name = "raport"
    # sql = "select *" + " from " + "apkadb."+table_name + " where date" +"='" +str(output[0]) +"' and company_name"+ "='" + str(output[1]+"'")
    sql = "select *" + " from " + database_param + "." + table_name + " where date" + "='" + str(output[0]) + "' and company_name" + "='" + str(output[1] + "'")
    mycursor.execute(sql)
    myresult = mycursor.fetchall()

    if len(myresult) > 0:
        return True
    else:
        return False


def check_if_record_already_exist_2(date, company_name):

    table_name = "raport"
    sql = "select *" + " from " + database_param + "." + table_name + " where date" + "='" + str(date) + "' and company_name" + "='" + str(company_name) + "'"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    if len(myresult) > 0:
        return True
    else:
        return False


def sendingMail(payload):
    port = 465  # For SSL
    smtp_server = "smtp.gazeta.pl"

    emailCredentials = ConfigFile.load_password()

    sender_email = emailCredentials[1]  # Enter your address
    receiver_email = emailCredentials[2]  # Enter receiver address

    messageStr = ""

    message = MIMEMultipart("alternative")
    message["Subject"] = "IMPORTANT STOCK UPDATE " + str(datetime.date.today())
    message["From"] = sender_email
    message["To"] = receiver_email

    payload = editPayloadForEmail(payload)
    for record in payload:
        messageStr += "\n" + str(record)
    if len(payload) > 0:

        part1 = MIMEText(messageStr, "plain")
        message.attach(part1)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, emailCredentials[0])
            server.sendmail(sender_email, receiver_email, message.as_string())

def editPayloadForEmail(payload):

    companies_list = ImportNamesFromFile.import_names_from_file(2)
    editedPayload = []
    for record in payload:
        if ("SELL" in str(record) and record[1] in companies_list) or ("BUY" in str(record) and record[1] not in companies_list):
            editedPayload.append(str(record[19]) + ' NOW ' + str(record[1]) + ' FOR PRICE ' + str(record[3]))

    return editedPayload

if __name__ == '__main__':
    main()

