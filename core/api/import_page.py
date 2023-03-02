import mysql.connector
from mysql.connector import errorcode
import os
import json


with open(os.path.join(os.getcwd(), 'core/connections/config.json')) as json_data_file:
    config = json.load(json_data_file)

# connect to the database
cnx = mysql.connector.connect(user=config['user'], password=config['password'],
                              host=config['host'], database=config['dbname'])

# create a cursor object
cursor = cnx.cursor()

# execute a query


def execute_query(query, data=[]):
    cursor.execute(query, data)
    cnx.commit()


DB_NAME = config['dbname']


def import_dropdown_query():
    query = """
    SELECT category, GROUP_CONCAT(reason SEPARATOR ',') AS reasons
    FROM life_cost_management.meta_info
    GROUP BY category
    """
    try:
        print("Extracting data by group-concat {}: ".format('all_options_dropdown'), end='')
        execute_query(query, data=[])
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    all_options = {}
    for category, reasons in cursor:
        all_options[category] = reasons.split(',')
    return all_options


def import_data_query(import_list):
    query = '''
    INSERT INTO import
                    (category, reason, import, import_date)
                    VALUES (%s, %s, %s, %s)
    '''
    try:
        print("Inserting data in to table {}: ".format('import'), end='')
        execute_query(query, import_list)
        response = True
        return response
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
            return False
        else:
            print(err.msg)
            return False
