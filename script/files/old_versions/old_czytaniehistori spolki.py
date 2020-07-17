import time
import datetime as dt
import csv
import os.path
from datetime import datetime,timedelta
from pathlib import Path
import pandas as pd
import mysql.connector

selenium_url = 'C:/selenium/'
filename_url_part1 = selenium_url + 'Benefit.mst'

today = dt.datetime.now().date()
todayStr = str(today)
todayStr2 = todayStr.replace("-","")
company_data_from_two_years = []
data_list = []
lower_list = []
upper_list = []
lets_say_current_list = []
date_list = []
curr_2year = []
companies_list = []
cheap_list = []
normal_list = []
expensive_list = []
day_param=350;# - year
day_param=1;
#day_param=1;

#parameters for sql connection

host_param = "remotemysql.com"
user_param = "zr00HYpK6O"
passwd_param = "SOdKgWqLJr"
database_param = "zr00HYpK6O"

#mysql connection set up
# mydb = mysql.connector.connect(
# host="localhost",
# user="root",
# passwd="that5whorule",
# database="apkadb"
# )
mydb = mysql.connector.connect(
host=host_param,
user=user_param,
passwd=passwd_param,
database=database_param
)
mycursor = mydb.cursor()

last_id=-1;
last_oid=-1;
    
def select_last_from_mysql_db(table_name):

    #sql = "select " + "max(" +table_name+"_oid)"+","+"max(" +table_name+"_id)" + " from " + "apkadb."+table_name
    sql = "select " + "max(" + table_name + "_oid)" + "," + "max(" + table_name + "_id)" + " from " + database_param + "." + table_name
    #print(sql)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    #print(myresult)
    temp1,temp2=myresult[0]
    #print(myresult[0])
    if (str(temp1)== "None"):
        #print("111111")
        return(-1,0)
    else:
        #print("000000")
        return myresult[0]
    

def read_raports():
    
    import_names_from_file()
    cheap_list.clear()
    normal_list.clear()
    expensive_list.clear()
    var_for_k_param = 1
    #companies_list.clear()
    #companies_list.append(["skarbiec"])
    #companies_list.append(["ideabank"])
    #companies_list.append(["skarbiec"])
    #companies_list.append(["domdev"])
    check_if_new_raport_exist()
    for k in range(day_param):
        print(k)
        for i in range(len(companies_list)):
            #print(companies_list)
            #if (k<var_for_k_param):
            company_data_from_two_years.clear()
            data_list.clear()
            lower_list.clear()
            upper_list.clear()
            lets_say_current_list.clear()
            date_list.clear()
            #print(companies_list[i][0])
            import_data_from_file(str(companies_list[i][0]))
            analyze_data(companies_list[i][0],k)
            #if (len(lets_say_current_list)<249):
            #    print(companies_list[i][0])
            #    print(len(lets_say_current_list))
            #print(len(lets_say_current_list))
            var_for_k_param = len(lets_say_current_list)
            #else:
            #    continue
        print("Under price channel:")
        for i in range(len(cheap_list)):        
            print(cheap_list[i])
            #print(cheap_list[i][1])
        print("")   
        print("In price channel:")
        for i in range(len(normal_list)):
            print(normal_list[i])
            #print(normal_list[i][1])
        print("")    
        print("Over price channel:")
        for i in range(len(expensive_list)):
            print(expensive_list[i])
        print("")
            #print(expensive_list[i][1])
        #import_data_from_file("VIVID")
        #analyze_data()
        #print(todayStr2)
        export_to_file(cheap_list,normal_list,expensive_list)
        cheap_list.clear()
        normal_list.clear()
        expensive_list.clear()

