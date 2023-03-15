# Wikipedia Edit Analysis, The relationship between wikipedia Edits on congressmen and the political events in real life

 This code analyzes the number of edits made to all Wikipedia articles over time as well as the ones specifically made on congressmen's pages.<br>
 It loads data from JSON files (each representing one edit made on a congressman's page on wikipedia in the Data folder and combines it with data from a CSV file named undefined.csv which includes the number of edits made on the entire platform on daily basis that has been obtained from Wikimedia website. <br>
 The resulting data is then saved as an Excel file named TheWholeThing1.xlsx. <br>
 The detrend Using "wikipedia1-moving average-SignificantEvents-Daily.py" is a Python code file that analyzes the number of edits made to all the Wikipedia page as well the ones made only to the Congressmen's pages on wikipedia. It produces a plot that shows the ratio of edits made to Congressmen's pages to total user activity over time.

# Dependencies
. calendar <br> . pandas <br> . datetime <br> . math <br> . numpy <br> . sm <br> . seasonal <br> . matplotlib <br> . json <br> . os <br> . collections <br> . random <br> . seaborn <br> . warnings

# Usage

 The dataset used in this project can be found in the "Data" folder. <br> To run the code, simply execute the following command:
 python "SaveTheFullCongress.py"
 The output will be saved as an Excel file named "TheWholeThing1.xlsx".
 Given the size of the congress files and depending on your processing power running this code might take a while.
 
 To use the "detrend Using wikipedia1-moving average-SignificantEvents-Daily.py" code, simply run the Python file in a Python environment. The code will produce a plot that shows the ratio of edits made on Congressmen's pages to total user activity over time.



# Methodology
 The code reads the JSON files in the "Data" folder, extracts the timestamp of each edit and aggregates the edits by day. <br>
 The resulting time series dataset is then merged with a complete range of timestamps to fill in missing days with a frequency of 0. <br>

 The dataset is then plotted using seaborn and matplotlib to visualize the pattern of Wikipedia edits over time.

# Results
 The resulting Excel file contains two columns: "Time_Stamp" and "Number of Edits". The "Time_Stamp" column contains a complete range of timestamps from the earliest to latest edit, with a frequency of 1 day. The "Number of Edits" column contains the number of edits made on each day.

The resulting time series plot shows a seasonal pattern, with higher edit frequencies in certain months. Further analysis using time series models can be done to identify the underlying pattern and make predictions on future edit frequencies.
