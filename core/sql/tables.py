
import mysql.connector
from mysql.connector import errorcode
# from connections.connector import execute_query, cnx, cursor
import os
import json

import mysql.connector

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

TABLES = {}
TABLES['import'] = (
    "CREATE TABLE `import` ("
    "  `id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `category` varchar(14) NOT NULL,"
    "  `reason` varchar(16) NOT NULL,"
    "  `import` int(11) NOT NULL,"
    "  `import_date` date NOT NULL,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")

TABLES['meta_info'] = (
    "CREATE TABLE `meta_info` ("
    "  `id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `category` varchar(16) NOT NULL,"
    "  `reason` varchar(16) NOT NULL,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")


for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        print("Creating table {}: ".format(table_name), end='')
        execute_query(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

cursor.close()
cnx.close()
