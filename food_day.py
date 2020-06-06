import myfitnesspal
from datetime import date, timedelta
import pandas as pd


# input is the object returned by client.get_date(date)
def food_day(client_day, username):
    # set up empty df structure
    df = pd.DataFrame({"date": [],
                       "meal": [],
                       "food": [],
                       'calories': [],
                       'carbohydrates': [],
                       'fat': [],
                       'protein': [],
                       'sodium': [],
                       'sugar': []})
    # Set up date value and loop through each meal
    this_date = str(client_day.date.year) + '-' + str(client_day.date.month) + '-' + str(client_day.date.day)
    for meal in range(len(client_day.meals)):
        meal_name = client_day.meals[meal].name
        for e in range(len(client_day.meals[meal].entries)):
            # sometimes short_name is empty
            food_name = None
            if client_day.meals[meal].entries[e]._short_name:
                food_name = client_day.meals[meal].entries[e]._short_name.strip()
            else:
                food_name = client_day.meals[meal].entries[e].name
            # create a new row for each food entry
            this_food = pd.DataFrame({"date": [this_date],
                                      "username": [username],
                                      "meal": [meal_name],
                                      "food": food_name, # might need to chop this down to 45 chars
                                      "unit": client_day.meals[meal].entries[e].unit,
                                      "quantity": client_day.meals[meal].entries[e].quantity,
                                      'calories': client_day.meals[meal].entries[e].totals['calories'],
                                      'carbohydrates': client_day.meals[meal].entries[e].totals['carbohydrates'],
                                      'fat': client_day.meals[meal].entries[e].totals['fat'],
                                      'protein': client_day.meals[meal].entries[e].totals['protein'],
                                      'sodium': client_day.meals[meal].entries[e].totals['sodium'],
                                      'sugar': client_day.meals[meal].entries[e].totals['sugar']})
            df = df.append(this_food)
    # return df that is a whole days worth of food
    return df

