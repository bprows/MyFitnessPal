import myfitnesspal
from datetime import date, timedelta
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine
import pymysql.cursors
from food_day import food_day

username = 'brodyprows97'
print("Setting up client for %s. \n" % username)
client = myfitnesspal.Client(username)

df = pd.DataFrame({"date": [],
                   "meal": [],
                   "food": [],
                   'calories': [],
                   'carbohydrates': [],
                   'fat': [],
                   'protein': [],
                   'sodium': [],
                   'sugar': []})

# Gets dates
delta = timedelta(days=1)
yesterdays_date = date.today() - delta


print("Getting data from %s \n" % (yesterdays_date))
day = client.get_date(yesterdays_date.year, yesterdays_date.month, yesterdays_date.day)
this_date = str(yesterdays_date.year) + '-' + str(yesterdays_date.month) + '-' + str(yesterdays_date.day)
for meal in range(len(day.meals)):
    meal_name = day.meals[meal].name
    for e in range(len(day.meals[meal].entries)):
        food_name = None
        if day.meals[meal].entries[e]._short_name:
            food_name = day.meals[meal].entries[e]._short_name.strip()
        else:
            food_name = day.meals[meal].entries[e].name
        this_food = pd.DataFrame({"date": [this_date],
                                  "username": [username],
                                  "meal": [meal_name],
                                  "food": food_name, # might need to chop this down to 45 chars
                                  "unit": day.meals[meal].entries[e].unit,
                                  "quantity": day.meals[meal].entries[e].quantity,
                                  'calories': day.meals[meal].entries[e].totals['calories'],
                                  'carbohydrates': day.meals[meal].entries[e].totals['carbohydrates'],
                                  'fat': day.meals[meal].entries[e].totals['fat'],
                                  'protein': day.meals[meal].entries[e].totals['protein'],
                                  'sodium': day.meals[meal].entries[e].totals['sodium'],
                                  'sugar': day.meals[meal].entries[e].totals['sugar']})
        df = df.append(this_food)

tableName = 'foods'
print("Appending to %s if exists"%tableName)

# sqlEngine       = create_engine('mysql+pymysql://mfp_boy:mfp_boy@localhost:3306/mfp', pool_recycle=3600)
sqlEngine       = create_engine('mysql+pymysql://mfp_brody:mfp_brody@mfp.cnx1wcpcowpl.us-east-2.rds.amazonaws.com:3306/mfp', pool_recycle=3600)
dbConnection    = sqlEngine.connect()

try:
    print("Deleting data from %s" % yesterdays_date)
    # delete any data from yesterday
    sql = "DELETE FROM mfp.foods WHERE date = %s and username = %s;"
    rs = dbConnection.execute(sql, (yesterdays_date, username))

    print("Adding data from %s" % yesterdays_date)
    # Add all the data from yesterday.
    frame           = df.to_sql(tableName, dbConnection, if_exists='append', index = False);

except ValueError as vx:

    print(vx)

except Exception as ex:

    print(ex)

else:

    print("Succesful upload to %s for %s \n" % (tableName,yesterdays_date));

finally:

    dbConnection.close()
