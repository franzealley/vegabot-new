# import the mysql client for python

import pymysql

connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='',
                             port=8888
                             )

cursor = connection.cursor(buffered=True)

query = ("CREATE DATABASE Vegabot")

cursor.execute(query)
print('here')

for item in cursor:
    print(item)

#connection.cursor().execute('create database Vegabot')

# # Create a connection object
#
# databaseServerIP = "127.0.0.1"  # IP address of the MySQL database server
#
# databaseUserName = "root"  # User name of the database server
#
# databaseUserPassword = ""  # Password for the database user
#
# newDatabaseName = "Vegabot"  # Name of the database that is to be created
#
# charSet = "utf8mb4"  # Character set
#
# cursorType = pymysql.cursors.DictCursor
#
# connectionInstance = pymysql.connect(host=databaseServerIP, user=databaseUserName, password=databaseUserPassword,
#
#                                      charset=charSet, cursorclass=cursorType, port=80)
#
#
# try:
#
#     # Create a cursor object
#
#     cursorInsatnce = connectionInstance.cursor()
#
#     # SQL Statement to create a database
#
#     sqlStatement = "CREATE DATABASE " + newDatabaseName
#
#     # Execute the create database SQL statment through the cursor instance
#
#     cursorInsatnce.execute(sqlStatement)
#
#     # # SQL query string
#     #
#     # sqlQuery = "SHOW DATABASES"
#     #
#     # # Execute the sqlQuery
#     #
#     # cursorInsatnce.execute(sqlQuery)
#     #
#     # # Fetch all the rows
#     #
#     # databaseList = cursorInsatnce.fetchall()
#     #
#     # for database in databaseList:
#     #     print(database)
#
#
#
# except Exception as e:
#
#     print("Exeception occured:{}".format(e))
#
#
#
# finally:
#
#     connectionInstance.close()