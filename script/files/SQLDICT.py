def getdict():

    sql_dict ={
        # 'maxoids' : "select " + "max(" + table_name + "_oid)" + "," + "max(" + table_name + "_id)" + " from " + database_param + "." + table_name,
        'maxoids': 'select max(raport_oid), max(raport_id) from raport'
    }

    return  sql_dict