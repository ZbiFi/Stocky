# Username: zr00HYpK6O
#
# Database name: zr00HYpK6O
#
# Password: SOdKgWqLJr
#
# Server: remotemysql.com
#
# Port: 3306

import mysql.connector

# mydb = mysql.connector.connect(
# host=" remotemysql.com",
# user="zr00HYpK6O",
# passwd="SOdKgWqLJr",
# database="zr00HYpK6O"
# )
#
# mycursor = mydb.cursor()
#
# sql = "CREATE TABLE IF NOT EXISTS table_name ( column1 VARCHAR(255) , column2 VARCHAR(255), column3 VARCHAR(255))"
# sql2 = "insert into table_name ( column1 , column2, column3) values (%s,%s,%s)"
# sql3 = (1,2,3)
# sql4 = "select * from table_name"
# sql5 = "drop table table_name"
#
# mycursor.execute(sql5)
# mydb.commit()
# mycursor.execute(sql)
# mydb.commit()
# mycursor.execute(sql2,sql3)
# mydb.commit()
# mycursor.execute(sql4)
# myresult = mycursor.fetchall()
# print (myresult)

mydb = mysql.connector.connect(
host = " remotemysql.com",
user = "wdswq04F2c",
passwd = "eMlH63DR0s",
database = "wdswq04F2c"
)

sql1 = "CREATE TABLE IF NOT EXISTS raport ( raport_oid int(11), raport_id int(11), date int(11), company_name varchar(45), current_value float, current_status varchar(45), previous_status varchar(45) , Streak int(11), special_value float, Perct_special_value float, bottom_price_channel float, upper_price_channel float, max_value float)"
sql5 = "drop table if exists raport"
sql6 = "INSERT INTO raport (raport_oid, raport_id, date, company_name, current_value, current_status,previous_status,Streak,special_value,Perct_special_value,bottom_price_channel, upper_price_channel, max_value) VALUES (1,2,3,4,5,6,7,8,9,10,11,12,13)"
sql4 = "select * from raport"
sql7 = "CREATE TABLE IF NOT EXISTS users (users_oid int(11), users_id int(11), user_name varchar (45))"
sql75 = "drop table if exists users"
sql8 = "select * from users"
sql9 = "CREATE TABLE IF NOT EXISTS transactions (transactions_oid int(11), transactions_id int(11), users_oid varchar (45), company_name varchar(45), buy_price float, quantity int(11), date int(11), db_status int (11))"
sql95 = "drop table if exists transactions"
sql10 = "select * from transactions"

mycursor = mydb.cursor()

#mycursor.execute(sql5)
#mycursor.execute(sql1)
#mycursor.execute(sql6)
#mycursor.execute(sql4)
#mycursor.execute(sql95)

#mycursor.execute(sql7)
#mycursor.execute(sql8)

mycursor.execute(sql9)
#mycursor.execute(sql95)
#mycursor.execute(sql10)

myresult = mycursor.fetchall()

print (myresult)