def analyze_data(company_name,day_param):

    timelapse=10000;
    global max_value;
    #max_value=0;
    days_in_year=0;
    current_status="";
    last_status="";
    previous_status="";
    change_bigger_status = 0;
    max_value=[];
    max_value.clear();
    statuses = [];
    output = [];
    buffor_day_range=5; #zakres bufforu z pocatku roku uniemozliwiajacy sell
    output.clear();
    temp_max_value=0;
    temp = "";
    lowest = 0;
    highest = 0;
    low_max_text="";
    low_max_value=0;
    #max_value=0;
    special_text="";
    special_value=0;
    temp_value_for_i = 0;
    max_value.clear(); 
    progression=0;
    change_status=1;
    for i in range (len(company_data_from_two_years)):
        if((int(todayStr2)-timelapse)>int(company_data_from_two_years[i][1])):
            days_in_year =(i)
            break

    for j in range (days_in_year):
        temp_var = days_in_year+j
        for i in range (j,temp_var):
            if (i==len(company_data_from_two_years)-1):
                break
            data_list.append(company_data_from_two_years[i][5])

        temp_max_value=0;
        #print (len(data_list))
        df=pd.DataFrame(data_list)
        lower_list.append(float(df.quantile(0.33)))
        upper_list.append(float(df.quantile(0.66)))
        #print(j,i,super_data[i][1])
        #print(super_data)
        #print(j,i)
        date_list.append(int(company_data_from_two_years[j][1]))#!!!!!!wrzucic do petli for i->powinno dzialac
        #print(data_list[0])
        lets_say_current_list.append(data_list[0])
        #max_value=max(map(float,data_list[0]))
        #if (data_list[0]>float(max_value)):
        #    max_value=float(data_list[0])
        #print(lets_say_current_list)
        #print(data_list)
        for k in range(buffor_day_range):
            #print(j,data_list[len(data_list)-1-k])
            #print("temp max val1 ",temp_max_value)
            if (float(data_list[len(data_list)-1-k])>float(temp_max_value)):
                temp_max_value=float(data_list[len(data_list)-1-k])
            #print("temp max val2 ",temp_max_value)        
        max_value.append(temp_max_value);
        #print(data_list[len(data_list)-1]));
        #max_value.append(max(data_list[0][len(data_list)-1],data_list[0][len(data_list)-2],data_list[0][len(data_list)-3],data_list[0][len(data_list)-4],data_list[0][len(data_list)-5]));
        data_list.clear()
    #print(data_list)
    #print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    highest = max(lets_say_current_list)
    lowest = min(lets_say_current_list)
    
    #for k in range(day_param+1):
    #  print (k)
    #print(day_param)
    if (1==1):
                    
        #print("III?",i)
        #for i in reversed(range(day_param,len(lower_list))):
        #print (day_param,"asdasdad")
        for i in reversed(range(day_param,len(lower_list))):
            #if (i>300):
            #print(i,lets_say_current_list[i],"          ",lower_list[i])
            #print(i,range(day_param,len(lower_list)))
            if (float(lets_say_current_list[i])<float(lower_list[i])):

                special_text="Perct to bottom price channel"
                special_value="{0:.2f}".format(100-(float(lets_say_current_list[i])/float(lower_list[i])*100))
                low_max_text="Min Value"
                low_max_value=lowest
                current_status="low"
                statuses.append("low")            
                if (last_status != current_status):
                    progression=1
             #       change_status=1
                    previous_status=last_status
                    last_status=current_status
                    
                else:
                    progression+=1
 
            elif (float(lets_say_current_list[i])>=float(lower_list[i]) and (float(lets_say_current_list[i])<=float(upper_list[i]) )):

                special_text="Perct from avg channel price"
                avg = ((float(upper_list[i])+float(lower_list[i]))/2)
                special_value="{0:.2f}".format(float(lets_say_current_list[i])/avg)
                low_max_text="Average channel price:"
                low_max_value=avg
                #print ("dupa",float(upper_list[i]),float(lower_list[i]),avg)
                current_status="in"
                statuses.append("in")
                if (last_status != current_status):
                    progression=1
              #      change_status=1
                    previous_status=last_status
                    last_status=current_status
                else:
                    progression+=1

            elif (float(lets_say_current_list[i])>float(upper_list[i])):

                special_text="Perct over top price channel"
                special_value="{0:.2f}".format(((float(lets_say_current_list[i])/float(upper_list[i])*100)-100))
                low_max_text="Max value"
                low_max_value=highest
                current_status="upper"
                statuses.append("upper")
                if (last_status != current_status):
                    progression=1
               #     change_status=1
                    previous_status=last_status
                    last_status=current_status
                else:
                    progression+=1

            
  
            if (previous_status==""):
                previous_status=current_status
        
            temp_value_for_i=i
        
        #print(len(max_value), day_param);
        
        if (int(day_param)<len(lower_list)):
                            
            output =[date_list[temp_value_for_i],company_name,"Current Value: ", lets_say_current_list[temp_value_for_i], "Current status", current_status,"Previous status",previous_status,"Streak",progression,low_max_text,low_max_value,special_text,special_value,"Lower Price Channel",lower_list[i],"Upper Price Channel",upper_list[i],max_value[day_param]]
        #print(company_name,output)
            analyze_price_channel(output)

            if (check_if_record_already_exist(output)):
                print("RECORD ALREADY EXISTS:" + str(output) )
            else:            
                global last_oid,last_id
            #print (last_oid,last_id,"before");
                insert_into_mysql_db(last_oid,last_id,output)
                last_oid,last_id = select_last_from_mysql_db("raport")
            
