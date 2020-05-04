#Author: John Dellape
#Last Updated: 5/4/2020

'''
This is a simple script to pull the updated New York Times data on COVID-19 cases and deaths
for all PA counties as of the current day.
NEXT STEP: Update this file to be scheduled to run each day and deploy to Heroku for automation.
'''


#Import the necessary libraries
import pandas as pd
from datetime import date, timedelta
import pygsheets

#Pull down the information posted by the NYTimes
df = pd.read_csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv')



#Set a variable for yesterday. Since as of today, the New York Times has the reported totals from the states from yesterday.
#Therefore, to isolate just the most recent day for PA counties, we will isolated where date = yesterday and state = Pennsylvania
yesterday = date.today() - timedelta(days=1)
yesterday = str(yesterday)


#Prepare dataframe (pa_df) which will be output to my google spreadsheet
columns_to_keep = ['county', 'state', 'cases', 'deaths', 'date']
pa_df = pa_df[columns_to_keep]
pa_df = pa_df[df.date == yesterday]
pa_df = pa_df[df.state == 'Pennsylvania']


pa_df['date'] = pa_df['date'].replace(yesterday, today)
pa_df['state'] = pa_df['state'].replace('Pennsylvania', 'PA')


#Make a list of all the rows in my dataframe
df_length = len(pa_df)
row_list = []
idx = 0

while idx < df_length:
    df_row = pa_df.iloc[idx].values
    clean_row = []
    for item in df_row:
        item = str(item)
        clean_row.append(item)
    row_list.append(clean_row)
    idx = idx + 1


#Append the rows to my google spreadsheet
gc = pygsheets.authorize(service_file='/Users/della/SDDS/SDDSProject-3c298c43dcbd.json')
sh = gc.open('Covid19PA_DEV')
wks = sh[0]
for row in row_list:
    wks.append_table(row,dimension='ROWS',overwrite='False')





