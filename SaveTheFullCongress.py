import calendar

import pandas as pd
from datetime import datetime
import math
import numpy as np
import sm as sm
from seasonal import fit_seasons, adjust_seasons
import matplotlib.pyplot as plt
## todo: ~~~~~~~~~~~~
import warnings
warnings.filterwarnings("ignore")
## todo: ~~~~~~~~~~~~

import json
import os
import pandas as pd
from collections import Counter
# Create an empty list to store the data frames
from collections import Counter
import datetime
## todo: ~~~~~~~~~~~~
import warnings
warnings.filterwarnings("ignore")
## todo: ~~~~~~~~~~~~

import json
import os
import pandas as pd
from collections import Counter
# Create an empty list to store the data frames
from collections import Counter
from datetime import datetime

import random
from datetime import  datetime, timedelta
import seaborn as sns
from matplotlib import pyplot as plt, pyplot
import math
import random

import seaborn as sns
from matplotlib import pyplot as plt
import math
data_frames = []

dater = dict()

for folder in os.listdir("Data"):
    # Skip the ".DS_Store" folder and the "wikipediarevs.log" file
    if folder == ".DS_Store" or folder == "wikipediarevs.log":
        continue

    # Load the data from each JSON file in the folder into a data frame
    df = pd.DataFrame()
    for file in os.listdir(f"Data/{folder}"):

        #if random.uniform(0, 1) > 0.002: continue

        if file.endswith(".json"):
            with open(f"Data/{folder}/{file}") as f:
                try:
                    file_data = json.load(f)
                except json.decoder.JSONDecodeError:
                    print(f"json.decoder.JSONDecodeError, Data/{folder}/{file}")
            ts = datetime.strptime(file_data["timestamp"], '%Y-%m-%dT%H:%M:%SZ')
            ts = ts.replace(hour=0, minute=0, second=0)
            #print()
            #hour, day, month, year = ts.hour, ts.day, ts.month, ts.year

           # particular_hour = hour + day * 24 + month * 24 * 30.437 + year * 24 * 30.437 * 12
            if ts not in dater: dater[ts] = 0
            dater[ts] += 1

plotta = [(_dk, dater[_dk]) for _dk in dater.keys()]
plotta.sort(key=lambda x: x[0])

def fill_dates_between(date1, date2):
    date_vals = list()
    start_date = date1[0]
    end_date = date2[0]  # perhaps date.now()

    delta = end_date - start_date  # returns timedelta

    for i in range(delta.days + 1):
        day = start_date + timedelta(days=i)
        date_vals.append((day, 0))
    return date_vals


#test
#fill_dates_between(plotta[0], plotta[1])


#for _date in range(len(plotta)-1):
#    pre, post = plotta[_date], plotta[_date+1]
#    date_returns = fill_dates_between(pre, post)
#    plotta = plotta[:_date] + date_returns + plotta[_date:]


# Read the Wikipedia data
wikipedia_data = pd.read_csv("undefined.csv")
wikipedia_data['month'] = pd.to_datetime(wikipedia_data['month'])

# Convert the datetime format in the congressmen's data
plotta = [(x[0].strftime('%Y-%m-%d %H:%M:%S'), x[1]) for x in plotta]
plotta = [(datetime.strptime(x[0], '%Y-%m-%d %H:%M:%S'), x[1]) for x in plotta]
plotta_df = pd.DataFrame(plotta, columns=['Time_Stamp', 'Number of Edits'])

plotta_df['Time_Stamp'] = pd.to_datetime(plotta_df['Time_Stamp'])

# Set Timestamp column as index
plotta_df.set_index('Time_Stamp', inplace=True)

# Create a new DataFrame with a complete range of timestamps
full_range = pd.date_range(start=plotta_df.index.min(), end=plotta_df.index.max(), freq='D')
df_full = pd.DataFrame(index=full_range)

# Merge the two DataFrames on the index
df_merged = pd.merge(df_full, plotta_df, how='left', left_index=True, right_index=True)

# Fill missing values with 0 frequency
df_merged.fillna(0, inplace=True)
df_merged=df_merged.reset_index().rename(columns={'index': 'Time_Stamp'})
#df_merged=df_merged.groupby(df_merged['Time_Stamp'].dt.to_period('M')).sum()
#df_merged=df_merged.reset_index().rename(columns={'index': 'Time_Stamp'})
#df_merged.set_index('Time_Stamp', inplace=True)
df_merged.to_excel('TheWholeThing1.xlsx', index=False)