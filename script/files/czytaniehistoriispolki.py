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
import DBCursos
import ImportNamesFromFile
import ImportDataFromFile
import NumberOfDayMenu
import DaysInYear
import ConfigFile
import SQLClass
import buySellSignalAnalysis
import SQLDICT

today = dt.datetime.now().date()
todayStr = str(today)
todayStr2 = todayStr.replace("-", "")

lower_list = []
upper_list = []
outputsArray = []
date_list = []
curr_2year = []
lower_quartile = 0.33
higher_quartile = 0.66
quartile_test = False
# companies_list = []
# day_param = 350 # - year
# day_param = 1

config_dict = ConfigFile.load_config()

auto_mode = int(config_dict['auto_mode'])
day_param = NumberOfDayMenu.days_choice(auto_mode)
sendmail = int(config_dict['send_email'])
online_mode = int(config_dict['online_mode'])

if online_mode == 1:
    mydb, mycursor, database_param = DBCursos.main()
    sqlClass = SQLClass.SQLClass(mydb, mycursor, database_param)
else:
    mydb, mycursor, database_param = 0, 0, 0

last_id = -1
last_oid = -1


# sql_data = SQLDICT.getdict()
# querry = sql_data['maxoids']
# mycursor.execute(querry)
# print(mycursor.fetchall())

def writeToFile(data, mode):

    # final = splitByCompanies(data)

    prefix = ''

    offset = int(config_dict['offset'])
    if offset >= 10000:
        prefix += str(offset/10000)+'y_'

    if day_param > 1:
        prefix += str(day_param) + '_multi_'
    else:
        prefix += 'single_'
    if quartile_test:
        prefix += str(lower_quartile) + str(higher_quartile) + '_'

    if mode == 2:
        prefix += 'withNewConnect' + '_'

    dataString = str(datetime.date.today())
    # prefix = ''
    # dataString = ''
    filename = prefix + 'output' + dataString + '.csv'

    with open(filename, 'w', newline='') as csvfile:
        for singleRow in data:
            spamwriter = csv.writer(csvfile)
            row = [str(singleRow).replace('[', '').replace(']', '').replace(',', '|').replace('\'', '').replace('| ', '|').replace('.', ',')]
            spamwriter.writerow(singleRow)

def splitByCompanies(data):

    # SEGREGATE BY COMPANY NAMES AND SPLIT INTO SUBLISTS
    indexes = [index for index, _ in enumerate(data) if data[index][1] != data[index - 1][1]]
    indexes.append(len(data))
    final = [data[indexes[i]:indexes[i + 1]] for i, _ in enumerate(indexes) if i != len(indexes) - 1]

    return final

def read_stock_raports(analysisMode):
    # 0 - test 1 - GPW 2 - NewConnect
    text = ''
    if analysisMode == 1:
        text = 'GPW'
    if analysisMode == 2:
        text = 'NEW CONNECT'

    print(f'{text} ANALYSIS')

    companies_list = ImportNamesFromFile.import_names_from_file(analysisMode)
    time_table = []
    timeStart = datetime.datetime.now()

    for k in range(day_param):
        print(str(k) + " from " + str(day_param))
        time_start = time.time()
        for company in companies_list:

            time_comp_start = time.time()
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
                if 'BUY3' in output or 'SELL' in str(output):
                    reducedList.append(output)
            if k <= 1:
                for record in reducedList:
                    print(record)
                    # print(str(float(record[17])/float(record[15])))
                if sendmail == 1:
                    payload = reducedList
                    sendingMail(payload)

            writeToFile(sortedOutputsArray, analysisMode)
        time_end = time.time()
        time_passed = time_end - time_start
        print(f'Time {time_passed}')
        time_table.append(time_passed)

    print(time_table)
    timeEnd = datetime.datetime.now()
    print("Done in : " + str(timeEnd - timeStart))


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

    data_list = []
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
        temp_var = days_in_year + j

        for i in range(j, temp_var):  # loop for creating data_list - list of company value in 1 y window offset by j (for 2 years span analysis)

            # if when company_data is shorter (example when not every day trading is available or something else
            if i == len(company_data_from_two_years) - 1:
                break
            data_list.append(company_data_from_two_years[i][5])

        temp_max_value = 0
        df = pd.DataFrame(data_list)
        lower_list.append(df.quantile(lower_quartile).values.min())
        upper_list.append(df.quantile(higher_quartile).values.min())
        date_list.append(int(company_data_from_two_years[j][1]))  # !!!!!!wrzucic do petli for i->powinno dzialac
        lets_say_current_list.append(data_list[0])
        for k in range(buffor_day_range):
            if float(data_list[len(data_list) - 1 - k]) > float(temp_max_value):
                temp_max_value = float(data_list[len(data_list) - 1 - k])
        max_value.append(temp_max_value)
        data_list.clear()
        time_j_end = time.time()
        # print(f'TimeJ: ' + str(time_j_end-time_j_start))
        timeJ.append(time_j_end - time_j_start)

    if len(lets_say_current_list) > 0:
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
                special_value = "{0:.2f}".format(100 - (float(lets_say_current_list[i]) / float(lower_list[i]) * 100))
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
                avg = ((float(upper_list[i]) + float(lower_list[i])) / 2)
                special_value = "{0:.2f}".format(float(lets_say_current_list[i]) / avg)
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
                special_value = "{0:.2f}".format(((float(lets_say_current_list[i]) / float(upper_list[i]) * 100) - 100))
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
                if sqlClass.check_if_record_already_exist(output):
                    print("RECORD ALREADY EXISTS:" + str(output))
                else:
                    global last_oid, last_id
                    sqlClass.insert_into_mysql_db(last_oid, last_id, output)
                    last_oid, last_id = sqlClass.select_last_from_mysql_db("raport")
            else:
                buySellSignalAnalysis.analyze_price_channel(output)
                outputsArray.append(output)


