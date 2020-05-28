import pandas as pd
import mysql.connector
from sqlalchemy import create_engine
import pymysql.cursors

# mydb = mysql.connector.connect(
#   host="mfp.cnx1wcpcowpl.us-east-2.rds.amazonaws.com",
#   user="mfp_brody",
#   passwd="mfp_brody",
#   database="mfp"
# )
#
# print(mydb)

sqlEngine       = create_engine('mysql+pymysql://mfp_brody:mfp_brody@mfp.cnx1wcpcowpl.us-east-2.rds.amazonaws.com:3306/mfp', pool_recycle=3600)
dbConnection    = sqlEngine.connect()
sql = 'select * from mfp.foods'
rs = dbConnection.execute(sql)
print(rs)

# mycursor = mydb.cursor()
#
# mycursor.execute("SELECT * FROM foods")
#
# myresult = mycursor.fetchall()
#
# for x in myresult:
#   print(x)
#
# print(myresult)
#
# df = pd.read_sql("select * from foods", mydb)
# print(df)
