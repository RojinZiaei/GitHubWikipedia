import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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
daily_data_df=daily_data_df[51:]
daily_data_df=daily_data_df[:-100]

# Convert the date column to a datetime data type if it isn't already
daily_data_df['Time_Stamp'] = pd.to_datetime(daily_data_df['Time_Stamp'])

# Filter the DataFrame to include only rows with dates after or equal to '2003-11-15 00:00:00'
daily_data_df = daily_data_df[daily_data_df['Time_Stamp'] >= '2003-11-15 00:00:00']

# Read the CSV file into a Pandas DataFrame
df = pd.read_csv('wikipedia_data_extended (1).csv')

# Convert the timestamp column to a datetime object
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Filter the dataframe to only include rows where the party is 'Democrat'
df_democrat = df[df['party'] == 'Democrat']

# Group the DataFrame by the timestamp column and count the number of rows in each group
groupedDem = df_democrat.groupby(pd.Grouper(key='timestamp', freq='D')).size().reset_index(name='Number of Edits')
groupedDem['timestamp'] = groupedDem['timestamp'].dt.tz_localize(None)

# Read the CSV file into a Pandas DataFrame
df1 = pd.read_csv('wikipedia_data_extended (1).csv')

# Convert the timestamp column to a datetime object
df1['timestamp'] = pd.to_datetime(df1['timestamp'])

# Filter the dataframe to only include rows where the party is 'Republican'
df_republican = df1[df1['party'] == 'Republican']

# Group the DataFrame by the timestamp column and count the number of rows in each group
groupedRep = df_republican.groupby(pd.Grouper(key='timestamp', freq='D')).size().reset_index(name='Number of Edits')
groupedRep['timestamp'] = groupedRep['timestamp'].dt.tz_localize(None)

# create a new dataframe with only Time_Stamp and Ratio_Democrat columns
Ratio_dem = pd.DataFrame({
    'Time_Stamp': groupedDem['timestamp'],
    'Ratio_Democrat': groupedDem['Number of Edits'] / daily_data_df['Number of edits']
})

# create a new dataframe with only Time_Stamp and Ratio_Republican columns
Ratio_rep = pd.DataFrame({
    'Time_Stamp': groupedRep['timestamp'],
    'Ratio_Republican': groupedRep['Number of Edits'] / daily_data_df['Number of edits']
})

# merge the two dataframes on Time_Stamp
merged_df_temp = pd.merge(daily_data_df, Ratio_dem, on='Time_Stamp')
merged_df_temp1 = pd.merge(daily_data_df, Ratio_rep, on='Time_Stamp')

# calculate
# calculate the 7-day moving average for both parties
dem_ma = Ratio_dem['Ratio_Democrat'].rolling(14).mean()
rep_ma = Ratio_rep['Ratio_Republican'].rolling(14).mean()
dem_ma = dem_ma.fillna(0)
rep_ma = rep_ma.fillna(0)

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
# Calculate the 7-day rolling average of the ratio of edits for each political affiliation
Ratio_dem['Ratio_Democrat_MA'] = Ratio_dem['Ratio_Democrat'].rolling(window=14).mean()
Ratio_rep['Ratio_Republican_MA'] = Ratio_rep['Ratio_Republican'].rolling(window=14).mean()
#Create a line plot of the data
fig, ax = plt.subplots()

ax.plot(Ratio_dem['Time_Stamp'], Ratio_dem['Ratio_Democrat_MA'], color='blue', label='Democratic Edits')
ax.plot(Ratio_rep['Time_Stamp'], Ratio_rep['Ratio_Republican_MA'], color='red', label='Republican Edits')

#Create gray background for election year
for year in congress_election_years:
    ax.axvspan(year, year + pd.DateOffset(months=3), facecolor='gray', alpha=0.3)

#Set the x-axis labels to display the time stamps
plt.xticks(rotation=45, ha='right')
ax.set_xlabel('Time Stamp')

ax.set_ylabel('Ratio of Edits')
ax.set_yscale('log')
ax.set_title('Ratio of Edits by Political Affiliation over Time (14-day Moving Average)')
ax.legend()

#Display the plot
plt.show()