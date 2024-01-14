class SQLClass:
    def __init__(self, cursor, db, databaseparam):

        self.mycursor = cursor
        self.mydb = db
        self.database_param = databaseparam

    def insert_into_mysql_db(self, last_oid_param, last_id_param, output):

        temp_oid = last_oid_param+1
        temp_id = last_id_param+1
        sql = "INSERT INTO raport (raport_oid, raport_id, date, company_name, current_value, current_status,previous_status,Streak,special_value,Perct_special_value,bottom_price_channel, upper_price_channel, max_value) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        # val = (temp_oid,temp_id,"20190205","Hydrotor","20","low","in","5","15","20","50","100")

        val = (temp_oid, temp_id, output[0], output[1], output[3], output[5], output[7], output[9], output[11], output[13], output[15], output[17], output[18])
        self.mycursor.execute(sql, val)
        self.mydb.commit()


    def check_if_record_already_exist(self, output):

        table_name = "raport"
        # sql = "select *" + " from " + "apkadb."+table_name + " where date" +"='" +str(output[0]) +"' and company_name"+ "='" + str(output[1]+"'")
        sql = "select *" + " from " + self.database_param + "." + table_name + " where date" + "='" + str(output[0]) + "' and company_name" + "='" + str(output[1] + "'")
        self.mycursor.execute(sql)
        myresult = self.mycursor.fetchall()

        if len(myresult) > 0:
            return True
        else:
            return False


    def check_if_record_already_exist_2(self, date, company_name):

        table_name = "raport"
        sql = "select *" + " from " + self.database_param + "." + table_name + " where date" + "='" + str(date) + "' and company_name" + "='" + str(company_name) + "'"
        self.mycursor.execute(sql)
        myresult = self.mycursor.fetchall()
        if len(myresult) > 0:
            return True
        else:
            return False

    def select_last_from_mysql_db(self, table_name):

        sql = "select " + "max(" + table_name + "_oid)" + "," + "max(" + table_name + "_id)" + " from " + self.database_param + "." + table_name
        self.mycursor.execute(sql)
        myresult = self.mycursor.fetchall()
        temp1, temp2 = myresult[0]
        if str(temp1) == "None":
            return -1, 0
        else:
            return myresult[0]