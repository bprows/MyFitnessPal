import myfitnesspal
from datetime import date, timedelta
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine
import pymysql


# Set up client to call REST API
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
todays_date = date.today()
streak = timedelta(days=252)
curr_date = start_date = todays_date - streak


print("Getting data from %s to %s \n" % (start_date,todays_date))
while curr_date <= todays_date - delta:
    if curr_date.day == 1:
        print("At %s" % curr_date)

    # Get data for curr_date
    day = client.get_date(curr_date.year, curr_date.month, curr_date.day)
    this_date = str(curr_date.year) + '-' + str(curr_date.month) + '-' + str(curr_date.day)
    for meal in range(len(day.meals)):
        meal_name = day.meals[meal].name
        for e in range(len(day.meals[meal].entries)):
            this_entry = day.meals[meal].entries[e]
            this_food = pd.DataFrame({"date": [this_date],
                                      "username": [username],
                                      "meal": [meal_name],
                                      "food": this_entry._short_name if this_entry._short_name == None else this_entry._short_name.strip(), # might need to chop this down to 45 chars
                                      "unit": this_entry.unit,
                                      "quantity": this_entry.quantity,
                                      'calories': this_entry.totals['calories'],
                                      'carbohydrates': this_entry.totals['carbohydrates'],
                                      'fat': this_entry.totals['fat'],
                                      'protein': this_entry.totals['protein'],
                                      'sodium': this_entry.totals['sodium'],
                                      'sugar': this_entry.totals['sugar']})
            df = df.append(this_food)
    # increment curr_date
    curr_date += delta


tableName = 'foods'
print("Appending to %s if exists."%tableName)

# sqlEngine       = create_engine('mysql+pymysql://mfp_boy:mfp_boy@localhost:3306/mfp', pool_recycle=3600)
sqlEngine       = create_engine('mysql+pymysql://mfp_brody:mfp_brody@mfp.cnx1wcpcowpl.us-east-2.rds.amazonaws.com:3306/mfp', pool_recycle=3600)
dbConnection    = sqlEngine.connect()


try:

    frame           = df.to_sql(tableName, dbConnection, if_exists='append', index = False);

except ValueError as vx:

    print(vx)

except Exception as ex:

    print(ex)

else:

    print("Succesful upload to %s for dates %s to %s \n" % (tableName,start_date,todays_date));

finally:

    dbConnection.close()
