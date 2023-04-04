import mysql.connector
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

# def execute_query(query):
#     cursor.execute(query)
# cursor.close()
# cnx.close()


# fetch the data and print it
# for row in cursor.fetchall():
#     print(row)

# close the cursor and connection
