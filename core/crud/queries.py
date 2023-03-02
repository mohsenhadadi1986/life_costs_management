import mysql.connector
from mysql.connector import errorcode
# from connections.connector import execute_query, cnx, cursor
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

QUERIES = {}

QUERIES['insert_meta_info'] = ("INSERT INTO meta_info "
                               "(category, reason) "
                               "VALUES (%s, %s)")

insert_meta_info = [('Cost', 'Travelling'), ('Cost', 'Other')]

QUERIES['all_options_dropdown'] = """
    SELECT category, GROUP_CONCAT(reason SEPARATOR ',') AS reasons
    FROM life_cost_management.meta_info
    GROUP BY category
"""

all_options = {}
for category, reasons in cursor:
    all_options[category] = reasons.split(',')

print(all_options)

for query_name in QUERIES:
    query_description = QUERIES[query_name]
    for data in insert_meta_info:
        try:
            print("Inserting data in to table {}: ".format(query_name), end='')
            execute_query(query_description, data)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
    else:
        print("OK")

cursor.close()
cnx.close()
