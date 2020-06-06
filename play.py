import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde, norm
from sqlalchemy import create_engine
import datetime

print("Connecting to mySQL on AWS")
sqlEngine       = create_engine('mysql+pymysql://mfp_brody:mfp_brody@mfp.cnx1wcpcowpl.us-east-2.rds.amazonaws.com:3306/mfp', pool_recycle=3600)
dbConnection    = sqlEngine.connect()
print("Connection Successful")

sql = "select * from mfp.foods where username = 'brodyprows97';"
df = pd.read_sql(sql, con=dbConnection)
df['year'] = pd.DatetimeIndex(df['date']).year
df['month'] = pd.DatetimeIndex(df['date']).month
df['day'] = pd.DatetimeIndex(df['date']).day
by_day = df.drop(['id'], axis=1).groupby(['day', 'month', 'year']).sum()
by_day.reset_index(level=['day','month','year'], inplace=True)

density = gaussian_kde(by_day.calories)
xs = np.linspace(100,3000,2000)
density.covariance_factor = lambda: .25
density._compute_covariance()
plt.plot(xs,density(xs))
y = norm.pdf(xs,np.mean(by_day.calories),np.std(by_day.calories))
plt.plot(xs,y)
plt.show()

print("Examine Plots by month")
by_month = by_day.groupby(['month', 'year']).mean()
by_month.reset_index(level=['month', 'year'], inplace=True)

# Define years to loop through
years = by_day.year.unique()
years.sort()
xs = np.linspace(100, 3000, 2000)
density.covariance_factor = lambda: .25
density._compute_covariance()
for y in years:
    # Define Months to loop through in a given year
    months = by_day.loc[by_day.year == y].month.unique()
    months.sort()
    for m in months:
        cals = by_day.loc[(by_day.year == y) & (by_day.month == m)].calories
        density = gaussian_kde(cals)
        plt.plot(xs, density(xs))
        ys = norm.pdf(xs, np.mean(by_month.calories), np.std(by_month.calories))
        plt.plot(xs, ys)
        plt.xlabel('Daily Calories')
        plt.ylabel('Density')
        plt.title('Daily Calories for %s - %s' % (datetime.date(1900, m, 1).strftime('%B'), y))
        plt.show()

# Once we get weights, want to have a daul axis that have weight
# trends over time, at the same date as a weigh-in show the avg.
# daily calories since the last weight-in