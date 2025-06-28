''' In order for this code to work you need to install first the following python libraries:
python3.11 -m pip install pandas
python3.11 -m pip install numpy
python3.11 -m pip install bs4

Then you need to wget https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMSkillsNetwork-PY0221EN-Coursera/labs/v2/exchange_rate.csv

The following code was made on the main wikipedaia page instead of the archive one hence the different banks ranked.
You may find the banks at: https://en.wikipedia.org/wiki/List_of_largest_banks
'''

# Importing the required python libraries
import requests
import sqlite3
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import os

# Declaring known values
url = "https://en.wikipedia.org/wiki/List_of_largest_banks"
exchange_csv = "./exchange_rate.csv"
table_attribs = ["Name", "Assets_USD_Billion"]
output_csv = "./Largest_banks_data.csv"
db_name = "Largest_Banks.db"
table_name = "Largest_banks"
log_file = "./stage_log.txt"

# Task 1: Logging function
def log_progress(message):
    ''' This function logs all messages of a stage of the
    code execution to a stage log file. Returns nothing'''

    timestamp_format = "%Y-%h-%d-%H:%M:%S" # Year-Monthname-Day-Hour-Minute-Second
    now = datetime.now() # gets the current timestamp
    timestamp = now.strftime(timestamp_format)
    with open(log_file,'a+') as f:
            f.write(timestamp + " : " + message + "\n")

# Task 2: Extraction of data
def extract(url, table_attribs):
    ''' This function extracts required information from the banks website table and save it to a data frame.
    The function returns data frame for further processing by other functions called below. '''

    page = requests.get(url).text
    soup = BeautifulSoup(page, "html.parser")

    df = pd.DataFrame(columns=table_attribs)

    tables = soup.find_all("tbody")
    rows = tables[0].find_all("tr")

    for row in rows:
        col = row.find_all("td")
        if len(col)!=0:
            data_dict = {"Name": col[1].find_all("a")[1]["title"],
                         "Assets_USD_Billion": float(col[2].contents[0][:-1].replace(',','',))}
            df1 = pd.DataFrame(data_dict, index=[0])
            df = pd.concat([df, df1], ignore_index=True)
    return df

# Task 3: Transformation of data
def transform(df, exchange_csv):
    ''' This function accesses exchange rate CSV file, and adds three columns to the data frame, each
    containing the transformed version of Assets column to currencies counted based on the currency CSV file'''

    # Read exchange rate CSV file
    exchange_rate = pd.read_csv(exchange_csv)

    # Convert to a dictionary with "Currency"
    exchange_rate = exchange_rate.set_index("Currency").to_dict()["Rate"]

    # Split assets to respective currency assets and add columns to the data frame. Round numbers to two decimals.
    df["Assets_GBP_Billion"] = [np.round(x * exchange_rate["GBP"], 2) for x in df["Assets_USD_Billion"]]
    df["Assets_EUR_Billion"] = [np.round(x * exchange_rate["EUR"], 2) for x in df["Assets_USD_Billion"]]
    df["Assets_INR_Billion"] = [np.round(x * exchange_rate["INR"], 2) for x in df["Assets_USD_Billion"]]
    return df

# Task 4: Loading data to Largest_banks_data.csv
def load_to_csv(df, output_csv):
    df.to_csv(output_csv)

# Task 5: Connecting and loading data to Largest_Banks.db
def load_to_db(df, sql_connection, table_name):
    df.to_sql(table_name, sql_connection, if_exists='replace', index=False)

# Task 6: Function to Run queries on Database
def run_query(query_statement, sql_connection):
    query_output = pd.read_sql(query_statement, sql_connection)
    print(query_statement)
    print(query_output)

# Task 7a: Verify log entries by printing them
with open(log_file, "r") as log:
    LogContent = log.read()
   


''' Below portion of the code is outside functions. The defined functions are being called here in respective order
to carry out necessary tasks so the execution of the code may succeed.'''

log_progress("Initiation complete. Starting ETL process")

#extract()
df = extract(url, table_attribs)
print(f"\n\n\nThe extracted Data Frame looks as below:\n\n",df)

log_progress("Data extraction complete. Starting data transformation process")

#transform()
df = transform(df, exchange_csv)
print(f"\n\n\nThe transformed Data Frame looks as below:\n\n",df)

log_progress("Data transformation complete. Starting data loading process")

#load_to_csv()
load_to_csv(df, output_csv)
log_progress("Data saved to CSV file")

#SQLite3 connection
sql_connection = sqlite3.connect(db_name)
log_progress("SQL connection opened")

#load_to_db()
load_to_db(df, sql_connection, table_name)
log_progress("Data loaded to database table, Starting queries")

#Run_query()
#1. Print all contents of the table
query_statement = f"\n\n\nSELECT Name, Assets_USD_Billion, Assets_GBP_Billion, Assets_EUR_Billion, Assets_INR_Billion from {table_name}\n"
run_query(query_statement, sql_connection)

#2. Print average market capitalization per Bank
query_statement = f"\n\nSELECT AVG(Assets_USD_Billion), AVG(Assets_GBP_Billion), AVG(Assets_EUR_Billion), AVG(Assets_INR_Billion) FROM {table_name}\n"
run_query(query_statement, sql_connection)

# 3. Print top 5 banks names
query_statement = f"\n\nSELECT Name from {table_name} LIMIT 5\n"
run_query(query_statement, sql_connection)

log_progress("Process Complete")

# Close DB connection
sql_connection.close()

log_progress("Database Connection closed")

#task7b
print("\n\n",LogContent)

# Mute warnings
def alert(*args, **kwargs):
    pass
import warnings
warnings.alert = alert
warnings.filterwarnings('ignore')
