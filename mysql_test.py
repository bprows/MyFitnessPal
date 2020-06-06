import mysql.connector
from mysql.connector import Error
from sqlalchemy import create_engine


# sqlEngine       = create_engine('mysql+pymysql://mfp_brody:mfp_brody@mfp.cnx1wcpcowpl.us-east-2.rds.amazonaws.com:3306/mfp', pool_recycle=3600)
# dbConnection    = sqlEngine.connect()
# sql = 'select * from mfp.foods'
# rs = dbConnection.execute(sql)
# print(rs)

username = 'brodyprows97'

try:
    connection = mysql.connector.connect(host='mfp.cnx1wcpcowpl.us-east-2.rds.amazonaws.com',
                                         database='mfp',
                                         user='mfp_brody',
                                         password='mfp_brody')

    sql_select_Query = "select food_update from users where username = '%s'" % username
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    food_update = cursor.fetchall()
    print("The retrieved date is: ", food_update)

except Error as e:
    print("Error reading data from MySQL table", e)
finally:
    if (connection.is_connected()):
        connection.close()
        cursor.close()
        print("MySQL connection is closed")