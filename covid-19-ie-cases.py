from matplotlib import pyplot as plt
import numpy as np

import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Variables
population = 4937786
days = 7

# Get latest data in csv format
filename = 'covid-19-ie-cases.csv'

data_url = 'https://opendata.arcgis.com/datasets/d8eb52d56273413b84b0187a4e9117be_0.csv'

data_content = requests.get(data_url).content
csv_file = open(filename, 'wb')
csv_file.write(data_content)
csv_file.close()

df = pd.read_csv(filename)

# Calculations
df['7DayAverage'] = df['ConfirmedCovidCases'].rolling(7).mean()
df['14DayAverage'] = df['ConfirmedCovidCases'].rolling(14).mean()
df['14DayPer100K'] = df['ConfirmedCovidCases'].rolling(14).sum() / population * 100000
df['7DayPer100K'] = df['ConfirmedCovidCases'].rolling(7).sum() / population * 100000

# Format columns
df['Date'] = pd.to_datetime(df['Date']).dt.date
df['7DayAverage'] = df['ConfirmedCovidCases'].round(0).astype(pd.Int64Dtype())
df['14DayAverage'] = df['ConfirmedCovidCases'].round(0).astype(pd.Int64Dtype())
df['14DayPer100K'] = df['14DayPer100K'].round(0).astype(pd.Int64Dtype())
df['7DayPer100K'] = df['7DayPer100K'].round(0).astype(pd.Int64Dtype())

# Print table
df = df.tail(days)
print(df[["Date", "ConfirmedCovidCases", "7DayAverage", "14DayAverage", "14DayPer100K", "7DayPer100K"]])
