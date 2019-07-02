import mysql.connector
import csv

sql_check_if_user_exists = "select * from users where user_name = %s;"
sql_create_user = "INSERT INTO users (users_oid , users_id , user_name ) values (%s,%s,%s) ;"
sql_select_last_user = "select max(users_oid) from users;"
sql_get_user_oid_from_user_name = "select users_oid from users where user_name = %s;"
sql_select_last_transaction_for_user = "select * from transactions where transactions_oid in (select max(TRANSACTIONs_oid) from transactions where users_oid=%s) and db_status > 0;"
sql_select_all_user_transactions = "select * from transactions where users_oid = %s and db_status > 0;"
sql_select_all_last_transactions = "select max(transactions_oid) from transactions;"
sql_create_new_transaction = "INSERT INTO transactions (transactions_oid, transactions_id, users_oid, company_name, buy_price, quantity , date, db_status) values (%s,%s,%s,%s,%s,%s,%s, %s);"
sql_select_all_user_transactions_with_SELL = ""
sql_remove_transaction = "update transactions set db_status = -1 where transactions_oid = %s"
sql_select_all_newest_raport_data_with_current_user_transaction_companies = ""
sql_select_newest_price_from_company = "select current_value from raport where company_name = %s and date in (select max(date) from raport where company_name= %s);"
sql_select_newest_status_from_company = "select current_status from raport where company_name = %s and date in (select max(date) from raport where company_name= %s);"
sql_select_newest_previous_status_from_company = "select previous_status from raport where company_name = %s and date in (select max(date) from raport where company_name= %s);"
sql_select_newest_max_value_from_company = "select max_value from raport where company_name = %s and date in (select max(date) from raport where company_name= %s);"

mydb = mysql.connector.connect(
 host=" remotemysql.com",
 user="zr00HYpK6O",
 passwd="SOdKgWqLJr",
 database="zr00HYpK6O"
)
mycursor = mydb.cursor()


def main():

    while True:
        print("Please LOG IN into the system or Register:")
        print("1: LOG IN")
        print("2: REGISTER")
        print("3: EXIT")

        choice = input()

        if choice == "1":
            login()
            print("Logged In")
        if choice == "2":
            register()
            print("Registered")
        if choice == "3":
            break


def register():

    print("Please register your username:")
    user_name = input()
    mycursor.execute(sql_select_last_user)
    last_user = mycursor.fetchone()[0]

    if (len(user_name)) == 0:
        print("User name can't be empty")
        return

    if last_user is None:
        last_user = 0
    else:
        last_user += 1

    mycursor.execute(sql_check_if_user_exists, (user_name,))
    temp_if_user_exist = mycursor.fetchall()

    if len(temp_if_user_exist) == 0:

        sql_values_to_pass = (last_user, last_user + 1, str(user_name))
        mycursor.execute(sql_create_user, sql_values_to_pass)
        mydb.commit()

    else:
        print("User already taken!")
        return

    print("You have been registered!")
    return


def login():

    print("Please insert your username:")
    user_name = input()

    if (len(user_name)) == 0:
        print("User name can't be empty")
        return

    mycursor.execute(sql_check_if_user_exists, (user_name,))
    temp_if_user_exist = mycursor.fetchall()

    if len(temp_if_user_exist) == 0:

        print("User not registered!")
        return
    else:
        print("Welcome " + user_name + "!")
        transactions(user_name)


def transactions(user_name):

    while True:

        print("Please choose from one of the options:")
        print("1: Register new transaction")
        print("2: Show last transaction")
        print("3: Show all transactions")
        print("4: Show all transactions that are sellable for you")
        print("5: Show all transactions that are sellable right now (You could not have any of those)")
        print("6: Remove one transactions")
        print("7: Remove all transactions")
        print("8: LOG-OUT")
        user_choice = input()

        if user_choice == "1":
            add_user_transactions(user_name)
        if user_choice == "2":
            show_last_user_transaction(user_name)
        if user_choice == "3":
            show_all_user_transactions(user_name)
        if user_choice == "4":
            show_all_user_transactions_sellable(user_name)
        if user_choice == "5":
            show_all_transactions_sellable()
        if user_choice == "6":
            remove_user_transaction(user_name)
        if user_choice == "7":
            remove_all_user_transaction(user_name)
        if user_choice == "8":
            break


