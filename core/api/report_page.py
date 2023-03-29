import mysql.connector
from mysql.connector import errorcode
import os
import json
import csv
import pathlib

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../../datasets").resolve()


with open(os.path.join(os.getcwd(), 'core/connections/config.json')) as json_data_file:
    config = json.load(json_data_file)

# connect to the database
cnx = mysql.connector.connect(user=config['user'], password=config['password'],
                              host=config['host'], database=config['dbname'])

# create a cursor object
cursor = cnx.cursor()

# execute a query


# def execute_query(query):
#     cursor.execute(query)


DB_NAME = config['dbname']


def report_table_query(year):
    query = """
    SELECT
  @rownum := @rownum + 1 AS ID,
  CONCAT(category, ' - ', reason) AS TITLE,
  COALESCE(SUM(CASE MONTH(import_date) WHEN 1 THEN `import` END), '') AS JAN,
  COALESCE(SUM(CASE MONTH(import_date) WHEN 2 THEN `import` END), '') AS FEB,
  COALESCE(SUM(CASE MONTH(import_date) WHEN 3 THEN `import` END), '') AS MAR,
  COALESCE(SUM(CASE MONTH(import_date) WHEN 4 THEN `import` END), '') AS APR,
  COALESCE(SUM(CASE MONTH(import_date) WHEN 5 THEN `import` END), '') AS MAY,
  COALESCE(SUM(CASE MONTH(import_date) WHEN 6 THEN `import` END), '') AS JUN,
  COALESCE(SUM(CASE MONTH(import_date) WHEN 7 THEN `import` END), '') AS JUL,
  COALESCE(SUM(CASE MONTH(import_date) WHEN 8 THEN `import` END), '') AS AUG,
  COALESCE(SUM(CASE MONTH(import_date) WHEN 9 THEN `import` END), '') AS SEP,
  COALESCE(SUM(CASE MONTH(import_date) WHEN 10 THEN `import` END), '') AS OCT,
  COALESCE(SUM(CASE MONTH(import_date) WHEN 11 THEN `import` END), '') AS NOV,
  COALESCE(SUM(CASE MONTH(import_date) WHEN 12 THEN `import` END), '') AS 'DEC'
FROM
  life_cost_management.import,
  (SELECT @rownum := 0) r
WHERE YEAR(import_date) = %s
GROUP BY
  category,
  reason
ORDER BY
  category,
  reason
    """
    try:
        print("Extracting data by group-concat from {}: ".format('import table'), end='')
        cursor.execute(query, (year,))
        # Retrieve the results
        # for result in cursor:
        #     print(result)
        # Open a CSV file and write the results to it
        with open(DATA_PATH.joinpath('report_{}.csv'.format(year)), 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([i[0]
                               for i in cursor.description])  # Write headers
            csvwriter.writerows(cursor)
        response = True
        return response
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
            return False
        else:
            print(err.msg)
            return False
