# Import necessary libraries
import calendar
import json
import os
import random
import warnings
from collections import Counter
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import sm as sm
from datetime import datetime
from seasonal import fit_seasons, adjust_seasons
import seaborn as sns
import matplotlib.pyplot as plt

# Ignore warnings for cleaner output
warnings.filterwarnings("ignore")
# Read the CSV file into a Pandas DataFrame
df = pd.read_csv('wikipedia_data_extended (1).csv')

# Convert the timestamp column to a datetime object
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Group the DataFrame by the timestamp column and count the number of rows in each group
grouped = df.groupby(pd.Grouper(key='timestamp', freq='D')).size().reset_index(name='Number of Edits')

# Set the timestamp column as the index of the grouped DataFrame
#grouped.set_index('timestamp', inplace=True)
grouped=grouped[:7902]
grouped.columns=['Time_Stamp', 'Number of Edits']
# Read in data and create dataframes
Congress = pd.DataFrame(grouped)
Congress_df = pd.DataFrame(Congress, columns=['Time_Stamp', 'Number of Edits'])
#Congress_df = Congress_df[5:]
#Congress_df['Time_Stamp'] = Congress_df['Time_Stamp'].str.replace('+00:00', '')
# Read Wikipedia data and calculate daily averages
wikipedia_data = pd.read_csv("undefined.csv")
wikipedia_data['day'] = pd.to_datetime(wikipedia_data['month'])
daily_data = wikipedia_data.groupby(pd.Grouper(key='day', freq='D'))['total.total'].mean()
daily_data_df = pd.Series(daily_data).to_frame()
daily_data_df.columns = ['Number of edits']
daily_data_df = daily_data_df.reset_index().rename(columns={'index': 'Time_Stamp'})
daily_data_df['day'] = pd.to_datetime(daily_data_df['day'])
daily_data_df['day'] = daily_data_df['day'].dt.strftime('%Y-%m-%d')
daily_data_df = daily_data_df.rename(columns={'day': 'Time_Stamp'})
daily_data_df=daily_data_df[52:]
daily_data_df=daily_data_df[:-100]
# Convert timestamp to datetime format and set as index
daily_data_df['Time_Stamp'] = pd.to_datetime(daily_data_df['Time_Stamp'])
Congress_df['Time_Stamp'] = pd.to_datetime(Congress_df['Time_Stamp'])
daily_data_df.set_index('Time_Stamp', inplace=True)
Congress_df['Time_Stamp'] = Congress_df['Time_Stamp'].dt.tz_localize(None)
Congress_df.set_index('Time_Stamp', inplace=True)

result = pd.concat([daily_data_df, Congress_df], axis=1, ignore_index=True)
# Resample Congress_df to daily frequency using mean aggregation
Congress_daily = Congress_df.resample('D').sum()
import matplotlib.pyplot as plt


# get the ratio of congressman_df and monthly_df
ratio = result[1] / result[0]
import pandas as pd
import matplotlib.pyplot as plt

# assuming daily_data_df, Congress_df and ratio are already defined
detrended_ratio_ma = ratio.rolling(window=14).mean()
# Create a list of timestamps of election years
congress_election_years = [
    '2002-11-01',
    '2004-11-01',
    '2006-11-01',
    '2008-11-01',
    '2010-11-01',
    '2012-11-01',
    '2014-11-01',
    '2016-11-01',
    '2018-11-01',
    '2020-11-01'
]
congress_election_years = [pd.to_datetime(year).year for year in congress_election_years]
congress_election_years = [pd.Timestamp(year=year, month=11, day=1) for year in congress_election_years]

# plot the ratio with log y-axis and the first column of both data frames on the x-axis
fig, ax = plt.subplots(figsize=(10, 6))

# plot the lines
ax.plot(daily_data_df,label="Total User activity")
ax.plot(Congress_df,label="Congress activity")
ax.plot(ratio, label="Detrended" )
ax.plot(detrended_ratio_ma, label="7-day Moving Average of Ratio")
# set yscale to log
ax.set_yscale('log')

# set title and labels
ax.set_title('Congressman / Monthly Ratio')
ax.set_xlabel('Date')
ax.set_ylabel('Ratio (log scale)')

# add vertical lines at election years
#for year in congress_election_years:
#    ax.axvline(year, color='grey', linestyle='--')

# add vertical shaded area at election years
for year in congress_election_years:
    start = pd.Timestamp(year=year.year, month=11, day=1)
    end = pd.Timestamp(year=year.year+1, month=1, day=3) if year.year != 2020 else pd.Timestamp(year=year.year+1, month=1, day=3)
    ax.axvspan(start, end, color='grey', alpha=0.3)
# add a legend
ax.legend()

# show the plot
plt.show()