def add_user_transactions(user_name):

    # fetching last_transaction_oid and id
    mycursor.execute(sql_select_all_last_transactions)
    last_transaction = mycursor.fetchone()[0]
    if last_transaction is None:
        temp_new_last_transactions_oid = 0
    else:
        temp_new_last_transactions_oid = last_transaction+1
    temp_new_last_transactions_id = temp_new_last_transactions_oid+1

    # fetching user_oid
    mycursor.execute(sql_get_user_oid_from_user_name, (user_name,))
    temp_user_oid = int(mycursor.fetchone()[0])

    print(str(temp_new_last_transactions_oid) + " " + str(temp_new_last_transactions_id) + " " + str(temp_user_oid))

    # fetching company_name
    company_choice = select_company()

    if company_choice == -1:
        return

    # fetching buy_price
    price_choice = insert_buying_price()

    if price_choice == -1:
        return

    # fetching quantity
    quantity_choice = insert_quantity()

    if quantity_choice == -1:
        return

    # fetching quantity
    date_choice = insert_date()

    if date_choice == -1:
        return

    val_to_pass = (temp_new_last_transactions_oid, temp_new_last_transactions_id, temp_user_oid, company_choice, price_choice, quantity_choice, date_choice, 1)
    mycursor.execute(sql_create_new_transaction, val_to_pass)
    mydb.commit()
    print("Transaction added!")


def insert_date():

    print("Please insert date of transaction (format YYYYMMDD e.g. 19991224 - 1999 / 12 / 24)")
    date_choice = int(input())

    if date_choice <= 19000101:
        print("Date can't be earlier then 1900/01/01")
        return -1

    return date_choice


def insert_quantity():

    print("Please insert bought quantity")
    quantity_choice = int(input())

    if quantity_choice <= 0:
        print("Quantity can't be lower or equal to 0")
        return -1

    return quantity_choice


def insert_buying_price():

    print("Please insert buying price (format NN.nnnn e.g. 65.4321)")
    price_choice = float(input())

    if price_choice <= 0:
        print("Price can't be lower or equal to 0")
        return -1

    return price_choice


def select_company():

    comp_list_str = ""
    comp_list = []

    filename = 'companies.txt'
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in (list(reader)):
            comp_list_str += str((row[0])) + ", "
            comp_list.append(row[0])

    print("Please write one of the names from following list:")
    print(comp_list_str)

    company_choice = input().upper()
    if company_choice in comp_list:
        return company_choice
    else:
        print("Error: unknown company name!")

    return -1


def show_last_user_transaction(user_name):
    mycursor.execute(sql_get_user_oid_from_user_name, (user_name,))
    temp_user_oid = str(mycursor.fetchone()[0])

    mycursor.execute(sql_select_last_transaction_for_user, (temp_user_oid,))
    temp_user_transactions = mycursor.fetchone()

    print(temp_user_transactions)
    return


def show_all_user_transactions(user_name):

    mycursor.execute(sql_get_user_oid_from_user_name, (user_name,))
    temp_user_oid = str(mycursor.fetchone()[0])

    mycursor.execute(sql_select_all_user_transactions, (temp_user_oid,))
    temp_user_transactions = mycursor.fetchall()

    for transaction in temp_user_transactions:
        current_price = float(get_current_price(transaction[3]))
        user_price = float(transaction[4])
        print(str(transaction) + " | Current Price: "+str(current_price) + "  | Your value compared to bought price: " + str(format(current_price/user_price*100, ".2f")) + "%")


