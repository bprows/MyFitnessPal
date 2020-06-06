import myfitnesspal
from datetime import date
import pandas as pd
from sqlalchemy import create_engine

# Set up client to call REST API
username = 'brodyprows97'
# Gets dates
todays_date = date.today()
start_date = date(2019, 9, 15)


def get_weight(user, start_day):
    print("Setting up client for %s. \n" % username)
    client = myfitnesspal.Client(user)
    print("Getting data from %s to %s \n" % (start_day, date.today()))
    weight = client.get_measurements('Weight', start_day)
    # weight is an ordered dict. ew.
    date_list = list(weight.keys())
    weight_list = list(weight.values())
    # Create DataFrame from lists
    df = pd.DataFrame(list(zip(date_list, weight_list)), columns=['date', 'weight'])
    df['username'] = user
    return df


df = pd.DataFrame({"date": [],
                   "username": [],
                   "weight": []})

df = df.append(get_weight(username, start_date))


tableName = 'weight'
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

    print("Succesful upload to %s for dates since %s\n" % (tableName, start_date));

finally:

    dbConnection.close()