def analyze_price_channel(output):

    text = ""
    #print(len(output))
    #cheap_list.clear()
    #normal_list.clear()
    #expensive_list.clear()
    #print(output[3],output[15])
    if (output[5]=="low"):
        if ((float(output[3])/float(output[11])>float(1.10))):
            #Cena ponad 10% od dołka(pod kanalem cenonwym)
            #print("Start of rising - BUY")
            #text = "Start of slowly rising - BUY"
            text = "BUY"
        #elif ((float(output[3])/float(output[11])>float(1.10)):
         #   text = "Heavy spike up - risky BUY"
            #print("aaaaaaaaaaaa")
                                                                    
        else:
            if (int(output[9]>int(10))):
                #Cena jest blisko dołka przez ponad 10 dni (pod kanalem cenonwym)
                #print("Lies deep beneath the ocean - time to buy")
                #text ="Lies deep beneath the ocean - time to buy"
                text ="BUY1"
            else:
                #Cena spadla pod kanal cenonwy
                #print("Starts being cheap - think about buying")
                text = "BUY2"
        #print(output)
        output.append(text)
        #print(output)
        cheap_list.append([output])
    if (output[5]=="in"):
        if (output[7]=="low"):
            if (float(output[13])<float(1)):
                #Cena wskoczyła w kanał z dołka
                #print("Rised above the bottom line - last moment for buying")
                text = "Late Buying"
            else:
                #Cena jest ponad średnią, ale w kanale - dom. rośnie bo wyszła z dołka
                #print("Stable and going up - should be expensive soon")
                text = "Close to Sell"
        if (output[7]=="upper"):
            if (float(output[13])<float(1)):
                #Cena jest w kanale - ale spada poniżej średniej - dom. była wczesniej nad kanałek
                #print("Going down - should be cheap soon")
                text = "Close to Buy"
            else:
                #Cena spadła do kanału z gorki
            
                #print("Starting to decline - last moment for selling")
                text ="Late Selling"
        output.append(text)
        normal_list.append([output])
    if ((output[5]=="upper") and (float(output[3])>float(output[18]))):
        if (float(output[3])/float(output[11])>float(0.9)):
            #Cena buduje szczyt - jestes w topie lub w 10% odleglosci od niego
            #print("Making summit - SELL!")
            text = "SELL"
        else:
            if (int(output[9]>int(10))):
                #cena zrobila szczyt i utrzymuje wartosc wieksza niz 10% od szczytu ale wciaz jest droga
                #print("Goind down - time to sell")
                text = "SELL1"
            else:
                #cena spadla o wiecej niz 10% od szczytu w ostatnich dniach(mniej niz 10 ergo. szybko), ale wciaz jest droga
                #print("Expensive but far from heaven - think of selling")
                text = "SELL2"
        output.append(text)
        expensive_list.append([output])
    elif ((output[5]=="upper") and (float(output[3])<=float(output[18]))):
        #Cena odbija ale jest ryzyko ze sell w stosunku do buya bedzie na -
        #text = "Starting to rise - risky Buy"
        text = "Selling not adviced - possible High Buying Price"
        output.append(text)
        expensive_list.append([output])
    #print("")
    return 
def check_if_new_raport_exist ():

    today = dt.datetime.now().date()

    if not os.path.exists(selenium_url+ '/PC'):
        os.makedirs(selenium_url + '/PC')
    filename = selenium_url + 'PC/' + 'raporty'+str(today)+'.txt'
    #filename = 'C:\\selenium\\PC\\'+'raporty'+str(today)+'.txt' #for new raports

    if os.path.exists(filename):
        os.remove(filename)

