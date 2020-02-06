import mysql.connector


def main():
    host_param = "remotemysql.com"
    user_param = "wdswq04F2c"
    passwd_param = "eMlH63DR0s"
    database_param = "wdswq04F2c"

    mydb = mysql.connector.connect(
        host=host_param,
        user=user_param,
        passwd=passwd_param,
        database=database_param
    )

    sql_cursor = mydb.cursor()

    return mydb,sql_cursor,database_param
