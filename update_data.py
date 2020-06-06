import myfitnesspal
from datetime import date, timedelta
import pandas as pd
import mysql.connector
from mysql.connector import Error
from food_day import food_day
import numpy as np


# Will just need a valid username as input for this eventually
class Refreshments:

    def __init__(self, username):
        self.connection = self.establish_connection()
        self.username = username
        self.username, self.start_date, self.last_food, self.last_weight = self.get_info()[0]
        self.client = self.establish_client()
        self.delta = timedelta(days=1)


    def establish_connection(self):
        print("Connecting to mySQL on AWS")
        try:
            connection = mysql.connector.connect(host='mfp.cnx1wcpcowpl.us-east-2.rds.amazonaws.com',
                                                      database='mfp',
                                                      user='mfp_brody',
                                                      password='mfp_brody')
        except Error as e:
            print("Error Connecting to mySQL db", e)
        print("Connection Successful")
        return connection

    def get_info(self):
        try:
            sql_select_Query = "select * from users where username = '%s'" % self.username
            cursor = self.connection.cursor()
            cursor.execute(sql_select_Query)
            user_info = cursor.fetchall()
        except Error as e:
            print("Error reading data from MySQL table", e)

        return user_info


    def establish_client(self):
        print("Setting up myfitnesspal.Client for %s" % self.username)
        client = myfitnesspal.Client(self.username)
        print("Client created successfully")
        return client


    def get_foods(self):
        df = pd.DataFrame()
        todays_date = date.today()
        curr_date = self.last_food
        print("Getting date from %s to %s" % (curr_date, todays_date - self.delta))
        while curr_date <= todays_date - self.delta:
            curr_day = self.client.get_date(curr_date)
            df = df.append(food_day(curr_day, self.username))
            curr_date += self.delta
        return df


    def get_weight(self):
        weight = self.client.get_measurements('Weight', self.last_weight)
        # weight is an ordered dict. ew.
        date_list = list(weight.keys())
        weight_list = list(weight.values())
        # Create DataFrame from lists
        df = pd.DataFrame(list(zip(date_list, weight_list)), columns=['date', 'weight'])
        df['username'] = self.username
        return df


    def append_foods(self):
        foods_df = self.get_foods()
        first_new_day = np.min(foods_df.date)
        try:
            print("Deleting data since %s" % first_new_day)
            cursor = self.connection.cursor()
            sql_Delete_query = "DELETE FROM foods WHERE date >= %s and username = '%s';" \
                               % (first_new_day, self.username)
            cursor.execute(sql_Delete_query)
            self.connection.commit()

            # creating column list for insertion
            cols = "`,`".join([str(i) for i in foods_df.columns.tolist()])
            cursor = self.connection.cursor()
            # Insert DataFrame records one by one.
            for i, row in foods_df.iterrows():
                sql = "INSERT INTO `foods` (`" + cols + "`) VALUES (" + "%s," * (len(row) - 1) + "%s)"
                cursor.execute(sql, tuple(row))
                # the connection is not auto committed by default, so we must commit to save our changes
                self.connection.commit()

            cursor = self.connection.cursor()
            sqlUpdate = "update users set food_update = '%s' where username = '%s';" \
                        % (first_new_day, self.username)
            cursor.execute(sqlUpdate)
            self.connection.commit()

        except ValueError as vx:
            print(vx)
        except Exception as ex:
            print(ex)
        else:
            print("Successfully updated mfp.foods");


    def append_weights(self):
        weight_df = self.get_weight()
        first_new_day = np.min(weight_df.date)
        try:
            print("Deleting data since %s" % first_new_day)
            cursor = self.connection.cursor()
            sql_Delete_query = "DELETE FROM weight WHERE date >= %s and username = '%s';" \
                               % (first_new_day, self.username)
            cursor.execute(sql_Delete_query)
            self.connection.commit()

            # creating column list for insertion
            cols = "`,`".join([str(i) for i in weight_df.columns.tolist()])
            cursor = self.connection.cursor()
            # Insert DataFrame records one by one.
            for i, row in weight_df.iterrows():
                sql = "INSERT INTO `weight` (`" + cols + "`) VALUES (" + "%s," * (len(row) - 1) + "%s)"
                cursor.execute(sql, tuple(row))
                # the connection is not auto committed by default, so we must commit to save our changes
                self.connection.commit()

            cursor = self.connection.cursor()
            sqlUpdate = "update users set weight_update = '%s' where username = '%s';" \
                        % (first_new_day, self.username)
            cursor.execute(sqlUpdate)
            self.connection.commit()

        except ValueError as vx:
            print(vx)
        except Exception as ex:
            print(ex)
        else:
            print("Successfully updated mfp.weight");

    def update_all(self):
        food = self.append_foods()
        weight = self.append_weights()

    def __del__(self):
        if self.connection.is_connected():
            self.connection.close()
            print("MySQL connection is closed")
        print("Refreshment object destroyed!")

