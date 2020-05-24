import myfitnesspal
from datetime import date, timedelta
import pandas as pd

# Set up client to call REST API
client = myfitnesspal.Client('brodyprows97')

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
todays_date = date.today()
one_week = timedelta(days=7)
one_week_ago = todays_date - one_week
# start_date = datetime.strptime("2017-8-6", "%Y-%m-%d")

# Loop through the dates

# for y in range(one_week_ago.year, todays_date.year + 1):
#     for m in range(one_week_ago.month, todays_date.month + 1):
#         for d in range(one_week_ago.day, todays_date.day + 1):
#             print(y, m, d)



day = client.get_date(todays_date.year, todays_date.month, todays_date.day)
this_date = str(todays_date.year) + '-' + str(todays_date.month) + '-' +str(todays_date.day)
for meal in range(len(day.meals)):
    meal_name = day.meals[meal].name
    for e in range(len(day.meals[meal].entries)):
        this_food = pd.DataFrame({"date": [this_date],
                                  "meal": [meal_name],
                                  "food": day.meals[meal].entries[e].name,
                                  'calories': day.meals[meal].entries[e].totals['calories'],
                                  'carbohydrates': day.meals[meal].entries[e].totals['carbohydrates'],
                                  'fat': day.meals[meal].entries[e].totals['fat'],
                                  'protein': day.meals[meal].entries[e].totals['protein'],
                                  'sodium': day.meals[meal].entries[e].totals['sodium'],
                                  'sugar': day.meals[meal].entries[e].totals['sugar']})
        df = df.append(this_food)

print(df)
