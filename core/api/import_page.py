import mysql.connector
from mysql.connector import errorcode
from core.connections.connector import cnx, cursor


# def execute_query(query, data=[]):
#     cursor.execute(query, data)
#     cnx.commit()


def execute_function(proc_name, data=[]):
    cursor.callproc(proc_name, data)
    cnx.commit()


def import_dropdown_query():
    # query = """
    # SELECT category, GROUP_CONCAT(reason SEPARATOR ',') AS reasons
    # FROM life_cost_management.meta_info
    # GROUP BY category
    # """
    procedure_name = 'get_meta_info_dropdown_options'
    try:
        print("Extracting data by group-concat {}: ".format('all_options_dropdown'), end='')
        # execute_query(query, data=[])
        execute_function(procedure_name)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    all_options = {}
    for result in cursor.stored_results():
        fetch_options_list = result.fetchall()
        for category, reasons in fetch_options_list:
            all_options[category] = reasons.split(',')
    return all_options


def import_data_query(import_list):
    # query = '''
    # INSERT INTO import
    #                 (category, reason, import, import_date)
    #                 VALUES (%s, %s, %s, %s)
    # '''
    procedure_name = 'insert_import'
    try:
        print("Inserting data in to table {}: ".format('import'), end='')
        # execute_query(query, import_list)
        execute_function(procedure_name, import_list)
        response = True
        return response
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
            return False
        else:
            print(err.msg)
            return False