def main():
    global last_oid, last_id, max_value
    if online_mode == 1:
        last_oid, last_id = sqlClass.select_last_from_mysql_db("raport")

    two_year_span = int(config_dict['two_year_span'])
    one_year_span = int(config_dict['one_year_span'])
    offset = int(config_dict['offset'])
    gpw_analysis = int(config_dict['analyze_gpw'])
    newconnect_analysis = int(config_dict['analyze_newconnect'])
    today_string = str(dt.datetime.now().date()).replace("-", "")

    analysisFrom = int(today_string) - one_year_span - offset
    analysisTo = int(today_string) - offset

    print(f'Analysis from {analysisFrom} to {analysisTo}')

    max_value = []
    # global lower_quartile
    # global higher_quartile
    # for i in range(7):
    #     match i:
    #         case 0:
    #             lower_quartile = 0.40
    #             higher_quartile = 0.60
    #         case 1:
    #             lower_quartile = 0.35
    #             higher_quartile = 0.65
    #         case 2:
    #             lower_quartile = 0.33
    #             higher_quartile = 0.66
    #         case 3:
    #             lower_quartile = 0.30
    #             higher_quartile = 0.70
    #         case 4:
    #             lower_quartile = 0.25
    #             higher_quartile = 0.75
    #         case 5:
    #             lower_quartile = 0.20
    #             higher_quartile = 0.80
    #         case 6:
    #             lower_quartile = 0.15
    #             higher_quartile = 0.85

    if gpw_analysis:
        read_stock_raports(1)
    if newconnect_analysis:
        read_stock_raports(2)

def sendingMail(payload):
    port = 465  # For SSL
    smtp_server = "smtp.gazeta.pl"

    emailCredentials = ConfigFile.load_password()

    sender_email = emailCredentials[0]  # Enter your address
    sender_password = emailCredentials[1]

    emailWithCompanies = ImportNamesFromFile.import_email_and_companies()
    for mailWithCompany in emailWithCompanies:
        receiver_email = mailWithCompany[:1][0]  # Enter receiver address

        messageStr = ""

        message = MIMEMultipart("alternative")
        message["Subject"] = "IMPORTANT STOCK UPDATE " + str(datetime.date.today())
        message["From"] = sender_email
        message["To"] = receiver_email
        editedPayload = editPayloadForEmail(payload, mailWithCompany[1:])
        for record in editedPayload:
            messageStr += "\n" + str(record)
        if len(editedPayload) > 0:
            part1 = MIMEText(messageStr, "plain")
            message.attach(part1)

            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, receiver_email, message.as_string())


def editPayloadForEmail(payload, companies):
    editedPayload = []
    for record in payload:
        if ("SELL" in str(record) and record[1] in str(companies)) or ("BUY" in str(record) and record[1] not in str(companies)):
            editedPayload.append(str(record[19]) + ' NOW ' + str(record[1]) + ' FOR PRICE ' + str(record[3]))

    return editedPayload


if __name__ == '__main__':
    main()