def export_to_file(cheap_list,normal_list,expensive_list):

    today = dt.datetime.now().date()
    date=0
    date1=0
    date2=0
    date3=0

    #print (last_oid,last_id,"after");

    if (len(cheap_list) != 0):
        date1 = cheap_list[0][0][0]
    if (len(normal_list) != 0):
        date2 = normal_list[0][0][0]
    if (len(expensive_list) != 0):
        date3 = expensive_list[0][0][0]
        
    if (date1!=0):
        #print("dupa",date1,date2,date3)
        date=date1
    elif (date2!=0):
        #print("dupa",date1,date2,date3)
        date=date2
    elif(date3!=0):
        #print("dupa",date1,date2,date3)
        date=date3
    if (date!=0):

        #filename = 'C:\\selenium\\PC\\'+'raporty'+'.txt' #for one big raports
        filename = selenium_url + 'PC/' +'raporty'+str(today)+'.txt' #for new raports
        #filename = 'C:\\selenium\\PC\\'+'raporty'+str(today)+'.txt' #for new raports
        
        with open(filename,'a', newline='') as f:
            writer = csv.writer(f, delimiter=' ')
            writer.writerow("Below Price Channel:")
            for i in range(len(cheap_list)):
                writer.writerow(cheap_list[i])
            writer.writerow("")
            writer.writerow("In Price Channel:")
            for i in range(len(normal_list)):
                writer.writerow(normal_list[i])
            writer.writerow("")
            writer.writerow("Above Price Channel:")
            for i in range(len(expensive_list)):
                writer.writerow(expensive_list[i])
            writer.writerow("")
    else:
        print("Something wrong with date", date)

def main ():

    global last_oid,last_id, max_value
    #print(select_last_from_mysql_db("raport"),"sasa")
    last_oid,last_id = select_last_from_mysql_db("raport")
    #max_value=0;
    max_value=[];
    #print (last_oid,last_id,"main")
    read_raports()
    
    #print(super_data)
    #print("nic")

def insert_into_mysql_db(last_oid,last_id,output):

    database = "raport"
    #print(last_oid,last_id)
    temp_oid=last_oid+1
    temp_id=last_id+1
    #print(temp_oid,temp_id)
    sql = "INSERT INTO raport (raport_oid, raport_id, date, company_name, current_value, current_status,previous_status,Streak,special_value,Perct_special_value,bottom_price_channel, upper_price_channel, max_value) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    #val = (temp_oid,temp_id,"20190205","Hydrotor","20","low","in","5","15","20","50","100")

    val = (temp_oid,temp_id,output[0],output[1],output[3],output[5],output[7],output[9],output[11],output[13],output[15],output[17],output[18])
    mycursor.execute(sql, val)
    mydb.commit()
    
    last_oid,last_id = select_last_from_mysql_db("raport")
    
    #print(mycursor.rowcount, "record inserted.")

def check_if_record_already_exist(output):

    table_name ="raport"
    #sql = "select *" + " from " + "apkadb."+table_name + " where date" +"='" +str(output[0]) +"' and company_name"+ "='" + str(output[1]+"'")
    sql = "select *" + " from " + database_param + "." + table_name + " where date" + "='" + str(output[0]) + "' and company_name" + "='" + str(output[1] + "'")
    #print (sql)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    
    #print (len(myresult))
    if (len(myresult)>0):
        return True
    else:
        return False

def import_names_from_file():

    #filename = 'C:\\selenium\\companies.txt'
    filename = 'companies.txt'
    with open(filename,'r') as f:
        reader =csv.reader(f)
        for row in (list(reader)):
            companies_list.append(row)

def import_data_from_file(company_name):
    
    i = 0;
    timelapse=20000 # 2 lata dla analizy na 1 rok
    #super_data = []
    #filename = 'C:\\selenium\\'+company_name+'.csv' # stooq data
    filename = selenium_url + 'ALL/'+company_name+'.mst' # BOS data
    #filename = 'C:\\selenium\\ALL\\'+company_name+'.mst' # BOS data
    with open(filename,'r') as f:
        reader =csv.reader(f)
        company_data_from_two_years
        company_data_from_two_years.clear()
        #print(super_data)
        f.readline()
        temporary_number=0
        j = 0;
        for row in reversed(list(reader)):
         #   if (j<=temporary_number):
         #(int(todayStr2)-10000)
            if ((int(todayStr2)-timelapse)<=int(row[1])):
                company_data_from_two_years.append(row)
                    #print(super_data[0])
                    #print (super_data[i][1])
                i+=1
            else:
                break
          #  j+=1
        #print(super_data)
    for i in range (len(company_data_from_two_years)):
        for j in range (1, len(company_data_from_two_years[i])):
            #if (isinstance(super_data[i][j], str)):
            # print("dupa")
                #break
            #print(super_data)
            company_data_from_two_years[i][j]=float(company_data_from_two_years[i][j])

main()