def remove_user_transaction(user_name):

    user_transaction_numbers = []
    mycursor.execute(sql_get_user_oid_from_user_name, (user_name,))
    temp_user_oid = str(mycursor.fetchone()[0])

    mycursor.execute(sql_select_all_user_transactions, (temp_user_oid,))
    temp_user_transactions = mycursor.fetchall()

    print("Transaction_oid | Transaction_id | User_oid | Company_name | Buy_value | Quantity | Date")
    for transaction in temp_user_transactions:
        user_transaction_numbers.append(transaction[0])
        print(transaction)

    print("Please choose transaction_oid for removal!")
    remove_choice = int(input())

    print(user_transaction_numbers)
    if remove_choice not in user_transaction_numbers:
        print("You can't remove other users transactions")

    elif remove_choice in user_transaction_numbers:
        mycursor.execute(sql_remove_transaction, (remove_choice,))
        mydb.commit()
        print("Transaction have been removed")

    else:
        print("Error something is wrong")
    return


def remove_all_user_transaction(user_name):

    print("ARE YOU SURE? (y/n)")
    remove_choice = str(input())

    if remove_choice == "y":

        mycursor.execute(sql_get_user_oid_from_user_name, (user_name,))
        temp_user_oid = str(mycursor.fetchone()[0])

        mycursor.execute(sql_select_all_user_transactions, (temp_user_oid,))
        temp_user_transactions = mycursor.fetchall()

        for transaction in temp_user_transactions:
            mycursor.execute(sql_remove_transaction, (transaction[0],))
            mydb.commit()
        print("Transactions have been removed")
    return


def show_all_transactions_sellable():

    comp_list = []
    filename = 'companies.txt'
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in (list(reader)):
            comp_list.append(row[0])
            current_price = float(get_current_price(str(row[0])))
            current_max_value_price = float(get_max_value(str(row[0])))
            current_status = str(get_current_status(str(row[0])))
            # previous_status = str(get_previous_status(str(row[0])))

            if current_status == "low":
                print(str(row[0] + " - STRONG BUY"))

            if (current_status == "upper") and (current_price > current_max_value_price):
                print(str(row[0] + " - POSSIBLE HIGH SELL"))

            else:
                print(str(row[0]) + " - SOMETHING IN BETWEEN!")

            # print (str(row[0] + " " + str(current_price) + " " + str(current_max_value_price) + " " + current_status))

    return


def show_all_user_transactions_sellable(user_name):

    # if ((output[5]=="upper") and (float(output[3])>float(output[18])))
    # elif ((output[5] == "upper") and (float(output[3]) <= float(output[18]))):

    mycursor.execute(sql_get_user_oid_from_user_name, (user_name,))
    temp_user_oid = str(mycursor.fetchone()[0])

    mycursor.execute(sql_select_all_user_transactions, (temp_user_oid,))
    temp_user_transactions = mycursor.fetchall()

    for transaction in temp_user_transactions:
        current_price = float(get_current_price(transaction[3]))
        current_max_value_price = float(get_max_value(transaction[3]))
        current_status = str(get_current_status(transaction[3]))
        user_price = float(transaction[4])

        if (current_status == "upper") and (current_price > current_max_value_price) and current_price > user_price:
            print(str(transaction) + " | Current Price: " + str(current_price) + "  | Your value compared to bought price: " + str(format(current_price/user_price*100, ".2f")) + "%" + " - TIME TO SELL!")

        if (current_status == "upper") and (current_price <= current_max_value_price) and current_price > user_price:
            print(str(transaction) + " | Current Price: " + str(current_price) + "  | Your value compared to bought price: " + str(format(current_price / user_price * 100, ".2f")) + "%" + " - profitable but not optimized sell!")


def get_previous_status(company_name):

    # previous_status = 0

    mycursor.execute(sql_select_newest_previous_status_from_company, (company_name, company_name))
    previous_status = mycursor.fetchone()[0]

    return previous_status


def get_current_status(company_name):

    # current_status = 0;

    mycursor.execute(sql_select_newest_status_from_company, (company_name, company_name))
    current_status = mycursor.fetchone()[0]

    return current_status


def get_max_value(company_name):

    # max_value = 0;
    mycursor.execute(sql_select_newest_max_value_from_company, (company_name, company_name))
    max_value = mycursor.fetchone()[0]

    return max_value


def get_current_price(company_name):

    # current_price = 0;

    mycursor.execute(sql_select_newest_price_from_company, (company_name, company_name))
    current_price = mycursor.fetchone()[0]

    return current_price


main()
